# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-11-05

### Added
- Initial release of PDF to Text Chunks application
- Lambda function with dual handlers (S3 trigger and Function URL)
- Web interface with drag-and-drop PDF upload
- Text extraction using PyPDF2
- Smart text formatting with paragraph detection
- Automatic chunking at 20,000 character boundaries
- Rate limiting (10 requests per IP per hour)
- Copy to clipboard functionality
- Download chunks as .txt files
- S3 trigger support for automated processing

### Features
- Serverless architecture (AWS Lambda + S3)
- Clean, responsive web UI
- Base64 encoding for binary data transfer
- CORS configuration for cross-origin requests
- Comprehensive error handling and logging
- CloudWatch integration for monitoring

### Infrastructure
- Lambda Function: PDFToTextChunker (Python 3.13)
- Lambda Layer: PyPDF2-Layer
- S3 Buckets: Input and Output
- Lambda Function URL enabled
- S3 static website hosting support

## Future Enhancements

### Planned
- [ ] Adjustable chunk size from UI
- [ ] Batch processing (multiple PDFs)
- [ ] Email notification when processing complete
- [ ] Progress indicator for large files
- [ ] Mobile-optimized interface
- [ ] Authentication/password protection
- [ ] Custom domain support
- [ ] Download all chunks as .zip
- [ ] Preview chunks before download
- [ ] Dark mode

### Under Consideration
- [ ] PDF page selection (process only certain pages)
- [ ] OCR support for scanned PDFs
- [ ] Multiple output formats (JSON, CSV)
- [ ] Webhook support
- [ ] API key authentication
- [ ] Usage analytics dashboard
