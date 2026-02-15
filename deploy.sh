#!/bin/bash
# Deploy Asclepius Backend to Google Cloud Run
# This script deploys the fixed backend code

set -e

echo "=================================="
echo "Deploying Asclepius Backend"
echo "=================================="

# Set your GCP project ID
PROJECT_ID="asclepius-300388107814"
REGION="asia-south1"
SERVICE_NAME="asclepius-backend"

echo "🚀 Starting deployment..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Navigate to backend directory
cd backend

# Build and deploy to Cloud Run
echo "📦 Building and deploying..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --project $PROJECT_ID \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=sqlite+aiosqlite:///./dev_db.sqlite \
  --timeout 3600 \
  --memory 2Gi \
  --cpu 2 \
  --port 8000

echo ""
echo "✅ Deployment complete!"
echo "Your backend is now live at:"
echo "https://$SERVICE_NAME-$REGION-run.app"
echo ""
echo "Test with: curl https://$SERVICE_NAME-$REGION-run.app/health"

