# Release delivery and live verification

Implemented 20 October 2026. These tools prepare and check release evidence;
they do not supply clinical approval, hosting accounts or production credentials.
No deployment or live patient evaluation was performed during implementation.

## Candidate publication

After reviewing and merging the change, dispatch **Publish verified release
candidate** from `master`. It calls the existing quality workflow, then builds
one candidate, smoke-tests and scans that image, and runs the full 30-minute
Compose capacity/recovery harness before pushing the same image to
`ghcr.io/<repository>`. GHCR is the default proposed registry; change it deliberately
if the deployment uses another registry. Repository Actions must have package
write permission. Confirm package visibility and host read access before use.
The workflow uses GitHub's documented [reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
and [container publication](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)
mechanisms.

Download `release-evidence-<revision>-<attempt>`. Its root contains `release.json`,
security evidence and capacity reports. The JSON binds the full source revision,
registry manifest digest, Docker image ID, dependency lock hashes and evidence
file hashes. All R1–R8 decisions start pending. Reports are retained by the
workflow for 90 days, subject to repository limits; copy the bundle to the
approved protected archive for longer retention. A failed job may leave useful
failure artifacts, but cannot produce a valid patient-release approval.

```bash
.venv/bin/python scripts/release_record.py validate artifacts/release.json
.venv/bin/python scripts/release_record.py validate artifacts/release.json --mode pilot
```

The first command checks technical eligibility for staging. The second must
fail until R1–R7 have explicit owner/reviewer acceptance. Each accepted gate
requires `accepted_at`, the matching `source_revision` and `image`, and at least
one evidence entry containing a relative `path` and its `sha256`. Evidence must
remain within the downloaded bundle. A `decision` additionally requires:

```json
{
  "mode": "pilot",
  "environment_id": "the-provisioned-production-id",
  "rollback_image": "registry/repository@sha256:<64-hex-digest>",
  "approved_at": "<timezone-aware-review-date>",
  "approvers": {"clinical": "<name>", "privacy": "<name>", "operations": "<name>"},
  "bootstrap": false
}
```

Production expansion requires all R1–R8 accepted and a `production` decision.
Candidate evidence expires after seven days; source/container scans must have
been generated within the day preceding candidate creation. Rebuild/retest or
renew evidence deliberately when it is stale. The checker verifies consistency,
not reviewer identities or digital signatures: protect bundle access, use the
organization's approval process and preserve the approved copy separately.
Editing JSON is not authorization to invent acceptance.

## Host deployment

Provision TLS ingress, readiness routing, secret storage, database/Storage,
monitoring and backup destinations using the operations runbook. Install Docker
Compose and Python on the deployment host. Use a clean checkout at the release's
source revision and authenticate the host to the private registry independently.
The deployment tool uses the host's configured Docker endpoint/context.

Copy `deploy/target.example.json` outside the repository and fill its actual
environment ID and absolute API/worker/migration environment-file paths. Those
files must have no group/world permissions, such as mode 0600. The target
`environment` must be `staging` for staging mode or `production` for pilot/full
release. Host target IDs must match the requested and approved IDs.

```bash
python3 scripts/deploy_release.py /protected/release/release.json   --mode staging --environment-id YOUR_STAGING_ID   --target /etc/enat/staging/target.json
```

This validates without deployment. Add `--apply` to pull the exact image, verify
its Docker ID and source-revision label, take the host deployment lock, run migrations, and update each API,
worker and scheduler with readiness checks. Ingress must stop routing to an API
that is not ready. On a rollout failure, the tool attempts to restore changed
services to their previous images. It retains additive schema changes and reports
rollback failure explicitly. It never claims to undo an incompatible migration;
compatibility is an R2/R7 acceptance requirement.

Pilot/full production requires all existing services to match the separately
approved rollback image. For the first pilot only, `--bootstrap` is supported
when the signed-off decision also has `bootstrap: true` and there are no existing
services. A distinct tested rollback digest is still mandatory. Partial existing
stacks cannot bypass the rollback baseline check. Rehearse these paths on the
actual host and ingress before accepting R7. Application readiness does not prove
external routing, notification delivery or database/object recovery.

## Live Auth and isolation checks

Create two confirmed synthetic users in the isolated staging project. Copy
`deploy/staging-checks.example.json` outside Git and enter the API origin,
project/environment ID and expected application user UUIDs. Supply these four
environment variables from the secret manager:

- `ENAT_STAGING_EMAIL_A`, `ENAT_STAGING_PASSWORD_A`
- `ENAT_STAGING_EMAIL_B`, `ENAT_STAGING_PASSWORD_B`

```bash
.venv/bin/python scripts/staging_verify.py   --config /protected/staging-checks.json   --confirm-origin https://YOUR_STAGING_HOST   --output artifacts/staging-auth-new-run.json
```

The runner requires an exact HTTPS-origin confirmation, a staging declaration
and synthetic-account declaration before network use. It does not infer the real
hosting environment from a hostname; the operator must validate that mapping.
It ignores `.env` and proxy environment variables and refuses redirects.
It checks live login, profile ownership, empty draft creation with an idempotency
key, cross-user draft denial, bounded history, refresh, logout, family revocation
and isolation of the other account. Issued sessions are logged out best-effort,
including on failure; investigate cleanup failures. Empty drafts remain subject
to existing expiry. Reports contain check names/statuses, never credentials or
response bodies. No clinical records are finalized and no voice calls are made.

This is a partial R3 check, not a substitute for email/recovery delivery, signing
key rotation, account disabling, Telegram, every resource-family isolation case,
direct database grants or Storage grants. Those remain explicit staging cases.

## Live authentication capacity

Prepare a private mode-0600 JSON file with `environment: staging`, `environment_id`,
`api_origin`, `synthetic_accounts_only: true`, `auth_kind` (`supabase` or `opaque`),
and an `accounts` array. Each account needs `user_id`, `access_token` and a
timezone-aware `expires_at`. Use dedicated identities, not patient sessions.
Acquire tokens shortly before the run with expiry beyond the entire test.

```bash
.venv/bin/python scripts/staging_load.py   --config /protected/staging-load-tokens.json   --confirm-origin https://YOUR_STAGING_HOST --rps 1 --seconds 60   --output artifacts/staging-load-new-run.json
```

Agree Auth/provider and edge quotas before increasing load. Limits are 50 RPS,
30 minutes, 100 concurrent requests and 1,000 identities. Per-user planned traffic
must stay below 100 requests/minute, leaving room under the application quota;
50 RPS requires at least 30 identities. The tool checks each token's actual user
before starting. Traffic is 80% bounded history and 20% profile reads, with real
Auth verification for Supabase tokens. Every scheduled request remains in the
failure denominator, including transport errors and generator saturation.
Latency includes scheduling delay. Do not adjust targets to conceal failures.

Run separate reports for opaque/Supabase paths. These are read-capacity results;
voice, writes, mobile networking and failure injection remain separate R6/R7
exercises. Run the existing mixed-write Compose harness as well.

## Amharic evaluation

The scorer accepts captured results; it does not contact a provider or approve
clinical policy. Keep corpus/audio/predictions in protected storage outside Git.
A corpus is JSON with `version` and nonempty `cases`. Each case has a unique
opaque `id`, `transcript`, a `fields` object and `danger_categories` string array.
Predictions have the same complete set of case IDs, `corpus_sha256`,
`source_revision`, `provider`, `prompt_version`, `policy_version`, `generated_at`
and `cases` in the same format. Use actual captured provider outputs; do not
copy reference labels into predictions. Record model identifiers separately if
available. Human review must verify the capture and label provenance.

A clinical reviewer must fill `deploy/voice-policy.example.json` with their name,
approval date, minimum case/danger-case counts, maximum word-error rate and minimum
field accuracy, danger recall and precision. Null defaults deliberately fail.
The policy must predate the captured predictions. Include representative dialect,
noise, uncertainty, negation, corrections and silence; sample size/representativeness
remain reviewer responsibilities.

```bash
.venv/bin/python scripts/evaluate_voice.py   --corpus /protected/corpus.json --predictions /protected/predictions.json   --policy /protected/approved-policy.json --output artifacts/voice-score.json
```

Scoring uses Unicode NFC plus whitespace tokenization for word error, exact
field-value matches over the union of expected/predicted keys, and micro-averaged
danger-label precision/recall. Empty, duplicate, incomplete or mismatched corpora
fail closed. Reports contain aggregate scores and input hashes, not transcripts.
They explicitly retain `clinical_release_approved: false`; TTS comprehension,
warning timing, clinician review and pilot acceptance are separate evidence.

## Remaining dependencies and work

The implemented tools support R2/R3/R4/R7 but do not close those gates. Still needed:

| Gate | External input or remaining implementation |
|---|---|
| R1 | Named owners/backups, hosting choice, budget, cohort and service targets. |
| R2 | Configured registry access and actual staging host/ingress/secrets; hosted execution of the new workflow and real deployment/rollback drill. |
| R3 | Dedicated live test users, actual Auth/Storage/database grants and remaining identity/authorization cases listed above. |
| R4 | Approved corpus, live provider capture, clinical thresholds and clinical/TTS comprehension review. |
| R5 | Owned export, deletion-review request tracking and privacy/share audit are implemented in migration 010. Assign the request owner and approve policy/support configuration; actual erasure, retention and processor/backup handling still need their approved specification. |
| R6 | Frontend repository/deployment, mobile journeys, 20-concurrent live voice measurements and approved monetary budgets. |
| R7 | Managed PITR/object snapshot scheduling and remote storage, host-loss tests, actual alert receiver/on-call acknowledgement, timed restore and live load. |
| R8 | Explicit pilot decision, supervised outcomes and review before expansion. |

These dependencies are not marked passed by synthetic tests or repository tooling.

## Local verification record

On 20 October, the final full suite passed **242 tests**, including 34 new tooling
regressions, with 62 integration tests skipped outside their dedicated harness
and 11 existing warnings. Coverage includes first-pilot fallback, failed rollback,
source-label mismatch, evidence tampering and staging/evaluation failures. The fresh
PostgreSQL harness passed 60 tests, with two legacy-only cases skipped; it applied
migrations 001–009. Ruff formatting/lint, configured strict mypy, Postman/OpenAPI
contracts, Bandit on the new operator tools, repository secret scanning and
Actionlint 1.7.7 passed. Live staging, registry publication and the hosted candidate
workflow were not executed. No current image vulnerability scan is claimed by
these local operator-tool checks.

The subsequent [privacy implementation](privacy-operations.md) adds application
features and migration 010. The earlier verification record above is retained;
current application unit/HTTP tests pass 250 cases and legacy database upgrade
tests pass 71 cases. Container/hosted verification is recorded separately when
completed; no patient release approval is implied.
