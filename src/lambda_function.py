import json
import boto3
import re
import base64
import os
from pypdf import PdfReader
from io import BytesIO
from datetime import datetime, timedelta

s3 = boto3.client('s3')

# Rate limiting: max requests per IP per hour (local to container)
request_history = {}
MAX_REQUESTS_PER_IP = int(os.environ.get('MAX_REQUESTS_PER_IP', '10'))
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '20000'))
OUTPUT_BUCKET = os.environ.get('OUTPUT_BUCKET', 'my-pdf-output-bucket-dave')

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
                    'error': f'Rate limit exceeded. Maximum {MAX_REQUESTS_PER_IP} requests per hour.'
                })
            }
        
        print("Handling web request...")
        
        # Get the body
        body_str = event.get('body', '{}')
        
        # If Lambda encoded the whole body as base64, decode it first
        if event.get('isBase64Encoded'):
            print("Decoding base64 body...")
            try:
                body_str = base64.b64decode(body_str).decode('utf-8')
            except Exception as e:
                raise ValueError(f"Invalid base64 encoded body: {str(e)}")
        
        # Parse as JSON
        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")
        
        pdf_base64 = body.get('pdf', '')
        filename = body.get('filename', 'upload.pdf')
        
        if not pdf_base64:
            raise ValueError("No PDF data in request")
        
        print(f"Processing file: {filename}")
        
        # Decode the PDF from base64
        try:
            pdf_content = base64.b64decode(pdf_base64)
        except Exception as e:
            raise ValueError(f"Invalid base64 encoded PDF data: {str(e)}")

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
        chunks = split_into_chunks(text, chunk_size=CHUNK_SIZE)
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
        
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
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
                'error': "Internal server error"
            })
        }

def handle_s3_trigger(event, context):
    """Handle S3 trigger event (existing functionality)"""
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: {key} from bucket: {bucket}")
    
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
        chunks = split_into_chunks(text, chunk_size=CHUNK_SIZE)
        print(f"Created {len(chunks)} chunks")
        
        # Upload each chunk to S3
        print("Uploading chunks to S3...")
        base_name = key.replace('.pdf', '').replace('.PDF', '')
        
        for i, chunk in enumerate(chunks, start=1):
            chunk_filename = f"{base_name}_part{i}.txt"
            
            s3.put_object(
                Bucket=OUTPUT_BUCKET,
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
    """Split text into chunks with strict size limits"""
    chunks = []
    paragraphs = text.split('\n\n')
    
    current_chunk = ""
    
    for para in paragraphs:
        # Check if paragraph itself is too large
        if len(para) > chunk_size:
            # If we have a current chunk, add it first
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # Split large paragraph
            sub_chunks = split_large_text(para, chunk_size)
            
            # Add all sub-chunks except potentially the last one if it fits in next
            # But for simplicity, just add them all as separate chunks
            chunks.extend(sub_chunks)
            
        elif len(current_chunk) + len(para) + 2 > chunk_size:
            # Current chunk full, push it
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            # Add to current chunk
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def split_large_text(text, limit):
    """Helper to split a large block of text into smaller pieces"""
    chunks = []
    
    # First try splitting by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current_chunk = ""
    
    for sentence in sentences:
        if len(sentence) > limit:
            # Sentence itself is too big, hard split
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            # Hard split by characters
            for i in range(0, len(sentence), limit):
                chunks.append(sentence[i:i+limit])
                
        elif len(current_chunk) + len(sentence) + 1 > limit:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
                
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks
