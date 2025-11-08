# PDF to Text Chunker

<div align="center">
  <img src="logo.png" alt="PDF to Text Chunker Logo" width="400"/>
  
  **Convert PDF files into email-friendly text chunks**
  
  [![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3-orange)](https://aws.amazon.com/)
  [![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
  
  [Live Demo](https://my-pdf-chunker-website.s3.us-east-2.amazonaws.com/pdf-chunker.html) • [Setup Guide](SETUP.md) • [Documentation](PROJECT_SUMMARY.md)
</div>

---

## 🎯 Overview

A serverless application that converts PDF files into text chunks of 20,000 characters each, perfect for sharing via email or other platforms with character limits. Built with AWS Lambda and S3, designed to stay within the free tier permanently.

**Why this exists:** Email clients and many platforms have character limits. This tool breaks down long PDF transcripts (like podcasts) into manageable chunks that fit those limits while preserving formatting and readability.

---

## ✨ Features

- 📄 **PDF Processing** - Extract text from PDF files with preserved formatting
- ✂️ **Smart Chunking** - Split text at paragraph boundaries (20,000 characters per chunk)
- 🌐 **Web Interface** - Drag-and-drop upload with instant processing
- 🔄 **S3 Trigger Support** - Automated processing for files uploaded to S3
- 📋 **Copy to Clipboard** - One-click copying of text chunks
- 💾 **Download Support** - Save chunks as .txt files
- 🛡️ **Rate Limiting** - Built-in protection (10 PDFs/hour per IP)
- 💰 **Cost Optimized** - Designed to stay $0/month on AWS free tier
- 🎨 **Professional Branding** - Custom logo with optimized image delivery

---

## 🏗️ Architecture

```
User Upload → Lambda Function URL → PyPDF2 Processing
     ↓
Text Extraction → Smart Chunking → JSON Response
     ↓
Web Interface → Copy/Download
```

**Alternative S3 Flow:**
```
S3 Upload → Event Trigger → Lambda Processing → Output to S3
```

**Key Design Decisions:**
- **Serverless (Lambda)** - No server management, auto-scaling, pay-per-use
- **Lambda Function URLs** - Simpler than API Gateway, free, built-in CORS
- **S3 Static Hosting** - Free, simple, no server needed
- **Bucket Policies** - Modern AWS security (not ACLs)
- **PyPDF2** - Popular, simple, handles text extraction well
- **20k chunks** - Fits email limits, large enough to be useful

---

## 🚀 Quick Start

### Using the Web Interface

1. Visit the [live site](https://my-pdf-chunker-website.s3.us-east-2.amazonaws.com/pdf-chunker.html)
2. Drag and drop your PDF file (max 6MB)
3. Wait for processing (usually 2-5 seconds)
4. Copy chunks to clipboard or download as .txt files

### Using S3 Direct Upload

1. Upload PDF to: `s3://my-pdf-input-bucket-dave/`
2. Lambda automatically processes the file
3. Download chunks from: `s3://my-pdf-output-bucket-dave/`

---

## 📦 Tech Stack

- **Backend:** AWS Lambda (Python 3.13)
- **Storage:** AWS S3
- **PDF Library:** PyPDF2
- **Frontend:** Vanilla JavaScript + HTML/CSS
- **Deployment:** AWS CLI + Bash Scripts
- **Image Optimization:** WEBP with PNG fallback

---

## 🛠️ Installation & Deployment

See **[SETUP.md](SETUP.md)** for complete step-by-step instructions including:

- AWS account setup
- IAM user creation
- AWS CLI installation (macOS, Linux, Windows)
- Lambda function configuration
- S3 bucket creation and policies
- Lambda Layer setup (PyPDF2)
- Deployment automation
- Testing procedures
- Troubleshooting

**Quick Deploy (if already configured):**

```bash
# Clone the repository
git clone https://github.com/dave-schmidt-dev/pdf-chunker.git
cd pdf-chunker

# Configure AWS CLI (one-time setup)
aws configure

# Deploy everything
./deploy.sh
```

**Deploy Options:**
```bash
./deploy.sh          # Deploy everything (Lambda + Website)
./deploy.sh lambda   # Deploy only Lambda function
./deploy.sh website  # Deploy only HTML/CSS/JS to S3
```

---

## 📊 AWS Resources

**Lambda Function:**
- Name: `PDFToTextChunker`
- Runtime: Python 3.13
- Memory: 128 MB
- Timeout: 60 seconds
- Layer: PyPDF2

**S3 Buckets:**
- `my-pdf-input-bucket-dave` - Input PDFs (S3 trigger)
- `my-pdf-output-bucket-dave` - Output text chunks
- `my-pdf-chunker-website` - Static website hosting

**Region:** us-east-2 (Ohio)

**IAM:** Lambda execution role with S3 access and CloudWatch Logs

---

## 💡 How It Works

### Web Upload Flow:

1. **Upload** - User drags PDF to web interface
2. **Encode** - JavaScript converts PDF to Base64
3. **Send** - POST request to Lambda Function URL
4. **Process** - Lambda extracts text with PyPDF2
5. **Clean** - Text formatting improved (paragraphs, speakers)
6. **Chunk** - Split into 20k character segments at paragraph boundaries
7. **Return** - JSON response with chunks and metadata
8. **Display** - User copies or downloads chunks

### S3 Trigger Flow:

1. **Upload** - PDF uploaded to S3 input bucket
2. **Trigger** - S3 event automatically invokes Lambda
3. **Process** - Lambda extracts and chunks text
4. **Save** - Chunks saved as .txt files to output bucket
5. **Download** - User retrieves chunks from S3

---

## 📈 Usage & Costs

### Typical Monthly Usage:
- Lambda requests: ~12/month
- S3 storage: ~5MB
- CloudWatch logs: ~1MB
- **Total cost: $0.00** (within free tier)

### AWS Free Tier Limits:
- **Lambda:** 1M requests/month + 400,000 GB-seconds compute
- **S3:** 5GB storage + 20,000 GET requests + 2,000 PUT requests
- **Data Transfer:** 1GB/month outbound
- **CloudWatch:** 5GB logs ingestion + 5GB archive

### Cost Protection:
- Rate limiting (10 PDFs/hour per IP)
- CloudWatch billing alarm at $5
- Lambda concurrency limit: 10
- Designed for minimal usage

---

## 🔒 Security

**Current Implementation:**
- IP-based rate limiting (10 requests/hour)
- In-memory rate limiting (resets on cold starts)
- Public access (no authentication)
- Modern bucket policies (not ACLs)
- No persistent user data storage
- CloudWatch logging for monitoring

**Production Considerations:**
- Add AWS Cognito for authentication
- Implement DynamoDB for persistent rate limiting
- Add input sanitization for malicious PDFs
- Enable HTTPS-only access
- Consider API Gateway for advanced rate limiting
- File encryption for sensitive documents

---

## 📝 Known Limitations

- **File Size:** 6MB maximum (Lambda Function URL payload limit)
- **OCR:** Cannot extract text from scanned PDFs (images)
- **Formatting:** Some complex PDF formatting may not preserve perfectly
- **Rate Limiting:** In-memory only, resets on Lambda cold starts
- **Authentication:** None (public access)
- **Storage:** No persistent storage (no database)

**Future Enhancements:** See [FUTURE_IMPROVEMENTS.md](FUTURE_IMPROVEMENTS.md) for roadmap

---

## 🎓 What I Learned

**AWS Skills:**
- Lambda function creation and configuration
- Lambda layers for dependencies
- Lambda Function URLs
- S3 static website hosting
- S3 event triggers
- IAM roles and permissions
- CloudWatch monitoring and logs
- Billing alarms
- AWS CLI automation
- Modern S3 bucket policies

**Development Skills:**
- Serverless architecture patterns
- Base64 encoding for binary data
- CORS configuration
- Rate limiting strategies
- Text processing algorithms
- Git version control (GitHub)
- Technical documentation
- Deployment automation with bash
- Image optimization (WEBP)
- Progressive enhancement

**Problem Solving:**
- Debugged PyPDF2 layer structure issues
- Fixed CORS double-header issue
- Resolved base64 double-encoding
- Implemented rate limiting without database
- Migrated from GitLab to GitHub
- Automated deployment workflows
- Migrated from ACLs to bucket policies (AWS security changes)
- Resolved PNG transparency issues
- Optimized images for web performance

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
- Bug fixes
- Documentation improvements
- Feature suggestions (via Issues)
- Code reviews
- Testing on different platforms

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

This project is free and open source. You can use, modify, and distribute it as you wish.

---

## 🙏 Acknowledgments

Built with assistance from Claude (Anthropic) for:
- Architecture design
- Troubleshooting
- Deployment automation
- Documentation
- Branding optimization

Special thanks to the open source community for:
- PyPDF2 library
- AWS documentation
- Markdown best practices

---

## 📞 Contact

**Developer:** David Schmidt  
**GitHub:** [@dave-schmidt-dev](https://github.com/dave-schmidt-dev)  
**Purpose:** Personal tool + portfolio project for job hunting  
**Status:** Actively maintained

---

## 📁 Repository Files

Browse all files in this repository:

### 📄 Documentation

- **[README.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/README.md)** - Project overview and quick start
- **[SETUP.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/SETUP.md)** - Complete AWS setup guide (step-by-step)
- **[PROJECT_SUMMARY.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/PROJECT_SUMMARY.md)** - Comprehensive project documentation
- **[PROJECT_FILES.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/PROJECT_FILES.md)** - File-by-file documentation
- **[CHANGELOG.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/CHANGELOG.md)** - Version history and updates
- **[CONTRIBUTING.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/CONTRIBUTING.md)** - Contribution guidelines
- **[LICENSE](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/LICENSE)** - MIT License

### 💻 Source Code

- **[lambda_function.py](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/lambda_function.py)** - AWS Lambda function (Python 3.13)
- **[pdf-chunker.html](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/pdf-chunker.html)** - Web interface (HTML/CSS/JS)
- **[deploy.sh](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/deploy.sh)** - Automated deployment script

### ⚙️ Configuration

- **[requirements.txt](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/requirements.txt)** - Python dependencies
- **[.env.example](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/.env.example)** - Environment variable template
- **[.gitignore](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/.gitignore)** - Git exclusions

### 🎨 Assets

- **[logo.png](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/logo.png)** - Project logo (PNG, 379KB)
- **[logo.webp](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/logo.webp)** - Optimized logo (WEBP, 23KB, 94% smaller)

### 📊 Diagrams

- **[DIAGRAMS.md](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/DIAGRAMS.md)** - Diagram documentation
- **[architecture-diagram.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/architecture-diagram.mermaid)** - System architecture
- **[aws-infrastructure.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/aws-infrastructure.mermaid)** - AWS resources layout
- **[code-logic.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/code-logic.mermaid)** - Processing logic flow
- **[cost-breakdown.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/cost-breakdown.mermaid)** - Cost analysis
- **[data-flow.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/data-flow.mermaid)** - Data flow diagram
- **[user-workflow.mermaid](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/user-workflow.mermaid)** - User interaction flow
- **[project-illustration.svg](https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/Diagrams/project-illustration.svg)** - Project illustration

---

<div align="center">
  
**Built for Portfolio Demonstration**  
AWS Serverless Architecture • Free Tier Optimized • Job Hunting Ready
  
⭐ Star this repo if you find it useful!

</div>
