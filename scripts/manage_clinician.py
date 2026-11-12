"""Provision an existing account using a separate restricted care operator login."""

import argparse
import os
from uuid import UUID

import psycopg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user_id", type=UUID)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--enable", action="store_true")
    action.add_argument("--disable", action="store_true")
    parser.add_argument("--display-name")
    args = parser.parse_args()
    if args.enable and (
        not args.display_name or not 1 <= len(args.display_name.strip()) <= 200
    ):
        parser.error("Enabling requires a display name of 1 to 200 characters")
    dsn = os.environ.get("CARE_OPERATOR_DATABASE_URL")
    if not dsn:
        parser.error("Set CARE_OPERATOR_DATABASE_URL to a separate care operator login")
    try:
        with psycopg.connect(dsn) as conn:
            role = conn.execute(
                "SELECT pg_has_role(current_user,'enat_care_operator','member') AND NOT rolsuper AND NOT rolbypassrls FROM pg_roles WHERE rolname=current_user"
            ).fetchone()
            if not role or not role[0]:
                raise SystemExit(
                    "A restricted enat_care_operator member login is required"
                )
            if args.enable:
                conn.execute(
                    "INSERT INTO clinician_profiles(user_id,display_name) VALUES(%s,%s) ON CONFLICT(user_id) DO UPDATE SET active=true,display_name=excluded.display_name,updated_at=now()",
                    (args.user_id, args.display_name.strip()),
                )
            else:
                result = conn.execute(
                    "UPDATE clinician_profiles SET active=false,updated_at=now() WHERE user_id=%s",
                    (args.user_id,),
                )
                if not result.rowcount:
                    raise SystemExit("Clinician profile not found")
    except psycopg.Error:
        raise SystemExit(
            "Provisioning failed; verify account ID, operator role, and schema"
        ) from None
    print("Clinician enabled" if args.enable else "Clinician disabled")


if __name__ == "__main__":
    main()
