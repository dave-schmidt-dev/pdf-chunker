# Project Instructions for AI Assistants

**Last Updated:** November 9, 2025  
**Purpose:** Provide context for AI assistants (Claude, ChatGPT, etc.) working on this project

---

## 📍 Repository Access

**GitHub Repository:** https://github.com/dave-schmidt-dev/pdf-chunker  
**README (raw):** https://raw.githubusercontent.com/dave-schmidt-dev/pdf-chunker/main/README.md

### Workflow for AI Assistants

1. **At conversation start:** Fetch the README above to access all repository files
2. **Repository Files section:** The README contains direct links to all project files
3. **After new files created:** Developer will update README and push, then request re-fetch
4. **For detailed context:** Read this file (PROJECT_INSTRUCTIONS.md) for full project background

---

## 🎯 Project Overview

**What:** Serverless PDF to text chunker  
**Purpose:** Convert PDF files into 20,000-character chunks for email sharing  
**Status:** Fully functional and deployed  
**Cost:** $0/month (AWS free tier optimized)

### Primary Use Case
Processing podcast transcripts and other PDFs to share via email (which has character limits). Built as a personal tool and portfolio piece for job hunting.

---

## 🛠️ Technical Stack

### Backend
- **AWS Lambda:** Python 3.13, PyPDF2 library
- **AWS S3:** Three buckets (input, output, website hosting)
- **CloudWatch:** Logging and billing alarms
- **IAM:** Execution roles with S3 permissions

### Frontend
- **Stack:** Vanilla JavaScript, HTML, CSS
- **Features:** Drag-and-drop upload, Base64 encoding, copy to clipboard
- **Hosting:** S3 static website

### Infrastructure
- **Region:** us-east-2 (Ohio)
- **Deployment:** Automated via bash script (deploy.sh)
- **Security:** Bucket policies (NOT ACLs - modern approach)
- **Rate Limiting:** In-memory, 10 PDFs/hour per IP

### Development
- **Version Control:** Git (GitHub primary)
- **AWS CLI:** Configured with Personal Access Token
- **Testing:** Manual testing, automated deployment verification

---

## 📊 Current State

### ✅ Completed Features
- PDF text extraction with PyPDF2
- Smart chunking at paragraph boundaries (20k chars)
- Web interface with drag-and-drop
- S3 trigger workflow (alternative upload method)
- Copy to clipboard functionality
- Download as .txt files
- Rate limiting (10/hour per IP)
- Professional logo with WEBP optimization (94% size reduction)
- Automated deployment script
- CloudWatch logging
- Billing protection ($5 alarm)
- Comprehensive documentation

### 🎨 Branding
- Modern logo with transparent background
- Blue (PDF) + Purple (cloud) color scheme
- WEBP optimization with PNG fallback
- Responsive design

### 📚 Documentation
- README.md - Overview and quick start
- SETUP.md - AWS setup guide
- PROJECT_SUMMARY.md - Comprehensive documentation
- CHANGELOG.md - Version history
- FUTURE_IMPROVEMENTS.md - Enhancement roadmap (60+ ideas)
- IMPROVEMENTS_INTERVIEW_GUIDE.md - Talking points for interviews

---

## 💻 Development Environment

### Hardware
- M3 MacBook Pro
- 8GB RAM
- 512GB SSD

### Software
- macOS
- AWS CLI (configured)
- Git (HTTPS with Personal Access Token)
- Python 3.13
- Text editor / IDE of choice

### AWS Resources
- Free tier account
- Region: us-east-2
- Lambda function: `PDFToTextChunker`
- S3 buckets: `my-pdf-input-bucket-dave`, `my-pdf-output-bucket-dave`, `my-pdf-chunker-website`

---

## 🔑 Key Development Principles

### Code Quality
1. **Professional standards** - Write portfolio-quality code (job hunting)
2. **Git as source of truth** - Always commit before deploying
3. **Modern best practices** - Use current approaches (bucket policies vs ACLs)
4. **Documentation matters** - Keep all docs current
5. **Readable and extensible** - Future-proof decisions

### Communication Preferences
1. **Explain concepts** - Don't just show solutions, teach the "why"
2. **Discuss options** - Present alternatives and trade-offs
3. **No over-apologizing** - Direct, honest communication
4. **Acknowledge mistakes** - Explain what happened and how to prevent recurrence
5. **Learning mindset** - Help build understanding, not just working code

### Workflow
1. Edit code locally
2. Test locally (if possible)
3. Commit to Git with descriptive message
4. Push to GitHub
5. Deploy to AWS via `./deploy.sh`
6. Test on live site
7. Check CloudWatch logs if issues

---

## 📁 Key Files

### Core Application
- **lambda_function.py** - Lambda processing logic (Python 3.13)
- **pdf-chunker.html** - Web interface (HTML/CSS/JS)
- **deploy.sh** - Automated deployment script (Lambda + S3 website)

### Configuration
- **requirements.txt** - Python dependencies (PyPDF2)
- **.env.example** - Environment variable template
- **.gitignore** - Git exclusions

### Documentation
- **PROJECT_SUMMARY.md** - Most comprehensive doc (current state, decisions, troubleshooting)
- **SETUP.md** - Step-by-step AWS setup guide
- **FUTURE_IMPROVEMENTS.md** - 60+ enhancement ideas organized by category
- **CHANGELOG.md** - Version history with dates
- **PROJECT_FILES.md** - File-by-file documentation
- **CONTRIBUTING.md** - Contribution guidelines

### Assets
- **logo.png** - Logo (PNG, 379KB)
- **logo.webp** - Optimized logo (WEBP, 23KB, 94% smaller)

### Diagrams
All diagrams are in `/diagrams/` directory (Mermaid format + SVG)

---

## 🚀 Deployment Process

### Standard Deployment
```bash
# After making changes
git add .
git commit -m "Descriptive commit message"
git push origin main

# Deploy to AWS
./deploy.sh  # Deploys both Lambda and website
```

### Deployment Script Options
```bash
./deploy.sh          # Deploy everything
./deploy.sh lambda   # Deploy only Lambda function
./deploy.sh website  # Deploy only S3 website
```

### What deploy.sh Does
1. Checks for uncommitted changes (warns if found)
2. Verifies AWS CLI is installed and configured
3. Packages lambda_function.py into deployment.zip
4. Updates Lambda function code via AWS CLI
5. Uploads html/logo files to S3 website bucket
6. Applies bucket policy (NOT ACLs)
7. Shows deployment status and URLs

---

## ⚠️ Important Technical Notes

### AWS-Specific
- **Use bucket policies, NOT ACLs** - Modern S3 security approach (ACLs are legacy)
- **Rate limiting is in-memory** - Resets on Lambda cold starts (acceptable for personal use)
- **Function URL payload limit** - 6MB max file size
- **Free tier optimized** - Designed for ~12 PDFs/month (~$0.00 cost)
- **Lambda timeout** - 60 seconds (sufficient for processing)

### Known Limitations
- No OCR support (scanned PDFs won't work)
- No authentication (public access)
- No persistent storage / database
- In-memory rate limiting (not persistent)
- Complex PDF formatting may not preserve perfectly

### Security Measures
- Rate limiting (10 PDFs/hour per IP)
- CloudWatch billing alarm ($5 threshold)
- Lambda concurrency limit (10 simultaneous executions)
- Input validation
- Error handling

---

## 🎯 Future Direction

### Immediate Priorities (Phase 1)
Quick wins with high impact:
1. Favicon
2. Mobile responsive design
3. Dark mode toggle
4. Better error messages
5. Loading progress indicator

### Near-Term (Phase 2)
Core functionality improvements:
1. Custom chunk size selector
2. Download all as ZIP
3. Processing history (localStorage)
4. Multiple file upload
5. Unit tests

### Long-Term (Phase 3)
Advanced features for portfolio:
1. React migration (component architecture)
2. CI/CD pipeline (GitHub Actions)
3. User authentication (AWS Cognito)
4. Client-side PDF processing (PDF.js)
5. AI integration (summarization)

See **FUTURE_IMPROVEMENTS.md** for complete list (60+ ideas with difficulty ratings and portfolio value assessments).

---

## 🗣️ Interview Talking Points

When discussing this project in job interviews:

### Architecture
- "Serverless design using AWS Lambda and S3"
- "Cost optimization - designed to stay in free tier permanently"
- "Dual upload methods: web UI and automated S3 triggers"

### Skills Demonstrated
- Python (text processing, AWS SDK)
- JavaScript (async/await, File API, Base64 encoding)
- AWS services (Lambda, S3, IAM, CloudWatch)
- Bash scripting (deployment automation)
- Modern web standards (WEBP optimization, progressive enhancement)
- Security best practices (bucket policies, rate limiting)

### Problem Solving
- Adapted to AWS security changes (ACL → bucket policy migration)
- Resolved transparency issues with logo (PNG alpha channel)
- Optimized images for web (94% size reduction with WEBP)
- Built deployment automation to reduce manual errors

### Professional Practices
- Version control (GitHub)
- Comprehensive documentation
- Automated deployment
- Cost awareness
- Portfolio-quality presentation

---

## 📝 Notes for AI Assistants

### When Providing Code
- Explain the "why" behind solutions, not just the "what"
- Point out trade-offs and alternative approaches
- Highlight modern best practices
- Consider future maintainability

### When Suggesting Changes
- Discuss impact on AWS costs
- Consider free tier implications
- Think about job interview talking points
- Balance quick wins vs learning opportunities

### When Troubleshooting
- Check CloudWatch logs (mention this to developer)
- Consider Git history (what changed recently?)
- Verify AWS CLI configuration
- Test deployment script vs manual deployment

### Project Context Awareness
- This is a portfolio project (presentation matters)
- Developer is job hunting (interview value important)
- Focus on professional practices and documentation
- Balance functionality with learning opportunities

---

## 🔄 Maintaining This File

**When to Update:**
- After major feature additions
- When deployment process changes
- After architectural decisions
- When adding new AWS resources
- After updating development workflow

**Who Updates:**
- Primary developer (Dave) after completing milestones
- AI assistants can suggest updates after significant work sessions

**Review Frequency:**
- After completing each phase of improvements
- Before major refactoring efforts
- When onboarding new collaborators
- Quarterly review for accuracy

---

**Version:** 1.0  
**Created:** November 9, 2025  
**Project Status:** Active Development  
**Next Milestone:** Phase 1 Quick Wins (mobile responsive, dark mode, favicon)
