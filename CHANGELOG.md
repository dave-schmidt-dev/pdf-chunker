# Changelog

All notable changes to the PDF to Text Chunker project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-11-09

### Added
- **PROJECT_INSTRUCTIONS.md** - Comprehensive AI assistant context file with complete project background, technical stack, development principles, and workflow instructions
- **Automated file access workflow** - README now includes explicit raw.githubusercontent.com URLs for all repository files, enabling AI assistants to automatically access any file without manual linking
- **Simplified project instructions** - Created CLAUDE_PROJECT_INSTRUCTIONS.txt for use in Claude Project settings

### Changed
- **README.md** - Repository Files section now uses explicit raw file URLs instead of generic "View" links, enabling automated tool access
- **README.md** - Added PROJECT_INSTRUCTIONS.md to Documentation table
- **Project workflow** - New conversation start process: provide README raw link, AI assistant can then access all files automatically

### Documentation
- AI assistants can now access entire repo by fetching README and following embedded links
- Established template for future projects with same workflow
- Updated documentation reflects modern approach to AI-assisted development

### Technical
- All file links point to raw.githubusercontent.com for direct content access
- Note added about cache delays when updating files
- Workflow designed around web_fetch tool capabilities and limitations

## [1.2.0] - 2025-11-07

### Added
- Professional logo with transparent background
- Logo files in both PNG (379KB) and WEBP (23KB) formats
- 94% file size reduction with WEBP optimization
- Progressive enhancement with `<picture>` element for logo display
- Logo integration in website header with fade-in animation
- Logo integration in README.md with professional badges
- Comprehensive logo documentation (LOGO_DEPLOYMENT.md, LOGO_SUMMARY.md)
- Cache troubleshooting documentation
- Bucket policy support in deployment script

### Changed
- Updated `deploy.sh` to use S3 bucket policies instead of ACLs
- Migrated from ACL-based permissions to bucket policy (modern AWS approach)
- Enhanced website visual design with logo and improved branding
- Updated README.md with centered logo, badges, and improved formatting
- Improved PROJECT_SUMMARY.md with branding section and deployment updates
- Updated repository structure to include logo files
- Enhanced deployment documentation with bucket policy instructions

### Fixed
- S3 ACL compatibility issues with modern bucket security settings
- PNG transparency issues (alpha channel properly set to 0)
- Logo background removal (removed light gray opaque background)
- Browser cache issues with logo display (added cache-busting documentation)
- Deploy script now works with S3 buckets that block ACLs

### Technical Improvements
- Image optimization: WEBP format reduces file size by 94%
- Progressive enhancement: Modern browsers get WEBP, older browsers get PNG
- Transparent background: Logo works on any background color
- Bucket policy: More secure and maintainable than per-file ACLs
- Deployment automation: Script handles both logo formats automatically

## [1.1.0] - 2025-11-07

### Added
- Automated deployment script (`deploy.sh`)
- Full automation for Lambda and S3 deployments
- Flexible deployment options (all/lambda/website)
- Git status checking in deployment script
- Color-coded output in deployment script
- AWS CLI setup and configuration
- Deployment script error handling

### Changed
- Migrated from GitLab to GitHub as primary repository
- Updated all documentation to reflect GitHub workflow
- Improved deployment workflow documentation
- Updated PROJECT_SUMMARY.md with deployment automation details

### Fixed
- Manual deployment errors through automation
- Inconsistent deployment process
- Missing deployment verification steps

## [1.0.0] - 2025-11-05

### Added
- Core PDF to text chunking functionality
- Lambda Function URL for direct web access
- Web interface with drag-and-drop upload
- S3 trigger support for automated processing
- Rate limiting (10 PDFs per hour per IP)
- Copy to clipboard functionality
- Download chunks as .txt files
- CloudWatch logging
- Billing alarm at $5 threshold
- Lambda concurrency limit (10)
- Purple gradient website design
- Error handling and user feedback
- Character count display for chunks
- Preview of text chunks
- Smart chunking at paragraph boundaries (20,000 characters)

### Technical Implementation
- AWS Lambda with Python 3.13
- PyPDF2 library via Lambda Layer
- S3 static website hosting
- S3 event triggers
- Lambda Function URLs with CORS
- Base64 encoding for PDF transfer
- In-memory rate limiting
- Text cleaning and formatting algorithms

### Documentation
- README.md with project overview
- SETUP.md with AWS configuration steps
- PROJECT_SUMMARY.md with comprehensive details
- CONTRIBUTING.md with contribution guidelines
- LICENSE (MIT)
- .gitignore for project files
- .env.example for configuration template
- Multiple Mermaid diagrams (architecture, workflow, etc.)
- DIAGRAMS.md with diagram documentation
- PROJECT_FILES.md with file descriptions

### Infrastructure
- Lambda function: PDFToTextChunker
- S3 input bucket: my-pdf-input-bucket-dave
- S3 output bucket: my-pdf-output-bucket-dave
- S3 website bucket: my-pdf-chunker-website
- IAM role with S3 full access
- CloudWatch log group

## [Unreleased]

### Planned Features
- Mobile responsive design improvements
- Adjustable chunk size (user configurable)
- Download all chunks as ZIP file
- Processing history (localStorage)
- Better error messages with suggestions
- Performance monitoring
- Unit tests
- Integration tests
- CI/CD pipeline
- Docker containerization
- React version of UI
- TypeScript migration

### Considerations
- Authentication/authorization system
- API Gateway migration (from Function URL)
- DynamoDB for persistent rate limiting
- CloudFront distribution
- Custom domain name
- Usage analytics
- OCR support for scanned PDFs
- Multi-language support
- Batch processing
- Email integration

---

## Version History Summary

- **1.2.0** - Logo, branding, and S3 bucket policy support
- **1.1.0** - Automated deployment and GitHub migration
- **1.0.0** - Initial release with core functionality

---

## Breaking Changes

### 1.2.0
- Deploy script now requires AWS CLI configured with proper credentials
- S3 buckets must allow bucket policies (no ACL support)
- Logo files must be present in project root for website deployment

### 1.1.0
- Deployment requires AWS CLI instead of manual console uploads
- Repository primary location changed from GitLab to GitHub

---

## Migration Guides

### Migrating to 1.2.0 (Bucket Policy)

If you have an older version using ACLs:

1. Update `deploy.sh` script:
   ```bash
   cp ~/Downloads/deploy.sh .
   chmod +x deploy.sh
   ```

2. Add logo files:
   ```bash
   cp ~/Downloads/logo.png .
   cp ~/Downloads/logo.webp .
   ```

3. Update HTML and README:
   ```bash
   cp ~/Downloads/pdf-chunker.html .
   cp ~/Downloads/README.md .
   ```

4. Set bucket policy:
   ```bash
   aws s3api put-bucket-policy --bucket my-pdf-chunker-website \
     --policy '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"arn:aws:s3:::my-pdf-chunker-website/*"}]}' \
     --region us-east-2
   ```

5. Deploy:
   ```bash
   ./deploy.sh
   ```

### Migrating to 1.1.0 (Automated Deployment)

If upgrading from 1.0.0:

1. Install AWS CLI:
   ```bash
   # macOS
   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /
   ```

2. Configure AWS CLI:
   ```bash
   aws configure
   ```

3. Add deploy script:
   ```bash
   cp ~/Downloads/deploy.sh .
   chmod +x deploy.sh
   ```

4. Test deployment:
   ```bash
   ./deploy.sh website
   ```

---

## Known Issues

### Current
- Rate limiting resets on Lambda cold starts (not persistent)
- No authentication (public access)
- OCR not supported (scanned PDFs don't work)
- 6MB file size limit

### Fixed
- ~~S3 ACL errors with modern buckets~~ - Fixed in 1.2.0 with bucket policy
- ~~Logo transparency issues~~ - Fixed in 1.2.0 with proper alpha channel
- ~~Manual deployment errors~~ - Fixed in 1.1.0 with automated script

---

## Contributors

- **David Schmidt** ([@dave-schmidt-dev](https://github.com/dave-schmidt-dev)) - Creator and maintainer
- **Claude (Anthropic)** - Architecture advice, troubleshooting, and optimization assistance

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated:** November 7, 2025
