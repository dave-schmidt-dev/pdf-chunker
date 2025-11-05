#!/bin/bash
# Deploy/Update Lambda Function
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Deploying PDF Chunker Lambda Function..."

# Configuration
FUNCTION_NAME="PDFToTextChunker"
REGION="us-east-2"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    echo "Install: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if function file exists
if [ ! -f "lambda_function.py" ]; then
    echo -e "${RED}❌ lambda_function.py not found!${NC}"
    exit 1
fi

echo "📦 Creating deployment package..."
zip -q deployment.zip lambda_function.py

echo "☁️  Uploading to AWS Lambda..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://deployment.zip \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo "Function: $FUNCTION_NAME"
    echo "Region: $REGION"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi

# Cleanup
rm deployment.zip
echo "🧹 Cleaned up temporary files"

echo -e "${GREEN}✨ Done!${NC}"
