"""Encrypted DB/object snapshot and isolated restore. Credentials come from environment.

Use a private directory on an encrypted volume for temporary plaintext. Export
object bytes to an immutable snapshot directory first; pg_dump alone omits them.
Production PITR must also be enabled with the database hosting provider.
"""

import argparse
import hashlib
import json
import os
import secrets

# Fixed PostgreSQL executables with argument arrays, no shell.
import subprocess  # nosec B404
import tarfile
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import psycopg
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAGIC = b"ENATBACKUP1"
CHUNK = 1024 * 1024


def key_from(path):
    if path.stat().st_mode & 0o077:
        raise ValueError("Key file must be private (0600)")
    key = path.read_bytes()
    if len(key) != 32:
        raise ValueError("Backup key must contain exactly 32 random bytes")
    return key


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def crypt(source, destination, key, encrypt):
    with source.open("rb") as src, destination.open("xb") as dst:
        os.chmod(destination, 0o600)
        if encrypt:
            nonce = secrets.token_bytes(12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
            dst.write(MAGIC + nonce)
            cipher.authenticate_additional_data(MAGIC)
            while chunk := src.read(CHUNK):
                dst.write(cipher.update(chunk))
            dst.write(cipher.finalize() + cipher.tag)
        else:
            if src.read(len(MAGIC)) != MAGIC:
                raise ValueError("Invalid archive header")
            nonce = src.read(12)
            src.seek(-16, 2)
            tag = src.read(16)
            remaining = src.tell() - len(MAGIC) - 12 - 16
            if remaining < 0:
                raise ValueError("Truncated archive")
            src.seek(len(MAGIC) + 12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag)).decryptor()
            cipher.authenticate_additional_data(MAGIC)
            while remaining:
                chunk = src.read(min(CHUNK, remaining))
                if not chunk:
                    raise ValueError("Truncated archive")
                remaining -= len(chunk)
                dst.write(cipher.update(chunk))
            dst.write(cipher.finalize())


def pg_env(dsn):
    values = psycopg.conninfo.conninfo_to_dict(dsn)
    mapping = {
        "host": "PGHOST",
        "port": "PGPORT",
        "dbname": "PGDATABASE",
        "user": "PGUSER",
        "password": "PGPASSWORD",  # nosec B105
        "sslmode": "PGSSLMODE",
        "sslrootcert": "PGSSLROOTCERT",
        "sslcert": "PGSSLCERT",
        "sslkey": "PGSSLKEY",
    }
    if set(values) - set(mapping):
        raise ValueError("Unsupported backup DSN option")
    return {**os.environ, **{mapping[k]: v for k, v in values.items()}}


def pg(command, dsn, *args):
    if command not in {"pg_dump", "pg_restore"}:
        raise ValueError("Unsupported PostgreSQL executable")
    binary = Path(os.environ.get("PG_BIN", "/usr/lib/postgresql/16/bin")) / command
    if not binary.is_absolute():
        raise ValueError("PG_BIN must be a trusted absolute directory")
    # DSN/password never appears in argv or error output.
    result = subprocess.run(  # nosec B603
        [str(binary), *map(str, args)],
        env=pg_env(dsn),
        capture_output=True,
        timeout=3600,
    )
    if result.returncode:
        raise RuntimeError(command + " failed; inspect protected database logs")


def references_from(conn):
    urls = [
        r[0]
        for r in conn.execute(
            "SELECT audio_url FROM stage_audio_prompts WHERE audio_url IS NOT NULL UNION SELECT qr_code_url FROM summaries WHERE qr_code_url IS NOT NULL"
        )
    ]
    keys = []
    for url in urls:
        path = unquote(urlsplit(url).path)
        found = False
        for marker in ("/object/public/", "/object/authenticated/", "/object/sign/"):
            if marker in path:
                key = path.split(marker, 1)[1]
                if not key or Path(key).is_absolute() or ".." in Path(key).parts:
                    raise ValueError("Invalid artifact reference")
                keys.append(key)
                found = True
                break
        if not found:
            raise ValueError("Artifact URL needs an explicit supported object mapping")
    return sorted(set(keys))


def references(dsn):
    with psycopg.connect(dsn) as conn:
        return references_from(conn)


def backup(dsn, objects, output, key, workdir):
    if output.exists():
        raise ValueError("Backup destination already exists")
    with tempfile.TemporaryDirectory(dir=workdir, prefix="enat-backup-") as directory:
        root = Path(directory)
        dump = root / "database.dump"
        with psycopg.connect(dsn) as conn:
            conn.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            snapshot = conn.execute("SELECT pg_export_snapshot()").fetchone()[0]
            required = references_from(conn)
            pg(
                "pg_dump",
                dsn,
                "--format=custom",
                "--snapshot",
                snapshot,
                "--file",
                dump,
            )
        inventory = {}
        for path in sorted(objects.rglob("*")):
            if path.is_symlink():
                raise ValueError("Object snapshots must not contain symlinks")
            if path.is_file():
                inventory[path.relative_to(objects).as_posix()] = digest(path)
        if set(required) - inventory.keys():
            raise ValueError("Snapshot is missing database-referenced objects")
        manifest = {
            "database_sha256": digest(dump),
            "objects": inventory,
            "required_objects": required,
        }
        (root / "manifest.json").write_text(json.dumps(manifest))
        archive = root / "snapshot.tar"
        with tarfile.open(archive, "w") as tar:
            tar.add(dump, arcname="database.dump")
            tar.add(root / "manifest.json", arcname="manifest.json")
            for name in inventory:
                tar.add(objects / name, arcname="objects/" + name, recursive=False)
        if any(
            digest(objects / name) != checksum for name, checksum in inventory.items()
        ):
            raise ValueError("Object snapshot changed during backup")
        crypt(archive, output, key, True)
        return manifest


def restore(dsn, archive, objects, key, workdir):
    with psycopg.connect(dsn) as conn:
        if conn.execute(
            "SELECT EXISTS(SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg_toast%' AND c.relkind IN ('r','p'))"
        ).fetchone()[0]:
            raise ValueError("Restore requires an empty isolated target database")
    if objects.exists() and any(objects.iterdir()):
        raise ValueError("Restore object destination must be empty")
    with tempfile.TemporaryDirectory(dir=workdir, prefix="enat-restore-") as directory:
        root = Path(directory)
        plain = root / "snapshot.tar"
        crypt(archive, plain, key, False)  # Authenticate all bytes before any restore.
        with tarfile.open(plain) as tar:
            for item in tar.getmembers():
                if (
                    not item.isfile()
                    or Path(item.name).is_absolute()
                    or ".." in Path(item.name).parts
                ):
                    raise ValueError("Invalid snapshot entry")
            tar.extractall(root / "unpacked", filter="data")
        unpacked = root / "unpacked"
        manifest = json.loads((unpacked / "manifest.json").read_text())
        if digest(unpacked / "database.dump") != manifest["database_sha256"]:
            raise ValueError("Database checksum mismatch")
        for name, checksum in manifest["objects"].items():
            if (
                Path(name).is_absolute()
                or ".." in Path(name).parts
                or digest(unpacked / "objects" / name) != checksum
            ):
                raise ValueError("Object checksum mismatch")
        pg(
            "pg_restore",
            dsn,
            "--exit-on-error",
            "--single-transaction",
            "--dbname",
            psycopg.conninfo.conninfo_to_dict(dsn)["dbname"],
            unpacked / "database.dump",
        )
        import shutil

        objects.mkdir(parents=True, exist_ok=True)
        if (unpacked / "objects").exists():
            shutil.copytree(unpacked / "objects", objects, dirs_exist_ok=True)
        if set(references(dsn)) - manifest["objects"].keys():
            raise ValueError("Restored database references missing objects")
        return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["backup", "restore"])
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--key-file", type=Path, required=True)
    parser.add_argument(
        "--work-dir", type=Path, required=True, help="Private encrypted scratch volume"
    )
    args = parser.parse_args()
    name = "BACKUP_DATABASE_URL" if args.command == "backup" else "RESTORE_DATABASE_URL"
    dsn = os.environ.get(name)
    if not dsn:
        parser.error(name + " is required")
    key = key_from(args.key_file)
    if args.command == "backup":
        backup(dsn, args.objects, args.archive, key, args.work_dir)
    else:
        restore(dsn, args.archive, args.objects, key, args.work_dir)
    print(args.command + " completed; checksums and object references verified")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        raise SystemExit(
            "Backup/restore failed; check inputs and protected database logs"
        ) from None
