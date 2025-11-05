# PDF to Text Chunks

Serverless PDF processing app using AWS Lambda

## Files
- `lambda_function.py` - Lambda function (Python 3.13)
- `pdf-chunker.html` - Web interface

## AWS Resources
- **Lambda Function**: PDFToTextChunker
- **Lambda URL**: https://6utxwfiwqyll6dtneyd54vcei40xfkmq.lambda-url.us-east-2.on.aws/
- **S3 Input Bucket**: my-pdf-input-bucket-dave
- **S3 Output Bucket**: my-pdf-output-bucket-dave
- **Lambda Layer**: PyPDF2-Layer (Python 3.13)

## Current Settings
- Rate limit: 10 requests per IP per hour
- Chunk size: 20,000 characters
- PDF size limit: 6 MB (web), unlimited (S3)

## Change Log
- 2025-11-05: Initial build with web interface and rate limiting