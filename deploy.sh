#!/bin/bash

# Configuration
PROJECT_ID="walletgenie-479217"
SERVICE_NAME="walletgenie"
REGION="us-central1"
DB_INSTANCE_NAME="walletgenie-db"
BUCKET_NAME="walletgenie-bucket-$PROJECT_ID"

echo "Deploying WalletGenie to Cloud Run..."

# 0. Enable APIs (One time setup)
# gcloud services enable run.googleapis.com sqladmin.googleapis.com storage.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 1. Create Resources (If not exist)
# echo "Creating GCS Bucket..."
# gcloud storage buckets create gs://$BUCKET_NAME --location=$REGION || echo "Bucket might already exist"

# echo "Creating Cloud SQL Instance (Postgres)..."
# gcloud sql instances create $DB_INSTANCE_NAME --database-version=POSTGRES_15 --cpu=1 --memory=3840Mi --region=$REGION --root-password=password123 || echo "Instance might already exist"
# gcloud sql databases create walletgenie --instance=$DB_INSTANCE_NAME || echo "DB might already exist"

# 2. Build and Submit Container
echo "Building container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

# 3. Deploy to Cloud Run
# Note: SQL_CONNECTION should be "PROJECT_ID:REGION:INSTANCE_NAME"
# Get the connection name:
# INSTANCE_CONNECTION_NAME=$(gcloud sql instances describe $DB_INSTANCE_NAME --format="value(connectionName)")

echo "Deploying service..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --set-env-vars PROJECT_ID=$PROJECT_ID \
  --set-env-vars GCS_BUCKET=$BUCKET_NAME \
  --set-env-vars SQL_CONNECTION="" \
  --set-env-vars DB_USER="postgres" \
  --set-env-vars DB_PASS=" \
  --set-env-vars DB_NAME="" \
  --set-env-vars GEMINI_API_KEY=""

echo "Deployment complete!"
