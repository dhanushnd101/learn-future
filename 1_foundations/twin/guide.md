# Deploying a Gradio + Gemini Application to Google Cloud Run

This guide covers the complete deployment process for a Gradio application that uses the Gemini API and Pushover notifications, including common troubleshooting steps.

---

# Architecture

```
User
   │
   ▼
Cloud Run (Gradio)
   │
   ├────────► Gemini API
   │
   └────────► Pushover API
```

---

# Prerequisites

Install the following:

- Homebrew
- Python 3.11+
- uv
- Docker Desktop
- Google Cloud SDK (gcloud)
- A Google Cloud Project with Billing Enabled

---

# 1. Install Google Cloud CLI

```bash
brew update
brew install --cask google-cloud-sdk
```

Add it to your shell:

```bash
echo 'source "$(brew --prefix)/share/google-cloud-sdk/path.zsh.inc"' >> ~/.zshrc

echo 'source "$(brew --prefix)/share/google-cloud-sdk/completion.zsh.inc"' >> ~/.zshrc

source ~/.zshrc
```

Verify:

```bash
gcloud --version
```

---

# 2. Authenticate

```bash
gcloud auth login
```

---

# 3. Configure your project

List projects:

```bash
gcloud projects list
```

Example:

```
Project ID:
gen-lang-client-0946793200

Project Name:
Udemy AI Engineer Agent Track

Project Number:
89072472602
```

Set the active project:

```bash
gcloud config set project gen-lang-client-0946793200
```

Verify:

```bash
gcloud config get-value project
```

---

# 4. Enable Required Services

```bash
gcloud services enable \
run.googleapis.com \
secretmanager.googleapis.com \
artifactregistry.googleapis.com \
cloudbuild.googleapis.com
```

---

# 5. Store Secrets

Create secrets once.

## Gemini

```bash
echo -n "YOUR_GEMINI_API_KEY" | \
gcloud secrets create GEMINI_API_KEY \
--data-file=-
```

## Google API Key

```bash
echo -n "YOUR_GOOGLE_API_KEY" | \
gcloud secrets create GOOGLE_API_KEY \
--data-file=-
```

## Pushover User

```bash
echo -n "YOUR_PUSHOVER_USER" | \
gcloud secrets create PUSHOVER_USER \
--data-file=-
```

## Pushover Token

```bash
echo -n "YOUR_PUSHOVER_TOKEN" | \
gcloud secrets create PUSHOVER_TOKEN \
--data-file=-
```

---

# Updating an Existing Secret

Create a new version.

Example:

```bash
echo -n "NEW_TOKEN" | \
gcloud secrets versions add PUSHOVER_TOKEN \
--data-file=-
```

List versions:

```bash
gcloud secrets versions list PUSHOVER_TOKEN
```

Read latest value:

```bash
gcloud secrets versions access latest \
--secret=PUSHOVER_TOKEN
```

---

# 6. Grant Secret Access

List service accounts:

```bash
gcloud iam service-accounts list
```

Grant access:

```bash
gcloud projects add-iam-policy-binding gen-lang-client-0946793200 \
--member="serviceAccount:89072472602-compute@developer.gserviceaccount.com" \
--role="roles/secretmanager.secretAccessor"
```

---

# 7. Project Structure

```
project/

├── app.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── README.md
└── .gitignore
```

---

# 8. Gradio Application

Cloud Run requires Gradio to bind to port 8080.

```python
import os

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 8080))
)
```

Without this Cloud Run will fail its health check.

---

# 9. Install Dependencies

Example:

```bash
uv add gradio
uv add google-genai
uv add requests
```

Sync:

```bash
uv sync
```

---

# 10. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY . .

EXPOSE 8080

CMD ["uv", "run", "python", "app.py"]
```

---

# 11. Deploy

```bash
gcloud run deploy gemini-gradio-app \
--source . \
--region us-central1 \
--allow-unauthenticated \
--set-secrets \
GOOGLE_API_KEY=GOOGLE_API_KEY:latest,\
GEMINI_API_KEY=GEMINI_API_KEY:latest,\
PUSHOVER_USER=PUSHOVER_USER:latest,\
PUSHOVER_TOKEN=PUSHOVER_TOKEN:latest
```

Cloud Run will

- Build the container
- Upload it
- Deploy it
- Inject secrets
- Return a URL

---

# 12. View Logs

Tail logs:

```bash
gcloud run services logs tail gemini-gradio-app \
--region us-central1
```

Read logs:

```bash
gcloud run logs read gemini-gradio-app \
--region us-central1
```

---

# 13. Update the Application

After code changes:

```bash
gcloud run deploy gemini-gradio-app \
--source . \
--region us-central1 \
--allow-unauthenticated \
--set-secrets \
GOOGLE_API_KEY=GOOGLE_API_KEY:latest,\
GEMINI_API_KEY=GEMINI_API_KEY:latest,\
PUSHOVER_USER=PUSHOVER_USER:latest,\
PUSHOVER_TOKEN=PUSHOVER_TOKEN:latest
```

---

# Troubleshooting Guide

## Build fails

### Error

```
Build failed
```

### Solution

View logs:

```bash
gcloud builds list
```

```bash
gcloud builds log BUILD_ID --region us-central1
```

---

## Python Version Not Found

Example:

```
Failed to download runtime 3.12.12
```

### Fix

Use a supported Python version.

Example:

```
.python-version

3.12
```

or remove `.python-version`.

---

## Container Failed to Start

Example:

```
Container failed to listen on PORT=8080
```

### Fix

Use

```python
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 8080))
)
```

---

## Secret Not Found

Check:

```bash
gcloud secrets list
```

Read:

```bash
gcloud secrets versions access latest \
--secret=SECRET_NAME
```

---

## Secret Updated but Application Still Uses Old Value

Cloud Run may still have running instances.

Redeploy:

```bash
gcloud run deploy gemini-gradio-app \
--source .
```

---

## Verify Environment Variables

```bash
gcloud run services describe gemini-gradio-app \
--region us-central1 \
--format="yaml(spec.template.spec.containers[0].env)"
```

---

## Gemini Works but Pushover Doesn't

Check logs.

If you see:

```
application token is invalid
```

The Pushover Application Token is incorrect.

This is **NOT** your User Key.

Correct values:

```
PUSHOVER_USER
→ User Key

PUSHOVER_TOKEN
→ Application API Token
```

---

## Verify Pushover

Log the response:

```python
response = requests.post(...)

print(response.status_code)
print(response.text)
```

Successful response:

```json
{
    "status": 1
}
```

---

## Common Pushover Errors

### Invalid application token

```
application token is invalid
```

Fix:

Update `PUSHOVER_TOKEN`.

---

### Invalid user

```
user identifier is invalid
```

Fix:

Update `PUSHOVER_USER`.

---

## Docker Issues

Verify Dockerfile exists:

```bash
ls Dockerfile
```

Build locally:

```bash
docker build -t gemini-gradio-app .
```

Run:

```bash
docker run -p 8080:8080 gemini-gradio-app
```

---

## View Cloud Run URL

```bash
gcloud run services describe gemini-gradio-app \
--region us-central1 \
--format="value(status.url)"
```

---

# Cost Optimisation

Limit instances:

```bash
gcloud run services update gemini-gradio-app \
--max-instances=1
```

Create Billing Budget:

```
Billing
    ↓
Budgets & Alerts
```

Recommended:

- £5 Budget
- 50% Alert
- 90% Alert
- 100% Alert

---

# Security Best Practices

✅ Store all API keys in Secret Manager.

✅ Never commit secrets to Git.

✅ Add `.env` to `.gitignore`.

✅ Use Cloud Run secrets instead of environment variables stored in code.

✅ Consider enabling Gradio authentication if the application is public.

---

# Useful Commands

Current project

```bash
gcloud config get-value project
```

List secrets

```bash
gcloud secrets list
```

Read a secret

```bash
gcloud secrets versions access latest --secret=SECRET_NAME
```

List Cloud Run services

```bash
gcloud run services list
```

Tail logs

```bash
gcloud run services logs tail gemini-gradio-app \
--region us-central1
```

Deploy

```bash
gcloud run deploy gemini-gradio-app \
--source .
```

---

# Deployment Checklist

- [ ] Billing enabled
- [ ] gcloud installed
- [ ] Logged into Google Cloud
- [ ] Project selected
- [ ] Required APIs enabled
- [ ] Secrets created
- [ ] Secret Manager permissions granted
- [ ] `demo.launch()` configured for Cloud Run
- [ ] Dependencies installed
- [ ] Dockerfile present (if using Docker)
- [ ] Application deployed
- [ ] Logs verified
- [ ] Gemini API working
- [ ] Pushover notifications working
- [ ] Budget alerts configured

---

Happy Deploying! 🚀