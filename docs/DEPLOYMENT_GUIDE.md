# Cloud Deployment & Distribution Guide (Option C: Containerized Cloud Web App)

This guide provides turn-key instructions for building, containerizing, deploying, and distributing **AnagramFrenzy** to public consumers.

---

## 1. Local Testing with Docker

Before pushing to the cloud, you can test the production image locally:

```bash
# Build & start container
docker compose up --build -d

# Verify health endpoint
curl -i http://localhost:8080/health

# Open in browser
open http://localhost:8080
```

---

## 2. Zero-Config Cloud Deployments

### Option C.1: Google Cloud Run (Recommended for Global Scale & Free Tier)
Cloud Run offers a generous free tier (2 million requests/month at $0/month) with auto-scaling to zero when idle.

```bash
# 1. Login & set GCP project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Build and deploy container directly from source directory
gcloud run deploy anagramfrenzy \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```
Upon completion, Cloud Run provisions a public HTTPS URL (e.g. `https://anagramfrenzy-xyz-uc.a.run.app`).

### Option C.2: Render / Railway (Single-Click Web Deployment)
1. Push this project repository to GitHub.
2. In **Render** or **Railway**:
   - Click **New Web Service** -> Select your GitHub repository.
   - Choose **Docker** as the Environment.
   - Set Port to `8080`.
   - Click **Deploy**.

---

## 3. Custom Domain & SSL Setup
To market the app professionally:
1. Purchase a domain from your registrar (e.g. Namecheap, Cloudflare, Google Domains): `anagramfrenzy.app` or `playanagramfrenzy.com`.
2. Map a `CNAME` or `A` record to your Cloud Run / Render / Railway service.
3. Managed HTTPS/SSL certificates are issued automatically.

---

## 4. GTM & Distribution Checklist
- [x] Deterministic Daily Challenge with puzzle sequence numbers (`/api/daily`).
- [x] Persistent `localStorage` streak tracking across calendar days.
- [x] One-click "Share Score" button with spoiler-safe emoji output for social feeds.
- [x] Containerized production `Dockerfile` with multi-worker `gunicorn` and non-root security.
- [x] OpenGraph meta tags configured for iMessage, WhatsApp, Twitter/X, and Slack link previews.
