# Quick Start Guide - QA Testing Environment

## Overview
Your environment is now configured as a 3-layer AI agent architecture specialized for generating comprehensive QA testing documentation.

## What Was Created

### 1. Core Architecture
- **[directives/](directives/)** - SOPs for test generation workflows
- **[execution/](execution/)** - Python scripts for automated document creation
- **[.tmp/](.tmp/)** - Temporary files (auto-generated, gitignored)

### 2. QA Testing Directives
- **[directives/generate_test_plan.md](directives/generate_test_plan.md)** - Instructions for creating comprehensive test plans
- **[directives/generate_test_cases.md](directives/generate_test_cases.md)** - Instructions for generating detailed test cases
- **[directives/generate_exploratory_tests.md](directives/generate_exploratory_tests.md)** - Instructions for exploratory testing charters

### 3. Execution Scripts
- **[execution/create_google_doc.py](execution/create_google_doc.py)** - Google Docs API integration
- **[execution/generate_test_plan.py](execution/generate_test_plan.py)** - Test plan content generator
- **[execution/generate_test_cases.py](execution/generate_test_cases.py)** - Test case generator with multiple techniques

### 4. Configuration Files
- **[.env.example](.env.example)** - Template for environment variables
- **[.gitignore](.gitignore)** - Prevents committing secrets and temp files
- **[requirements.txt](requirements.txt)** - Python dependencies

### 5. Agent Instructions
- **[AGENT.md](AGENT.md)** - Core architecture documentation
- **[GEMINI.md](GEMINI.md)** - Extended with Senior QA Engineer role and instructions
- **[CLAUDE.md](CLAUDE.md)** - Mirror for Claude environments

## Setup Instructions

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env to add your API keys if needed
```

### Step 3: Google API Setup (Required for Google Docs)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Google Docs API
   - Google Drive API
4. Create OAuth 2.0 credentials:
   - Application type: Desktop app
   - Download as `credentials.json`
   - Place in project root
5. First run will prompt OAuth and create `token.json` automatically

## How to Use

### Generate QA Documentation for a Requirement

When you provide a requirement to your AI agent (via Gemini, Claude, etc.), it will:

1. **Analyze the requirement** and ask clarifying questions
2. **Generate Test Plan** using the directives and scripts
3. **Generate Test Cases** with comprehensive coverage using:
   - Equivalence Partitioning
   - Boundary Value Analysis
   - Positive/Negative Testing
   - Security Testing
4. **Generate Exploratory Testing Charters** for uncovering edge cases
5. **Create Google Docs** for all deliverables
6. **Provide URLs** to access the documents

### Example Interaction

```
You: "I need test documentation for a login feature with email/password
     and OAuth (Google, Facebook)"

AI Agent:
1. Asks clarifying questions about:
   - MFA requirements
   - Password policies
   - Session management
   - Target platforms

2. Generates:
   - Test Plan (25-30 pages)
   - Test Cases (50-100 test cases)
   - Exploratory Testing Charters (5-10 charters)

3. Returns:
   - Google Docs URLs
   - Summary of coverage
```

## Testing Capabilities

### Test Design Techniques Covered
- ✅ Equivalence Partitioning
- ✅ Boundary Value Analysis
- ✅ Positive Testing (Happy Path)
- ✅ Negative Testing
- ✅ Decision Table Testing
- ✅ State Transition Testing
- ✅ Security Testing (OWASP Top 10)
- ✅ Use Case Testing

### Test Coverage Includes
- Functional testing
- Integration testing
- Regression testing
- Security testing (SQL injection, XSS, authorization)
- Performance testing guidelines
- Accessibility testing (WCAG 2.1 AA)
- Cross-browser/device compatibility

## Manual Testing (Without AI Agent)

You can also use the scripts directly:

### Generate Test Plan
```bash
python execution/generate_test_plan.py "Login feature with OAuth" \
  --platform web \
  --project "MyApp" \
  --output .tmp/test_plan.json
```

### Generate Test Cases
```bash
python execution/generate_test_cases.py "Login feature" \
  --feature "LOGIN" \
  --output .tmp/test_cases.json
```

### Create Google Doc
```bash
python execution/create_google_doc.py test_plan "MyApp - Test Plan"
```

## Architecture Benefits

### Why 3 Layers?

**Problem:** AI doing everything = 90% accuracy per step = 59% success over 5 steps

**Solution:**
- **Layer 1 (Directives):** Human-readable instructions
- **Layer 2 (AI Orchestration):** Intelligent routing and decision-making
- **Layer 3 (Execution):** Deterministic Python scripts

**Result:** Reliable, consistent, and self-improving system

### Self-Annealing
When errors occur:
1. AI reads error and stack trace
2. Fixes the script
3. Tests the fix
4. Updates the directive with learnings
5. System becomes stronger

## Next Steps

1. **Test the setup:**
   ```bash
   python execution/generate_test_cases.py "Sample feature" --feature "TEST"
   ```

2. **Provide a real requirement** to your AI agent

3. **Review generated documents** and provide feedback

4. **Customize directives** based on your organization's standards

## Support

- Check [README.md](README.md) for detailed architecture
- Check [AGENT.md](AGENT.md) for operating principles
- Check [GEMINI.md](GEMINI.md) for QA engineer role details

## File Organization

```
requirment_analyzer/
├── AGENT.md              # Core architecture
├── GEMINI.md             # QA Engineer role (extended)
├── CLAUDE.md             # Mirror for Claude
├── README.md             # Project documentation
├── QUICKSTART.md         # This file
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git exclusions
├── credentials.json      # Google OAuth (you create)
├── token.json            # Google OAuth token (auto-generated)
├── directives/           # Testing SOPs
│   ├── generate_test_plan.md
│   ├── generate_test_cases.md
│   └── generate_exploratory_tests.md
├── execution/            # Python scripts
│   ├── create_google_doc.py
│   ├── generate_test_plan.py
│   └── generate_test_cases.py
└── .tmp/                 # Temporary files (auto-generated)
```

## Key Principle

**Local files are temporary. Deliverables live in Google Docs/Sheets where stakeholders can access them.**

Everything in `.tmp/` can be deleted and regenerated as needed.

---

Your QA testing environment is ready! 🚀
