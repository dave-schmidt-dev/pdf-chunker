import json
import boto3
import re
import base64
from PyPDF2 import PdfReader
from io import BytesIO
from datetime import datetime, timedelta

s3 = boto3.client('s3')

# Rate limiting: max 10 requests per IP per hour
request_history = {}
MAX_REQUESTS_PER_IP = 10

def is_rate_limited(ip_address):
    """Check if this IP has exceeded rate limit"""
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    # Clean old entries
    request_history[ip_address] = [
        req_time for req_time in request_history.get(ip_address, [])
        if req_time > one_hour_ago
    ]
    
    # Check limit
    if len(request_history.get(ip_address, [])) >= MAX_REQUESTS_PER_IP:
        return True
    
    # Add this request
    if ip_address not in request_history:
        request_history[ip_address] = []
    request_history[ip_address].append(now)
    
    return False

def lambda_handler(event, context):
    """Route to appropriate handler based on event type"""
    if 'Records' in event:
        return handle_s3_trigger(event, context)
    else:
        return handle_web_request(event, context)

def handle_web_request(event, context):
    """Handle direct PDF upload from web interface"""
    try:
        # Get IP address for rate limiting
        ip_address = event.get('requestContext', {}).get('http', {}).get('sourceIp', 'unknown')
        print(f"Request from IP: {ip_address}")
        
        # Check rate limit
        if is_rate_limited(ip_address):
            print(f"Rate limit exceeded for {ip_address}")
            return {
                'statusCode': 429,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': 'Rate limit exceeded. Maximum 10 requests per hour.'
                })
            }
        
        print("Handling web request...")
        
        # Get the body
        body_str = event.get('body', '{}')
        
        # If Lambda encoded the whole body as base64, decode it first
        if event.get('isBase64Encoded'):
            print("Decoding base64 body...")
            body_str = base64.b64decode(body_str).decode('utf-8')
        
        # Parse as JSON
        body = json.loads(body_str)
        
        pdf_base64 = body.get('pdf', '')
        filename = body.get('filename', 'upload.pdf')
        
        if not pdf_base64:
            raise ValueError("No PDF data in request")
        
        print(f"Processing file: {filename}")
        
        # Decode the PDF from base64
        pdf_content = base64.b64decode(pdf_base64)
        print(f"Decoded PDF: {len(pdf_content)} bytes")
        
        # Extract text
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_content)
        
        # Clean up formatting
        print("Cleaning up formatting...")
        text = clean_text(text)
        print(f"Final text: {len(text)} characters")
        
        # Split into chunks
        print("Splitting into chunks...")
        chunks = split_into_chunks(text, chunk_size=20000)
        print(f"Created {len(chunks)} chunks")
        
        # Return chunks directly to the user
        response_body = {
            'success': True,
            'chunks': chunks,
            'total_characters': len(text),
            'num_chunks': len(chunks)
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response_body)
        }
        
    except Exception as e:
        print(f"Error in web request: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }

def handle_s3_trigger(event, context):
    """Handle S3 trigger event (existing functionality)"""
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: {key} from bucket: {bucket}")
    
    output_bucket = 'my-pdf-output-bucket-dave'
    
    try:
        # Download PDF from S3
        print("Downloading PDF from S3...")
        pdf_object = s3.get_object(Bucket=bucket, Key=key)
        pdf_content = pdf_object['Body'].read()
        
        # Extract text
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_content)
        
        # Clean up formatting
        print("Cleaning up formatting...")
        text = clean_text(text)
        print(f"Final text: {len(text)} characters")
        
        # Split into chunks
        print("Splitting into chunks...")
        chunks = split_into_chunks(text, chunk_size=20000)
        print(f"Created {len(chunks)} chunks")
        
        # Upload each chunk to S3
        print("Uploading chunks to S3...")
        base_name = key.replace('.pdf', '').replace('.PDF', '')
        
        for i, chunk in enumerate(chunks, start=1):
            chunk_filename = f"{base_name}_part{i}.txt"
            
            s3.put_object(
                Bucket=output_bucket,
                Key=chunk_filename,
                Body=chunk.encode('utf-8'),
                ContentType='text/plain'
            )
            
            print(f"Uploaded {chunk_filename} ({len(chunk)} characters)")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {key}',
                'chunks_created': len(chunks)
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

def extract_text_from_pdf(pdf_content):
    """Extract all text from PDF bytes"""
    pdf_file = BytesIO(pdf_content)
    reader = PdfReader(pdf_file)
    
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    return text

def clean_text(text):
    """Clean up text formatting to make it readable"""
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Add line break after sentence endings
    text = re.sub(r'([.!?])\s+([A-Z])', r'\1\n\n\2', text)
    
    # Add line break after speaker names
    text = re.sub(r'([A-Z][A-Za-z\s]+:)\s*', r'\1\n', text)
    
    # Clean up excessive newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    return text.strip()

def split_into_chunks(text, chunk_size=20000):
    """Split text into chunks at paragraph boundaries"""
    chunks = []
    paragraphs = text.split('\n\n')
    
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                chunks.append(para)
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
