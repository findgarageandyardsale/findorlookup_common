# findorlookup_common

Shared Python package used by the four FindOrLookup Django backends (`fcs`, `fgys`, `foh`, `fsf`) to standardize their AWS integration.

## What it provides

- `findorlookup_common.storage.s3` — `MediaStorage` + `StaticStorage` on S3 with presigned GET URLs.
- `findorlookup_common.email.send` — `send_branded(brand, template_name, context, to)`.
- `findorlookup_common.email.templates` — ported from Find Mobile Services' `mailer.ts`:
  - `verify_email`, `welcome`, `reset_password`, `login_notification`, `payment_success`.
- `findorlookup_common.email.layout` — shared HTML shell (logo, tri-color stripe, footer) that each app brands via a `Brand` dict.
- `findorlookup_common.settings.brand` — `Brand` TypedDict.
- `findorlookup_common.settings.validation.validate_prod_env(required=[...])` — fail-fast env check.

## Install (editable, from a FOL backend)

```
pip install -e ../../findorlookup_common
```

## Credentials

Credentials come from the EC2 **instance role** attached to each app's host. No `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` env vars needed in production. boto3 picks them up automatically.

## Email identity

- `From`: `<App Name> <noreply@findorlookup.com>` (display name per-app from `Brand.app_name`).
- `Reply-To`: `support@findorlookup.com` (shared triage inbox).
