# WalletGenie Cloud Run Deployment Guide

## Prerequisites
✅ You have authenticated: `gcloud auth application-default login`
✅ GCS Bucket verified: `walletgenie`
✅ Project: `walletgenie-479217`

## Step 1: Enable Required APIs
```bash
gcloud services enable run.googleapis.com \
  sqladmin.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com
```

## Step 2: Create Cloud SQL Instance (Optional)
If you want to use Cloud SQL instead of SQLite:

```bash
# Create Cloud SQL instance
gcloud sql instances create walletgenie-db \
  --database-version=POSTGRES_15 \
  --cpu=1 \
  --memory=3840Mi \
  --region=us-central1 \
  --root-password=<CHOOSE_SECURE_PASSWORD>

# Create database
gcloud sql databases create walletgenie --instance=walletgenie-db

# Get connection name (you'll need this)
gcloud sql instances describe walletgenie-db --format="value(connectionName)"
```

## Step 3: Build Frontend
```bash
cd frontend
npx ng build --configuration production
cd ..
```

## Step 4: Deploy to Cloud Run
```bash
# Set your variables
PROJECT_ID="walletgenie-479217"
SERVICE_NAME="walletgenie"
REGION="us-central1"
BUCKET_NAME="walletgenie"

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --set-env-vars GCS_BUCKET=$BUCKET_NAME \
  --set-env-vars GEMINI_API_KEY="<YOUR_GEMINI_API_KEY>"

# If using Cloud SQL, add these env vars:
# --set-env-vars SQL_CONNECTION="<INSTANCE_CONNECTION_NAME>" \
# --set-env-vars DB_USER="postgres" \
# --set-env-vars DB_PASS="<YOUR_PASSWORD>" \
# --set-env-vars DB_NAME="walletgenie"
```

## Step 5: Access Your App
After deployment completes, you'll get a URL like:
```
https://walletgenie-XXXXX-uc.a.run.app
```

## Notes
- **For hackathon/demo**: You can skip Cloud SQL and use SQLite (data won't persist between deployments)
- **Storage**: Files uploaded will be stored in the `walletgenie` GCS bucket
- **Cost**: With minimal traffic, this should cost <$5/month
