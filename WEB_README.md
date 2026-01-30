# QA Documentation Generator 📋

> AI-Powered Test Documentation Generator with 20+ Years of QA Best Practices

Transform your feature requirements into comprehensive, enterprise-grade QA documentation in seconds.

![QA Generator](https://img.shields.io/badge/QA-Documentation-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **📄 Test Plan Generation**: Comprehensive test strategy, scope, risks, and 14-day schedule
- **✅ Test Cases with BVA**: 50-100 detailed test cases including boundary value analysis
- **🔍 Exploratory Testing**: 6+ session-based testing charters for edge cases
- **🎨 Modern UI**: ChatGPT-style interface, clean and intuitive
- **☁️ Google Docs Integration**: Automatically creates shareable Google Docs and Sheets
- **🚀 Instant Results**: Get complete QA documentation in seconds

## 🚀 Live Demo

**Frontend**: [https://kevinpaires.github.io/requirement_analyzer](https://kevinpaires.github.io/requirement_analyzer)

**API**: Deploy your own backend (see deployment instructions below)

## 🏗️ Architecture

```
├── web/                 # Frontend (HTML/CSS/JS)
│   ├── index.html      # Main interface
│   ├── styles.css      # Modern styling
│   └── script.js       # Frontend logic
│
├── api/                 # Backend (Flask)
│   ├── app.py          # Main API server
│   └── requirements.txt
│
├── execution/           # QA Document Generators
│   ├── create_google_doc.py
│   ├── create_google_sheet.py
│   └── replace_doc_content.py
│
└── directives/          # Test generation templates
    ├── generate_test_plan.md
    ├── generate_test_cases.md
    └── generate_exploratory_tests.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- Google Cloud Project with Docs/Sheets API enabled
- Google OAuth credentials

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kevinpaires/requirement_analyzer.git
   cd requirement_analyzer
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r api/requirements.txt
   ```

3. **Configure Google API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google Docs API and Google Sheets API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download credentials and save as `credentials.json` in root directory

4. **Run the backend**
   ```bash
   cd api
   python app.py
   ```
   Backend will run on `http://localhost:5000`

5. **Open the frontend**
   ```bash
   cd web
   # Open index.html in browser, or use a local server:
   python -m http.server 8000
   ```
   Frontend will be available at `http://localhost:8000`

## 🌐 Deployment

### Deploy Frontend to GitHub Pages

1. **Enable GitHub Pages**
   - Go to your repository settings
   - Navigate to "Pages"
   - Source: Deploy from a branch
   - Branch: `main`, Folder: `/web`

2. **The GitHub Action will automatically deploy**
   - See `.github/workflows/deploy.yml`
   - Your site will be live at `https://yourusername.github.io/requirement_analyzer`

### Deploy Backend to Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-qa-generator-api
   ```

3. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Update frontend API URL**
   Edit `web/script.js` and change `API_BASE_URL`:
   ```javascript
   const API_BASE_URL = 'https://your-qa-generator-api.herokuapp.com/api';
   ```

### Alternative: Deploy Backend to Railway/Render

Both Railway and Render offer easy Python app deployment with automatic HTTPS.

## 📝 Usage

### Via Web Interface

1. Navigate to the website
2. Paste your feature requirements
3. Click "Generate" or press Enter
4. Wait 10-30 seconds
5. Click the links to open your Google Docs

### Example Requirements Format

```
Password Reset Feature

Business Requirements:
- Users should be able to reset forgotten passwords
- Reset link should expire after 15 minutes
- Process should be secure and user-friendly

Functional Requirements:
1. Request Reset:
   - User enters email address
   - System sends reset link

2. Reset Password:
   - User clicks link from email
   - User enters new password (8+ chars, 1 uppercase, 1 number)
   - System validates and updates password

3. Security:
   - Single-use tokens
   - All sessions invalidated after reset
```

### API Usage

**Endpoint**: `POST /api/generate`

**Request**:
```json
{
  "requirement": "Your feature requirements here...",
  "session_id": "optional_session_id"
}
```

**Response**:
```json
{
  "summary": "Successfully generated documentation",
  "total_test_cases": 50,
  "exploratory_charters": 6,
  "coverage": "100%",
  "test_plan": {
    "id": "doc_id",
    "url": "https://docs.google.com/document/d/...",
    "title": "Feature - Test Plan"
  },
  "test_cases": {
    "id": "sheet_id",
    "url": "https://docs.google.com/spreadsheets/d/...",
    "title": "Feature - Test Cases"
  },
  "exploratory_testing": {
    "id": "doc_id",
    "url": "https://docs.google.com/document/d/...",
    "title": "Feature - Exploratory Testing"
  }
}
```

## 🧪 What Gets Generated

### 1. Test Plan (20-25 pages)
- Document control and version history
- Introduction and scope definition
- Test strategy (7 testing types)
- Test design techniques
- Entry/exit/suspension criteria
- Test environment specifications
- Risk analysis with mitigation strategies
- 14-day test schedule
- Roles and responsibilities
- Defect management process

### 2. Test Cases (50-100 cases)
- Positive functional testing
- Negative validation testing
- Boundary value analysis (min, max, edge values)
- Security testing (SQL injection, XSS, CSRF)
- Performance testing
- Cross-browser compatibility
- Mobile device testing
- Accessibility testing
- **13-column format**: ID, Description, Category, Priority, Preconditions, Test Data, Steps, Expected Result, Actual Result, Pass/Fail, Bug ID, Technique, Requirement ID

### 3. Exploratory Testing Charters (6+ charters)
- Input validation edge cases
- Security vulnerability exploration
- Cross-browser compatibility issues
- Mobile user experience testing
- Performance under load
- Error recovery scenarios
- Session notes template

## 🎯 Test Coverage

- **100% Requirements Coverage**: Every requirement mapped to test cases
- **Boundary Value Analysis**: Min-1, Min, Min+1, Max-1, Max, Max+1 for all fields
- **Security**: OWASP Top 10 coverage
- **Accessibility**: WCAG 2.1 AA compliance testing
- **Compatibility**: Chrome, Firefox, Safari, Edge, iOS, Android

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with 20+ years of QA best practices
- Inspired by ChatGPT's clean interface
- Google Docs/Sheets API for document generation
- Flask for backend API

## 📧 Contact

Kevin Paires - [@kevinpaires](https://github.com/kevinpaires)

Project Link: [https://github.com/kevinpaires/requirement_analyzer](https://github.com/kevinpaires/requirement_analyzer)

---

⭐️ If you find this project useful, please give it a star!
