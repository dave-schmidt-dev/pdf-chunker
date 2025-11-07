#!/bin/bash
# Complete Deployment Script for PDF Chunker Project
# Deploys both Lambda function and HTML website
# Usage: ./deploy.sh [lambda|website|all]

set -e  # Exit on error

# Configuration
FUNCTION_NAME="PDFToTextChunker"
REGION="us-east-2"
S3_WEBSITE_BUCKET="my-pdf-chunker-website"
HTML_FILE="pdf-chunker.html"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default to deploying everything
DEPLOY_TARGET="${1:-all}"

# Functions
deploy_lambda() {
    echo -e "${BLUE}📦 Deploying Lambda Function...${NC}"
    
    # Check if function file exists
    if [ ! -f "lambda_function.py" ]; then
        echo -e "${RED}❌ lambda_function.py not found!${NC}"
        return 1
    fi
    
    echo "  → Creating deployment package..."
    zip -q deployment.zip lambda_function.py
    
    echo "  → Uploading to AWS Lambda..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://deployment.zip \
        --region $REGION > /dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ Lambda deployed successfully!${NC}"
    else
        echo -e "${RED}  ❌ Lambda deployment failed!${NC}"
        return 1
    fi
    
    # Cleanup
    rm deployment.zip
}

deploy_website() {
    echo -e "${BLUE}🌐 Deploying Website...${NC}"
    
    # Check if HTML file exists
    if [ ! -f "$HTML_FILE" ]; then
        echo -e "${RED}❌ $HTML_FILE not found!${NC}"
        return 1
    fi
    
    echo "  → Uploading to S3..."
    aws s3 cp $HTML_FILE s3://$S3_WEBSITE_BUCKET/ \
        --region $REGION > /dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ Website deployed successfully!${NC}"
        echo -e "  🔗 URL: https://$S3_WEBSITE_BUCKET.s3.$REGION.amazonaws.com/$HTML_FILE"
    else
        echo -e "${RED}  ❌ Website deployment failed!${NC}"
        return 1
    fi
}

show_status() {
    echo ""
    echo -e "${BLUE}📊 Deployment Status:${NC}"
    echo "  Function: $FUNCTION_NAME"
    echo "  Region: $REGION"
    echo "  Website: https://$S3_WEBSITE_BUCKET.s3.$REGION.amazonaws.com/$HTML_FILE"
}

# Main deployment logic
echo -e "${YELLOW}🚀 PDF Chunker Deployment Tool${NC}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
    echo "Install: https://aws.amazon.com/cli/"
    exit 1
fi

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes!${NC}"
    echo "Consider committing to Git first:"
    echo "  git add ."
    echo "  git commit -m 'Your message'"
    echo "  git push origin main"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Deploy based on target
case $DEPLOY_TARGET in
    lambda)
        deploy_lambda
        ;;
    website)
        deploy_website
        ;;
    all)
        deploy_lambda
        echo ""
        deploy_website
        ;;
    *)
        echo -e "${RED}❌ Invalid target: $DEPLOY_TARGET${NC}"
        echo "Usage: $0 [lambda|website|all]"
        exit 1
        ;;
esac

show_status
echo ""
echo -e "${GREEN}✨ Deployment complete!${NC}"
