# Project Files Guide

Complete list of files for the PDF to Text Chunks project and their purposes.

## Core Application Files

### `lambda_function.py` ⭐ REQUIRED
**What:** The main Lambda function code
**Why:** The backend that processes PDFs
**Git:** ✅ YES - Commit this
**AWS:** Deploy to Lambda function
**Notes:** This is your actual application logic

### `pdf-chunker.html` ⭐ REQUIRED
**What:** Web interface for uploading PDFs
**Why:** User-facing frontend
**Git:** ✅ YES - Commit this
**AWS:** Optionally upload to S3 for static hosting
**Notes:** Works standalone or from S3

---

## Configuration Files

### `.gitignore` ⭐ CRITICAL
**What:** Tells Git which files to ignore
**Why:** Prevents committing secrets, temp files, credentials
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Only for Git
**Notes:** MUST HAVE - protects you from exposing sensitive data

### `requirements.txt`
**What:** Lists Python dependencies
**Why:** Standard Python practice, shows what packages are needed
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Useful for documentation, Lambda layer creation

### `.env.example`
**What:** Template showing what configuration variables are needed
**Why:** Documents required settings without exposing real values
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Copy to `.env` locally, NEVER commit `.env`

---

## Documentation Files

### `README.md` ⭐ IMPORTANT
**What:** Main project description
**Why:** First thing people see on GitLab/GitHub
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Only for Git
**Notes:** Critical for portfolio/job applications

### `PROJECT_INSTRUCTIONS.md` ⭐ IMPORTANT
**What:** Comprehensive AI assistant context file
**Why:** Provides complete project background for AI-assisted development
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Contains technical stack, development principles, workflow instructions, and interview talking points. Use at start of AI work sessions and when onboarding collaborators. Update after major features, deployment changes, or architectural decisions.

### `SETUP.md`
**What:** AWS setup instructions
**Why:** Helps others (or future you) recreate the project
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Step-by-step AWS configuration

### `CHANGELOG.md`
**What:** Track of all changes over time
**Why:** Professional documentation practice
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Update every time you make changes

### `CONTRIBUTING.md`
**What:** Guidelines for contributors
**Why:** If you open-source it, tells people how to help
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Optional but professional

---

## Legal/License Files

### `LICENSE`
**What:** MIT License (permissive open source)
**Why:** Tells people they can use/modify your code
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Reference only
**Notes:** Replace "[Your Name]" with your actual name

---

## Utility Scripts

### `deploy.sh`
**What:** Bash script to deploy Lambda updates
**Why:** Makes updating Lambda function easier
**Git:** ✅ YES - Commit this
**AWS:** ❌ NO - Run locally
**Notes:** Make executable with `chmod +x deploy.sh`
**Usage:** `./deploy.sh` (after configuring AWS CLI)

---

## Files You Should NOT Commit

### ❌ `.env`
**What:** Your actual configuration with real values
**Why:** Contains secrets (bucket names, URLs)
**Git:** ❌ NO - NEVER commit
**AWS:** ❌ NO
**Notes:** Copy from `.env.example`, add to `.gitignore`

### ❌ `*.zip`
**What:** Lambda deployment packages or layer zips
**Why:** Binary files, can regenerate
**Git:** ❌ NO - Too large
**AWS:** Upload when needed
**Notes:** .gitignore excludes these

### ❌ `__pycache__/`, `*.pyc`
**What:** Python compiled bytecode
**Why:** Generated files
**Git:** ❌ NO - Auto-generated
**AWS:** ❌ NO
**Notes:** .gitignore excludes these

### ❌ `.DS_Store`
**What:** Mac system file
**Why:** Not part of your project
**Git:** ❌ NO - System file
**AWS:** ❌ NO
**Notes:** .gitignore excludes these

### ❌ Test PDFs
**What:** Sample PDFs you use for testing
**Why:** Can contain sensitive info, large files
**Git:** ❌ NO - Too large
**AWS:** ❌ NO
**Notes:** .gitignore excludes `test_*.pdf`

---

## Complete File Structure

Your project should look like this:

```
pdf-chunker/
├── lambda_function.py          # ⭐ Lambda code
├── pdf-chunker.html            # ⭐ Web interface
├── README.md                   # ⭐ Project overview
├── PROJECT_INSTRUCTIONS.md     # ⭐ AI assistant context
├── SETUP.md                    # AWS setup guide
├── CHANGELOG.md                # Change history
├── CONTRIBUTING.md             # Contribution guide
├── LICENSE                     # MIT License
├── requirements.txt            # Python dependencies
├── .env.example                # Config template
├── .gitignore                  # ⭐ CRITICAL - Git exclusions
├── deploy.sh                   # Deployment script
└── .git/                       # Git repository (hidden)
```

---

## First Time Setup Checklist

When setting up the repository:

1. ✅ Create all files above
2. ✅ Replace "[Your Name]" in LICENSE
3. ✅ Update URLs in README.md with your actual URLs
4. ✅ Copy `.env.example` to `.env` and fill in your values
5. ✅ Add `.env` to `.gitignore` (already done)
6. ✅ Initialize Git: `git init`
7. ✅ Add all files: `git add .`
8. ✅ First commit: `git commit -m "Initial commit"`
9. ✅ Push to GitLab: `git push origin main`

---

## What to Update When Making Changes

### Changed Lambda function?
- Update `lambda_function.py`
- Update `CHANGELOG.md`
- Commit and push
- Deploy to AWS

### Changed web interface?
- Update `pdf-chunker.html`
- Update `CHANGELOG.md`
- Commit and push
- Re-upload to S3 if hosting there

### Changed configuration?
- Update `.env.example` (template)
- Update `SETUP.md` if instructions changed
- Update your own `.env` (don't commit)
- Commit template changes

### Added new feature?
- Update relevant code files
- Update `README.md` (add to features list)
- Update `CHANGELOG.md` (under [Unreleased] or new version)
- Commit and push

---

## For Job Applications

**Minimum files to show:**
- `lambda_function.py` - Shows Python/AWS skills
- `pdf-chunker.html` - Shows frontend skills
- `README.md` - Shows documentation skills

**Professional bonus:**
- All the documentation files show you're thorough
- `CHANGELOG.md` shows you track your work
- `.gitignore` shows you understand best practices
- `deploy.sh` shows automation thinking

---

## Quick Reference: Git Commands

```bash
# See what files will be committed
git status

# See what changed
git diff

# Add all files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitLab
git push

# Pull latest
git pull
```

---

## Questions?

If you're unsure about any file:
1. Check if it's in `.gitignore` → Don't commit
2. Contains secrets/keys? → Don't commit
3. Auto-generated? → Don't commit
4. Everything else → Probably commit it
