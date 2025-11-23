import os
import json
import base64
import sys
import time

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m' # No Color

def generate_minimal_pdf():
    """
    Generates a minimal valid PDF 1.4 file in memory.
    Contains the text "Hello World" on a single page.
    """
    # Minimal PDF structure
    pdf_content = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n"
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"5 0 obj\n<< /Length 44 >>\nstream\n"
        b"BT /F1 24 Tf 100 700 Td (Hello World from Smoke Test) Tj ET\n"
        b"endstream\nendobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000244 00000 n \n"
        b"0000000331 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n425\n%%EOF"
    )
    return pdf_content

def get_lambda_url():
    """Get Lambda URL from env var or prompt user."""
    url = os.environ.get('LAMBDA_FUNCTION_URL')
    if not url:
        print(f"{YELLOW}LAMBDA_FUNCTION_URL environment variable not set.{NC}")
        print("Please enter the Lambda Function URL:")
        url = input("> ").strip()
    
    if not url:
        print(f"{RED}Error: No URL provided.{NC}")
        sys.exit(1)
        
    return url

def make_request(url, payload):
    """Make HTTP POST request using urllib (dependency-free)."""
    import urllib.request
    import urllib.error
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PDF-Chunker-Smoke-Test/1.0'
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')
            return status_code, json.loads(response_body)
    except urllib.error.HTTPError as e:
        response_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(response_body)
        except:
            return e.code, {'error': str(e), 'body': response_body}
    except Exception as e:
        return 0, {'error': str(e)}

def main():
    print(f"{YELLOW}Starting PDF Chunker Smoke Test...{NC}")
    
    # 1. Configuration
    url = get_lambda_url()
    print(f"Target URL: {url}")
    
    # 2. Test Data
    print("Generating minimal PDF...")
    pdf_bytes = generate_minimal_pdf()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    
    payload = {
        "pdf": pdf_base64,
        "filename": "smoke_test.pdf"
    }
    
    # 3. Execution
    print("Sending request...")
    start_time = time.time()
    status_code, response = make_request(url, payload)
    duration = time.time() - start_time
    
    print(f"Response received in {duration:.2f}s")
    print(f"Status Code: {status_code}")
    
    # 4. Validation
    failed = False
    failure_reasons = []
    
    if status_code != 200:
        failed = True
        failure_reasons.append(f"Expected status 200, got {status_code}")
    
    if not response.get('success'):
        failed = True
        failure_reasons.append(f"Response 'success' is not True. Error: {response.get('error')}")
    
    chunks = response.get('chunks', [])
    if not isinstance(chunks, list):
        failed = True
        failure_reasons.append("Response 'chunks' is not a list")
    elif len(chunks) == 0:
        failed = True
        failure_reasons.append("No chunks returned")
    else:
        # Check content of first chunk
        first_chunk = chunks[0]
        if "Hello World" not in first_chunk:
            failed = True
            failure_reasons.append(f"Expected 'Hello World' in chunk, got: {first_chunk[:50]}...")
            
    # 5. Reporting
    print("-" * 40)
    if failed:
        print(f"{RED}❌ SMOKE TEST FAILED{NC}")
        for reason in failure_reasons:
            print(f"{RED}  - {reason}{NC}")
        print(f"\nFull Response:\n{json.dumps(response, indent=2)}")
        sys.exit(1)
    else:
        print(f"{GREEN}✅ SMOKE TEST PASSED{NC}")
        print(f"Chunks received: {len(chunks)}")
        print(f"First chunk preview: {chunks[0][:50]}")
        sys.exit(0)

if __name__ == "__main__":
    main()
