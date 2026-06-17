# Blog-2 — Railway deployment

## Service setup

1. Railway project → **+ New → GitHub Repo → BLOG-2** (or use existing **BLOG-2** service).
2. Connect the **Postgres** plugin (not Postgres-Fintech) via `DATABASE_URL`.
3. Builder: **Dockerfile** (from `railway.toml`). Custom start command: **empty**.

## Variables (BLOG-2 web service only)

| Name | Value |
|------|--------|
| `DJANGO_SECRET_KEY` | long random string |
| `DJANGO_DEBUG` | `false` |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` — pick your Postgres service from the reference menu |

Optional:

| Name | Value |
|------|--------|
| `DJANGO_ALLOWED_HOSTS` | `.railway.app,.up.railway.app,healthcheck.railway.app` (auto-added when Railway env is detected) |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | GitHub OAuth |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | Contact form SMTP |

Do **not** set `PORT`.

## Deploy

**Deploy latest commit** from GitHub. Good build log: `load build definition from Dockerfile`.  
Good runtime log: `[blog-2] gunicorn on 0.0.0.0:8080`.

## Verify

`https://<your-railway-domain>/health/?format=json` → `{"status":"ok","service":"blog-2"}`

Portfolio live demo: `https://blog-2-production-72bc.up.railway.app`
