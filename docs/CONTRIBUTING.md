# Contributing to PDF to Text Chunks

Thank you for your interest in contributing! This is a personal learning project, but improvements are welcome.

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in Issues
- Include steps to reproduce
- Include expected vs actual behavior
- Include CloudWatch logs if applicable

### Suggesting Enhancements
- Describe the enhancement and why it would be useful
- Consider AWS free tier implications
- Keep it simple - this is a learning project

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly in your own AWS account
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

See [SETUP.md](SETUP.md) for AWS configuration.

### Local Development
```bash
# Clone the repo
git clone https://gitlab.com/yourname/pdf-chunker.git
cd pdf-chunker

# Install dependencies
pip install -r requirements.txt

# Test Lambda function locally (optional)
# You'll need AWS SAM or similar tools
```

## Code Style

### Python
- Follow PEP 8
- Use descriptive function names
- Add docstrings to functions
- Keep functions focused (single responsibility)

### JavaScript
- Use modern ES6+ syntax
- Use `const` and `let` (not `var`)
- Add comments for complex logic

## Testing Checklist

Before submitting a PR, verify:
- [ ] Lambda function deploys successfully
- [ ] Web interface loads without errors
- [ ] PDF upload works via web
- [ ] S3 trigger still works
- [ ] Rate limiting functions correctly
- [ ] CloudWatch logs show no errors
- [ ] Chunks are properly formatted
- [ ] Character counts are accurate

## Questions?

Open an issue or reach out directly. This is a learning project, so don't be shy!
