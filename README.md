# Requirement Analyzer

A 3-layer AI agent architecture for reliable, deterministic execution of complex workflows.

## Architecture Overview

This system separates concerns into 3 layers:

1. **Directives** (`directives/`) - Natural language SOPs defining what to do
2. **Orchestration** (AI Agent) - Intelligent routing and decision-making
3. **Execution** (`execution/`) - Deterministic Python scripts that do the work

See [AGENT.md](AGENT.md) for detailed architecture documentation.

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
```

### 3. Google API Setup (if using Google Sheets/Slides)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API and Google Slides API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` and place in project root
6. First run will generate `token.json` automatically

## Directory Structure

```
.
├── AGENT.md              # Agent architecture instructions
├── CLAUDE.md             # Mirror of AGENT.md for Claude
├── GEMINI.md             # Mirror of AGENT.md for Gemini
├── directives/           # SOPs and instructions (natural language)
├── execution/            # Python scripts (deterministic tools)
├── .tmp/                 # Temporary/intermediate files (gitignored)
├── .env                  # Environment variables (gitignored)
├── credentials.json      # Google OAuth credentials (gitignored)
└── token.json           # Google OAuth token (gitignored)
```

## Usage

The AI agent reads directives from `directives/`, makes decisions, and calls execution scripts from `execution/`.

1. Create or use existing directives in `directives/`
2. Chat with your AI agent about what you want to accomplish
3. Agent reads directives and executes appropriate scripts
4. System self-anneals: errors update tools and directives

## Key Principles

- **Check for tools first** - Always look in `execution/` before creating new scripts
- **Self-anneal** - Fix errors, update scripts, improve directives
- **Local files are temporary** - Deliverables live in cloud services (Google Sheets, etc.)
- **Everything in `.tmp/` can be deleted** - It's all regenerated as needed

## Adding New Capabilities

1. Write a directive in `directives/` describing the goal
2. Create execution script(s) in `execution/`
3. Agent will use them automatically based on directive instructions
