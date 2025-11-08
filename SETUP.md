# PDF to Text Chunker - Setup Guide

This guide will walk you through setting up the PDF to Text Chunker application from scratch on AWS.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [AWS Account Setup](#aws-account-setup)
3. [AWS CLI Installation](#aws-cli-installation)
4. [Creating AWS Resources](#creating-aws-resources)
5. [Lambda Layer Setup](#lambda-layer-setup)
6. [Deployment](#deployment)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have:

- **AWS Account** (free tier is sufficient)
- **Git** installed on your machine
- **Python 3.13** installed (or Python 3.11+)
- **pip** (Python package manager)
- **zip** utility (for creating deployment packages)
- **Terminal/Command Line** access
- **Text editor** or IDE

**Cost:** This project is designed to stay within AWS free tier. Expected cost: $0/month for typical usage.

---

## AWS Account Setup

### 1. Create an AWS Account

If you don't have one already:

1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the registration process
4. You'll need a credit card (for verification, but free tier won't charge you)

### 2. Create an IAM User (Recommended)

**Why?** It's best practice not to use your root AWS account for day-to-day operations.

1. Sign in to [AWS Console](https://console.aws.amazon.com)
2. Go to **IAM** (Identity and Access Management)
3. Click **Users** → **Add users**
4. Username: `pdf-chunker-admin` (or your choice)
5. Check **"Provide user access to the AWS Management Console"**
6. Click **Next**
7. Choose **"Attach policies directly"**
8. Search for and select these policies:
   - `AmazonS3FullAccess`
   - `AWSLambda_FullAccess`
   - `IAMFullAccess`
   - `CloudWatchLogsFullAccess`
9. Click **Next** → **Create user**

### 3. Create Access Keys

For AWS CLI access:

1. Go to **IAM** → **Users** → Click your username
2. Go to **Security credentials** tab
3. Scroll to **Access keys** → Click **Create access key**
4. Select **"Command Line Interface (CLI)"**
5. Check the confirmation box → Click **Next**
6. Add description: "PDF Chunker CLI Access"
7. Click **Create access key**
8. **IMPORTANT:** Download the CSV file or copy both:
   - Access Key ID
   - Secret Access Key
   
   ⚠️ **You won't be able to see the Secret Access Key again!**

---

## AWS CLI Installation

### macOS

**Option 1: Official Installer (Recommended)**

```bash
# Download the installer
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"

# Install
sudo installer -pkg AWSCLIV2.pkg -target /

# Verify installation
aws --version
```

**Option 2: Homebrew**

```bash
brew install awscli
aws --version
```

### Linux

```bash
# Download and install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify
aws --version
```

### Windows

1. Download: [AWS CLI MSI Installer](https://awscli.amazonaws.com/AWSCLIV2.msi)
2. Run the installer
3. Verify in Command Prompt: `aws --version`

### Configure AWS CLI

After installation:

```bash
aws configure
```

You'll be prompted for:

```
AWS Access Key ID: [paste your Access Key ID]
AWS Secret Access Key: [paste your Secret Access Key]
Default region name: us-east-2
Default output format: json
```

**Region:** Use `us-east-2` (Ohio) to match the project configuration, or choose a region closer to you.

**Verify configuration:**

```bash
# Test AWS CLI
aws sts get-caller-identity

# You should see output with your AWS account info
```

---

## Creating AWS Resources

### 1. Clone the Repository

```bash
git clone https://github.com/dave-schmidt-dev/pdf-chunker.git
cd pdf-chunker
```

### 2. Create S3 Buckets

You need three S3 buckets. **Bucket names must be globally unique**, so add your initials or a random string.

```bash
# Input bucket (for S3 trigger workflow)
aws s3 mb s3://my-pdf-input-bucket-dave --region us-east-2

# Output bucket (for processed chunks from S3 workflow)
aws s3 mb s3://my-pdf-output-bucket-dave --region us-east-2

# Website bucket (for hosting the HTML interface)
aws s3 mb s3://my-pdf-chunker-website --region us-east-2
```

**Note:** Replace `dave` with your own identifier if these bucket names are taken.

### 3. Configure S3 Website Hosting

Enable static website hosting on the website bucket:

```bash
aws s3 website s3://my-pdf-chunker-website \
  --index-document pdf-chunker.html \
  --region us-east-2
```

### 4. Set Bucket Policy (Public Read)

The website bucket needs to allow public read access:

```bash
aws s3api put-bucket-policy \
  --bucket my-pdf-chunker-website \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-pdf-chunker-website/*"
    }]
  }' \
  --region us-east-2
```

### 5. Create IAM Role for Lambda

Lambda needs permissions to access S3 and CloudWatch Logs.

**Create Trust Policy:**

```bash
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "lambda.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }]
}
EOF
```

**Create the Role:**

```bash
aws iam create-role \
  --role-name PDFChunkerLambdaRole \
  --assume-role-policy-document file://trust-policy.json \
  --region us-east-2
```

**Attach Policies:**

```bash
# S3 access
aws iam attach-role-policy \
  --role-name PDFChunkerLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# CloudWatch Logs access
aws iam attach-role-policy \
  --role-name PDFChunkerLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
```

**Get the Role ARN (you'll need this next):**

```bash
aws iam get-role --role-name PDFChunkerLambdaRole --query 'Role.Arn' --output text
```

Copy this ARN - it looks like: `arn:aws:iam::123456789012:role/PDFChunkerLambdaRole`

### 6. Create Lambda Function

**Create the function:**

```bash
# First, create a temporary deployment package
zip deployment.zip lambda_function.py

# Create the Lambda function (replace YOUR_ROLE_ARN with the ARN from previous step)
aws lambda create-function \
  --function-name PDFToTextChunker \
  --runtime python3.13 \
  --role YOUR_ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://deployment.zip \
  --timeout 60 \
  --memory-size 128 \
  --region us-east-2

# Clean up temporary file
rm deployment.zip
```

### 7. Create Lambda Function URL

This enables direct HTTPS access to your Lambda function:

```bash
aws lambda create-function-url-config \
  --function-name PDFToTextChunker \
  --auth-type NONE \
  --cors '{
    "AllowOrigins": ["*"],
    "AllowMethods": ["POST", "OPTIONS"],
    "AllowHeaders": ["Content-Type"],
    "MaxAge": 86400
  }' \
  --region us-east-2
```

**Save the Function URL** that's returned - you'll need to add it to your HTML file.

### 8. Configure S3 Trigger

Set up Lambda to automatically process PDFs uploaded to the input bucket:

**Grant S3 permission to invoke Lambda:**

```bash
aws lambda add-permission \
  --function-name PDFToTextChunker \
  --statement-id s3-trigger-permission \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::my-pdf-input-bucket-dave \
  --region us-east-2
```

**Create S3 notification configuration:**

```bash
cat > s3-notification.json << 'EOF'
{
  "LambdaFunctionConfigurations": [{
    "LambdaFunctionArn": "YOUR_LAMBDA_ARN",
    "Events": ["s3:ObjectCreated:*"],
    "Filter": {
      "Key": {
        "FilterRules": [{
          "Name": "suffix",
          "Value": ".pdf"
        }]
      }
    }
  }]
}
EOF
```

**Get your Lambda ARN:**

```bash
aws lambda get-function --function-name PDFToTextChunker --query 'Configuration.FunctionArn' --output text --region us-east-2
```

Replace `YOUR_LAMBDA_ARN` in `s3-notification.json` with this ARN, then apply:

```bash
aws s3api put-bucket-notification-configuration \
  --bucket my-pdf-input-bucket-dave \
  --notification-configuration file://s3-notification.json \
  --region us-east-2
```

### 9. Set Up CloudWatch Billing Alarm (Optional but Recommended)

Protect yourself from unexpected charges:

```bash
# Enable billing alerts (one-time setup)
aws ce put-cost-anomaly-monitor \
  --anomaly-monitor Name=PDFChunkerMonitor,MonitorType=DIMENSIONAL,MonitorDimension=SERVICE

# Create SNS topic for alerts
aws sns create-topic --name BillingAlerts --region us-east-1

# Subscribe your email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:BillingAlerts \
  --protocol email \
  --notification-endpoint your-email@example.com \
  --region us-east-1
```

(Check your email and confirm the subscription)

---

## Lambda Layer Setup

Lambda needs the PyPDF2 library. We'll create a Lambda Layer for this.

### 1. Create Layer Directory Structure

```bash
mkdir -p lambda-layer/python/lib/python3.13/site-packages
```

### 2. Install PyPDF2

```bash
pip3 install PyPDF2 -t lambda-layer/python/lib/python3.13/site-packages/
```

### 3. Create Layer Zip File

```bash
cd lambda-layer
zip -r pypdf2-layer.zip python
cd ..
```

### 4. Create Lambda Layer

```bash
aws lambda publish-layer-version \
  --layer-name PyPDF2-Layer \
  --zip-file fileb://lambda-layer/pypdf2-layer.zip \
  --compatible-runtimes python3.13 \
  --region us-east-2
```

**Save the LayerVersionArn** from the output.

### 5. Attach Layer to Function

```bash
aws lambda update-function-configuration \
  --function-name PDFToTextChunker \
  --layers YOUR_LAYER_VERSION_ARN \
  --region us-east-2
```

Replace `YOUR_LAYER_VERSION_ARN` with the ARN from the previous step.

### 6. Clean Up

```bash
rm -rf lambda-layer
```

---

## Deployment

Now that everything is set up, you can use the automated deployment script for future updates.

### 1. Update Configuration

**Edit `pdf-chunker.html`:**

Find this line (around line 172):

```javascript
const response = await fetch('YOUR_LAMBDA_FUNCTION_URL', {
```

Replace `YOUR_LAMBDA_FUNCTION_URL` with your actual Lambda Function URL.

**Verify `lambda_function.py` configuration:**

Check that the output bucket name matches (around line 130):

```python
bucket_name = 'my-pdf-output-bucket-dave'
```

Update if you used a different bucket name.

### 2. Make Deploy Script Executable

```bash
chmod +x deploy.sh
```

### 3. Deploy Everything

```bash
./deploy.sh
```

This will:
- Check for uncommitted Git changes
- Package and upload Lambda function
- Upload HTML and logo files to S3
- Set the bucket policy
- Display deployment results

**Deploy only Lambda:**

```bash
./deploy.sh lambda
```

**Deploy only website:**

```bash
./deploy.sh website
```

---

## Testing

### 1. Test the Web Interface

1. Open your browser
2. Go to: `https://my-pdf-chunker-website.s3.us-east-2.amazonaws.com/pdf-chunker.html`
3. Drag and drop a PDF file (or click to select)
4. Wait for processing (2-10 seconds depending on file size)
5. You should see text chunks displayed
6. Test "Copy to Clipboard" and "Download" buttons

### 2. Test S3 Trigger Workflow

```bash
# Upload a test PDF to the input bucket
aws s3 cp test.pdf s3://my-pdf-input-bucket-dave/ --region us-east-2

# Wait 5-10 seconds, then check the output bucket
aws s3 ls s3://my-pdf-output-bucket-dave/ --region us-east-2

# You should see chunk_1.txt, chunk_2.txt, etc.

# Download a chunk to verify
aws s3 cp s3://my-pdf-output-bucket-dave/chunk_1.txt . --region us-east-2
cat chunk_1.txt
```

### 3. Check CloudWatch Logs

If something goes wrong:

```bash
# View recent logs
aws logs tail /aws/lambda/PDFToTextChunker --follow --region us-east-2
```

Or go to AWS Console → CloudWatch → Log groups → `/aws/lambda/PDFToTextChunker`

---

## Troubleshooting

### "Access Denied" when accessing website

**Problem:** S3 bucket policy not set correctly.

**Solution:**

```bash
# Reapply bucket policy
aws s3api put-bucket-policy \
  --bucket my-pdf-chunker-website \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-pdf-chunker-website/*"
    }]
  }' \
  --region us-east-2
```

### "No PDF data in request" error

**Problem:** Visiting the Lambda Function URL directly in browser.

**Solution:** Don't visit the Function URL directly. Use the web interface instead.

### Lambda function timing out

**Problem:** Large PDF files take too long to process.

**Solution:** Increase Lambda timeout:

```bash
aws lambda update-function-configuration \
  --function-name PDFToTextChunker \
  --timeout 120 \
  --region us-east-2
```

### PyPDF2 import errors

**Problem:** Lambda layer not attached or incorrect structure.

**Solution:** Verify layer structure. The path must be exactly:
```
python/lib/python3.13/site-packages/PyPDF2/
```

Recreate the layer following the Lambda Layer Setup section.

### Can't push to GitHub

**Problem:** Authentication failing.

**Solution:** Use Personal Access Token (PAT):

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (all checkboxes)
4. Copy the token
5. When pushing, use token as password:
   ```bash
   git push https://github.com/dave-schmidt-dev/pdf-chunker.git main
   ```
   - Username: your GitHub username
   - Password: paste your PAT

### AWS CLI commands fail

**Problem:** Credentials not configured or expired.

**Solution:**

```bash
# Verify credentials
aws sts get-caller-identity

# If that fails, reconfigure
aws configure
```

### Deployment script fails

**Problem:** Various issues.

**Solutions:**

1. Check AWS CLI is installed: `aws --version`
2. Check credentials: `aws configure list`
3. Verify you're in the project directory: `pwd`
4. Check file exists: `ls lambda_function.py`
5. Check script permissions: `ls -l deploy.sh`
6. Make executable if needed: `chmod +x deploy.sh`

### Rate limit errors

**Problem:** Too many requests in short time.

**Solution:** Wait one hour. The rate limit is 10 PDFs per hour per IP address. This resets on Lambda cold starts.

---

## Cost Monitoring

Keep an eye on your AWS usage:

**Via AWS CLI:**

```bash
# Check current month's costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +%Y-%m-01),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --region us-east-1
```

**Via AWS Console:**

1. Go to AWS Console → Billing Dashboard
2. Check "Month-to-date costs"
3. Expected: $0.00 for typical usage

---

## Next Steps

Once everything is working:

1. ✅ Test with various PDF files
2. ✅ Customize chunk size if needed (edit lambda_function.py)
3. ✅ Add custom domain name (optional)
4. ✅ Implement authentication (if making it public)
5. ✅ Explore the [FUTURE_IMPROVEMENTS.md](FUTURE_IMPROVEMENTS.md) for enhancement ideas

---

## Getting Help

**If you encounter issues:**

1. Check CloudWatch Logs for errors
2. Review this troubleshooting section
3. Check the [GitHub Issues](https://github.com/dave-schmidt-dev/pdf-chunker/issues)
4. Create a new issue with:
   - What you were trying to do
   - What error you received
   - Relevant log output
   - Your AWS region

---

## Additional Resources

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)

---

**Last Updated:** November 8, 2025  
**Maintained By:** David Schmidt  
**License:** MIT
