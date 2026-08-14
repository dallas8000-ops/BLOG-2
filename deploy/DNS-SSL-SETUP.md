# Domain & SSL Setup

Production URL: https://blog-2-production-72bc.up.railway.app
Domain: blog-2-production-72bc.up.railway.app
Framework: django

## SSL
SSL/TLS is automatic on Vercel, Railway, and Fly.io custom domains.

## Stripe Webhook (production)
Update webhook URL to: `https://blog-2-production-72bc.up.railway.app/stripe/webhook/`

## Verification
```bash
curl https://blog-2-production-72bc.up.railway.app/stripe/health
```
Run readiness from Stripe Installer after deploy.
