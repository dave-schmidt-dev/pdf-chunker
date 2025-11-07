#!/bin/bash

# deploy.sh - Automated deployment script for PDF Chunker
# Usage: ./deploy.sh [lambda|website|all]
# - lambda: Deploy only Lambda function
# - website: Deploy only website files
# - all or no argument: Deploy everything

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LAMBDA_FUNCTION="PDFToTextChunker"
WEBSITE_BUCKET="my-pdf-chunker-website"
REGION="us-east-2"

# Determine what to deploy
DEPLOY_MODE="${1:-all}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  PDF Chunker Deployment Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check for uncommitted changes
if [[ $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo -e "${YELLOW}   Consider committing before deploying${NC}"
    echo ""
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ Error: AWS CLI is not installed${NC}"
    echo -e "${YELLOW}   Install it from: https://aws.amazon.com/cli/${NC}"
    exit 1
fi

# Verify AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ Error: AWS credentials not configured${NC}"
    echo -e "${YELLOW}   Run: aws configure${NC}"
    exit 1
fi

echo -e "${GREEN}✓ AWS CLI configured${NC}"
echo ""

# Function to deploy Lambda
deploy_lambda() {
    echo -e "${BLUE}Deploying Lambda function...${NC}"
    
    # Check if lambda_function.py exists
    if [ ! -f "lambda_function.py" ]; then
        echo -e "${RED}❌ Error: lambda_function.py not found${NC}"
        echo -e "${YELLOW}   Make sure you're in the project root directory${NC}"
        exit 1
    fi
    
    # Create deployment package
    echo "📦 Creating deployment package..."
    zip -q deployment.zip lambda_function.py
    
    # Upload to Lambda
    echo "⬆️  Uploading to Lambda..."
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION \
        --zip-file fileb://deployment.zip \
        --region $REGION \
        > /dev/null
    
    # Clean up
    rm deployment.zip
    
    echo -e "${GREEN}✅ Lambda function deployed successfully!${NC}"
    echo ""
}

# Function to deploy website
deploy_website() {
    echo -e "${BLUE}Deploying website files...${NC}"
    
    # Check if files exist
    if [ ! -f "pdf-chunker.html" ]; then
        echo -e "${RED}❌ Error: pdf-chunker.html not found${NC}"
        exit 1
    fi
    
    # Upload HTML file
    echo "⬆️  Uploading pdf-chunker.html..."
    aws s3 cp pdf-chunker.html s3://$WEBSITE_BUCKET/ \
        --region $REGION \
        --quiet
    
    # Upload logo files if they exist
    if [ -f "logo.png" ]; then
        echo "⬆️  Uploading logo.png..."
        aws s3 cp logo.png s3://$WEBSITE_BUCKET/ \
            --region $REGION \
            --quiet
    fi
    
    if [ -f "logo.webp" ]; then
        echo "⬆️  Uploading logo.webp..."
        aws s3 cp logo.webp s3://$WEBSITE_BUCKET/ \
            --region $REGION \
            --quiet
    fi
    
    # Set bucket policy for public access (replaces ACLs)
    echo "🔐 Setting bucket policy for public access..."
    
    # Create temporary policy file
    cat > /tmp/bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$WEBSITE_BUCKET/*"
    }
  ]
}
EOF
    
    # Apply bucket policy
    aws s3api put-bucket-policy \
        --bucket $WEBSITE_BUCKET \
        --policy file:///tmp/bucket-policy.json \
        --region $REGION \
        2>/dev/null || echo -e "${YELLOW}   Note: Bucket policy already set or unable to update${NC}"
    
    # Clean up
    rm /tmp/bucket-policy.json
    
    echo -e "${GREEN}✅ Website deployed successfully!${NC}"
    echo -e "${GREEN}🌐 URL: https://$WEBSITE_BUCKET.s3.$REGION.amazonaws.com/pdf-chunker.html${NC}"
    echo ""
}

# Deploy based on mode
case $DEPLOY_MODE in
    lambda)
        deploy_lambda
        ;;
    website)
        deploy_website
        ;;
    all)
        deploy_lambda
        deploy_website
        ;;
    *)
        echo -e "${RED}❌ Error: Invalid argument '$DEPLOY_MODE'${NC}"
        echo -e "${YELLOW}Usage: ./deploy.sh [lambda|website|all]${NC}"
        exit 1
        ;;
esac

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  • Test Lambda: Upload a PDF via the website"
echo "  • Check CloudWatch logs if there are issues"
echo "  • View website: https://$WEBSITE_BUCKET.s3.$REGION.amazonaws.com/pdf-chunker.html"
echo ""
