# PDF to Text Chunks - Project Summary

**Last Updated:** November 6, 2025  
**Status:** ✅ Fully Functional  
**Cost:** $0/month (AWS Free Tier)

---

## 🎯 Project Overview

**What it does:** Converts PDF files into email-friendly text chunks (20,000 characters each) with preserved formatting.

**Why it exists:** To process podcast transcripts and other PDFs for sharing via email, which has character limits.

**Primary user:** Just me (David) - personal tool, potential portfolio piece for job hunting

---

## 🏗️ Current Architecture

### AWS Resources (Region: us-east-2)

**Lambda Function:**
- Name: `PDFToTextChunker`
- Runtime: Python 3.13
- Memory: 128 MB
- Timeout: 60 seconds
- Handler: `lambda_function.lambda_handler`
- Function URL: `https://6utxwfiwqyll6dtneyd54vcei40xfkmq.lambda-url.us-east-2.on.aws/`
- Auth: NONE (public)
- CORS: Enabled (POST allowed)

**Lambda Layer:**
- Name: `PyPDF2-Layer`
- Runtime: Python 3.13
- Contents: PyPDF2 library
- Structure: `python/lib/python3.13/site-packages/`

**S3 Buckets:**
1. Input: `my-pdf-input-bucket-dave`
   - Purpose: S3 trigger workflow (alternative upload method)
   - Trigger: Fires Lambda on `.pdf` upload
   
2. Output: `my-pdf-output-bucket-dave`
   - Purpose: Stores text chunks from S3 trigger workflow
   
3. Website: `my-pdf-chunker-website`
   - Purpose: Hosts the HTML web interface
   - Website URL: `https://my-pdf-chunker-website.s3.us-east-2.amazonaws.com/pdf-chunker.html`
   - Static hosting: Enabled
   - Bucket policy: Public read access

**IAM Permissions:**
- Lambda execution role has: `AmazonS3FullAccess`
- Allows Lambda to read/write to all S3 buckets

**Monitoring:**
- CloudWatch Log Group: `/aws/lambda/PDFToTextChunker`
- Retention: Default (indefinite)

---

## 🔧 How It Works

### Two Usage Methods:

#### Method 1: Web Interface (Primary)
1. User visits S3 website URL
2. Drags/drops PDF file
3. JavaScript converts PDF to Base64
4. Sends POST request to Lambda Function URL
5. Lambda processes and returns JSON with text chunks
6. User copies to clipboard or downloads

#### Method 2: S3 Trigger (Alternative)
1. User uploads PDF to input bucket
2. S3 event triggers Lambda automatically
3. Lambda processes and saves chunks to output bucket
4. User downloads from output bucket

### Processing Pipeline:

```
PDF Input (up to 6MB)
  ↓
Rate Limit Check (10 per hour per IP)
  ↓
Base64 Decode
  ↓
PyPDF2 Text Extraction
  ↓
Text Cleaning:
  - Remove extra spaces
  - Add paragraph breaks after sentences
  - Format speaker names
  ↓
Split into 20k Character Chunks (at paragraph boundaries)
  ↓
Output (JSON for web, .txt files for S3)
```

---

## 🔒 Security & Cost Controls

### Rate Limiting:
- **10 PDFs per hour per IP address**
- Implemented in-memory in Lambda function
- Resets on cold starts (not persistent)

### Billing Protection:
- **CloudWatch Billing Alarm:** Set at $5 threshold
- **Lambda Concurrency Limit:** 10 (max 10 simultaneous executions)
- **Designed for free tier:** ~12 PDFs/month typical usage

### Current Usage:
- Lambda requests: ~12/month (0.001% of free tier)
- S3 storage: ~5 MB (0.1% of free tier)
- CloudWatch logs: ~1 MB (0.02% of free tier)
- **Monthly cost: $0.00**

---

## 📁 Git Repository

**Location:** GitLab (private repo)  
**URL:** `https://gitlab.com/[username]/pdf-chunker` (fill in actual URL)

**Remote:** HTTPS (not SSH)  
**Branch:** `main`

### Repository Structure:
```
pdf-chunker/
├── lambda_function.py          # Lambda code
├── pdf-chunker.html            # Web interface
├── README.md                   # Project overview
├── SETUP.md                    # AWS setup instructions
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── PROJECT_SUMMARY.md          # This file
├── requirements.txt            # Python dependencies
├── .env.example                # Config template
├── .gitignore                  # Git exclusions
├── deploy.sh                   # Deployment script
├── diagrams/                   # Visual diagrams
│   ├── architecture-diagram.mermaid
│   ├── user-workflow.mermaid
│   ├── aws-infrastructure.mermaid
│   ├── data-flow.mermaid
│   ├── code-logic.mermaid
│   ├── cost-breakdown.mermaid
│   ├── project-illustration.svg
│   └── DIAGRAMS.md
└── PROJECT_FILES.md            # File documentation
```

---

## 🎨 Features Implemented

✅ **Core Functionality:**
- PDF text extraction
- Smart chunking at paragraph boundaries
- Web upload interface
- S3 trigger support
- Copy to clipboard
- Download as .txt files

✅ **Security:**
- Rate limiting (10/hour per IP)
- Error handling
- Input validation

✅ **UX:**
- Drag and drop upload
- Visual feedback (processing, success, error)
- Preview of chunks
- Character counts displayed

✅ **Infrastructure:**
- Serverless architecture
- Dual trigger support (web + S3)
- CloudWatch logging
- Free tier optimized

---

## 🐛 Known Limitations

1. **File Size:** 6 MB limit (Lambda Function URL payload limit)
2. **OCR:** Cannot extract text from scanned PDFs (images)
3. **Complex Formatting:** Some PDF formatting may not preserve perfectly
4. **Rate Limiting:** In-memory only (resets on cold starts)
5. **Authentication:** None (public access)
6. **Storage:** Not persistent (no database)

---

## 🔑 Key Technical Decisions

### Why Lambda?
- Serverless = no server management
- Pay-per-use (free for our volume)
- Auto-scaling built-in
- Simple deployment

### Why Lambda Function URLs?
- Simpler than API Gateway
- Free (no extra cost)
- Built-in CORS support
- Good enough for personal project

### Why S3 for Website?
- Free static hosting
- Simple setup
- No server needed
- Built-in CDN

### Why PyPDF2?
- Popular, well-maintained
- Simple API
- Handles text extraction well
- Small footprint

### Why 20k Character Chunks?
- Fits email character limits
- Large enough to be useful
- Small enough to read
- Easy to remember/configure

### Why Rate Limiting?
- Prevent abuse
- Protect free tier
- Simple implementation
- Good enough without database

---

## 📝 Configuration Details

### Environment Variables (for reference, not used in Lambda):
```
AWS_REGION=us-east-2
S3_INPUT_BUCKET=my-pdf-input-bucket-dave
S3_OUTPUT_BUCKET=my-pdf-output-bucket-dave
LAMBDA_FUNCTION_NAME=PDFToTextChunker
LAMBDA_FUNCTION_URL=https://6utxwfiwqyll6dtneyd54vcei40xfkmq.lambda-url.us-east-2.on.aws/
MAX_REQUESTS_PER_IP=10
CHUNK_SIZE=20000
MAX_PDF_SIZE_MB=6
```

### Hardcoded in Lambda:
- Output bucket name: `my-pdf-output-bucket-dave` (line ~130 in lambda_function.py)
- Rate limit: `10` (line 11 in lambda_function.py)
- Chunk size: `20000` (multiple locations)

### Hardcoded in HTML:
- Lambda Function URL: Line 172 in pdf-chunker.html

---

## 🚀 Deployment Process

### Lambda Function:
**Option 1: Manual (current method)**
1. Go to Lambda console
2. Paste code into editor
3. Click "Deploy"

**Option 2: Automated (script available)**
```bash
./deploy.sh
```

### HTML Website:
1. Edit `pdf-chunker.html` locally
2. Go to S3 → `my-pdf-chunker-website` bucket
3. Upload file (overwrites existing)

### Layer Updates:
1. Recreate layer locally:
```bash
mkdir -p lambda-layer/python/lib/python3.13/site-packages
pip3 install PyPDF2 -t lambda-layer/python/lib/python3.13/site-packages/
cd lambda-layer
zip -r pypdf2-layer.zip python
```
2. Upload to Lambda Layers
3. Update function to use new layer version

---

## 🔄 Recent Changes

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version:** 1.0.0 (Initial Release)

**Last significant change:** November 5, 2025
- Added rate limiting
- Enabled Lambda Function URL
- Deployed web interface to S3

---

## 📚 Testing Scenarios

### Successful Test:
- ✅ Upload 18-page PDF transcript
- ✅ Receives 3 chunks (20k, 20k, 12k characters)
- ✅ Formatting preserved (paragraphs, speakers)
- ✅ Copy to clipboard works
- ✅ Download works
- ✅ S3 trigger path works independently

### Known Good Test File:
- "844_This_Is_the_Case_of_Henry_Dee.pdf" (18 pages)
- Processes successfully
- Clean text output with proper formatting

---

## 🎯 Future Enhancement Ideas

See full list in main conversation, but top priorities:

**For Portfolio/Interviews:**
1. Mobile responsive design
2. Better error messages
3. Download all as ZIP
4. Add tests

**For Functionality:**
1. Adjustable chunk size
2. Better text formatting options
3. Processing history (localStorage)

**For Learning:**
1. TypeScript version
2. React rebuild
3. CI/CD pipeline

---

## 💡 Talking Points for Interviews

**When discussing this project:**

1. **Architecture:** "Serverless design using AWS Lambda and S3"
2. **Cost Optimization:** "Designed to stay in free tier permanently"
3. **Security:** "Implemented rate limiting to prevent abuse"
4. **UX:** "Clean interface with drag-and-drop, copy to clipboard"
5. **Versatility:** "Supports both web UI and automated S3 triggers"
6. **Documentation:** "Full diagrams, setup guides, and Git repo"

**Technical skills demonstrated:**
- Python, JavaScript, HTML/CSS
- AWS (Lambda, S3, IAM, CloudWatch)
- Serverless architecture
- API design (Function URLs)
- Text processing algorithms
- Git version control
- Technical documentation

---

## 🆘 Troubleshooting Quick Reference

### "No PDF data in request" error when visiting Function URL
- ✅ **This is normal!** Don't visit the Function URL directly in browser
- Use the web interface instead

### "Rate limit exceeded"
- Wait 1 hour, or
- Lambda cold start will reset counter

### Text formatting looks bad
- Some PDFs have complex formatting that doesn't extract cleanly
- Try different PDF, or
- Modify `clean_text()` function for specific needs

### Lambda not triggering from S3
- Check S3 trigger is configured correctly
- Verify file ends in `.pdf` (lowercase)
- Check CloudWatch logs for errors

### Can't push to GitLab
- Using HTTPS remote (not SSH)
- Need Personal Access Token (not password)
- Check: `git remote -v` shows HTTPS URL

---

## 📞 For Future Claude Conversations

**When starting a new conversation, provide:**

1. **This summary document**
2. **Specific goal:** "I want to add feature X" or "Debug issue Y"
3. **Current code files** (if modifying code)

**Claude will need to know:**
- AWS resource names (listed above)
- Current functionality (listed above)
- Git repo structure (listed above)

**Quick context statement:**
```
I have a serverless PDF processing app using AWS Lambda and S3.
It converts PDFs to text chunks for email. Lambda Function URL
for web interface, S3 triggers for automated processing.
Rate limited, free tier optimized. Currently working.
Here's my PROJECT_SUMMARY.md...
```

---

## ✅ Project Status Checklist

**Infrastructure:**
- [x] Lambda function deployed
- [x] PyPDF2 layer attached
- [x] S3 buckets created
- [x] Function URL enabled
- [x] S3 triggers configured
- [x] Website hosted
- [x] IAM permissions set
- [x] CloudWatch logging active
- [x] Billing alarm set

**Code:**
- [x] Lambda function complete
- [x] Web interface complete
- [x] Rate limiting implemented
- [x] Error handling implemented
- [x] Text processing working

**Documentation:**
- [x] README.md
- [x] SETUP.md
- [x] CHANGELOG.md
- [x] PROJECT_FILES.md
- [x] PROJECT_SUMMARY.md (this file)
- [x] DIAGRAMS.md
- [x] LICENSE
- [x] .gitignore

**Git:**
- [x] Repository created
- [x] Initial commit done
- [x] All files added
- [x] Pushed to GitLab

**Testing:**
- [x] Web upload tested
- [x] S3 trigger tested
- [x] Rate limiting tested
- [x] Error handling tested
- [x] Copy/download tested

---

## 📊 Key Metrics

**Development Time:** ~8 hours (initial build + iterations)  
**Code Lines:** ~300 (Python) + ~200 (JavaScript/HTML)  
**AWS Services:** 4 (Lambda, S3, IAM, CloudWatch)  
**Total Cost:** $0.00/month  
**Uptime:** 100% (serverless)  

---

## 🎓 What I Learned

**AWS Skills:**
- Lambda function creation and configuration
- Lambda layers (dependencies)
- Lambda Function URLs
- S3 static website hosting
- S3 event triggers
- IAM roles and permissions
- CloudWatch monitoring
- Billing alarms

**Development Skills:**
- Serverless architecture patterns
- Base64 encoding for binary data
- CORS configuration
- Rate limiting strategies
- Text processing algorithms
- Git version control
- Technical documentation

**Problem Solving:**
- Debugged PyPDF2 layer structure (typo: "puthon")
- Fixed CORS double-header issue
- Resolved base64 double-encoding
- Implemented rate limiting without database
- URL encoding issues with special characters

---

## 📝 Notes for Future Maintenance

**When updating Lambda code:**
1. Test locally if possible
2. Update in AWS console
3. Click Deploy
4. Test with actual PDF
5. Check CloudWatch logs
6. Update local Git files
7. Commit and push

**When updating website:**
1. Edit local HTML file
2. Test locally (open in browser)
3. Upload to S3 (overwrites)
4. Test on actual S3 URL
5. Commit to Git

**When costs change:**
1. Check CloudWatch billing metrics
2. Review CloudWatch logs for unusual activity
3. Verify rate limiting is working
4. Check S3 bucket sizes

**Before making public:**
- Add authentication mechanism
- Consider API Gateway instead of Function URL
- Add usage analytics
- Improve rate limiting (use DynamoDB)

---

## 🔗 Important Links

**Live Website:** https://my-pdf-chunker-website.s3.us-east-2.amazonaws.com/pdf-chunker.html  
**Lambda Function URL:** https://6utxwfiwqyll6dtneyd54vcei40xfkmq.lambda-url.us-east-2.on.aws/  
**GitLab Repo:** [Add your actual URL here]  
**CloudWatch Logs:** AWS Console → CloudWatch → /aws/lambda/PDFToTextChunker

---

## 👤 Contact & Credits

**Developer:** David Schmidt  
**Purpose:** Personal tool + portfolio project  
**Status:** Actively maintained  
**License:** MIT

**Built with help from:** Claude (Anthropic) for architecture advice and troubleshooting

---

**Last Updated:** November 6, 2025  
**Next Review:** When adding new features or if issues arise
