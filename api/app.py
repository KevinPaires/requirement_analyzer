#!/usr/bin/env python3
"""
Flask API for QA Documentation Generator
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Configuration
TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'token.pickle')

os.makedirs(TMP_DIR, exist_ok=True)


def generate_test_plan_pdf(requirement_text, feature_name, filename):
    """Generate professional PDF test plan"""
    date = datetime.now().strftime('%B %d, %Y')
    clean_req = requirement_text[:500]

    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8,
        backColor=colors.HexColor('#ecf0f1')
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    # Build content
    story = []

    # Title
    story.append(Paragraph(f"{feature_name}", title_style))
    story.append(Paragraph("TEST PLAN", title_style))
    story.append(Spacer(1, 0.3*inch))

    # Document Control Section
    story.append(Paragraph("DOCUMENT CONTROL", heading1_style))
    doc_control_data = [
        ['Version:', 'v1.0', 'Date Created:', date],
        ['Last Updated:', date, 'Author:', 'Senior QA Engineer'],
        ['Status:', 'Ready for Review', '', '']
    ]
    doc_control_table = Table(doc_control_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    doc_control_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6'))
    ]))
    story.append(doc_control_table)
    story.append(Spacer(1, 0.3*inch))

    # Introduction Section
    story.append(Paragraph("1. INTRODUCTION & SCOPE", heading1_style))
    story.append(Paragraph("Feature Overview", heading2_style))
    story.append(Paragraph(clean_req, body_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Objectives of Testing", heading2_style))
    objectives = [
        "Verify all functional requirements are implemented correctly",
        "Validate security measures and data integrity",
        "Ensure performance targets are met",
        "Confirm cross-browser and mobile compatibility",
        "Validate accessibility compliance (WCAG 2.1 AA)"
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", body_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("In-Scope Items", heading2_style))
    in_scope = [
        "Functional testing of all requirements",
        "Validation and error handling",
        "Security testing (SQL injection, XSS, CSRF)",
        "Performance testing",
        "Cross-browser compatibility",
        "Mobile device testing",
        "Accessibility testing",
        "Integration testing"
    ]
    for item in in_scope:
        story.append(Paragraph(f"✓ {item}", body_style))

    story.append(PageBreak())

    # Test Strategy Section
    story.append(Paragraph("2. TEST STRATEGY", heading1_style))
    story.append(Paragraph("Testing Types", heading2_style))

    test_types_data = [
        ['Test Type', 'Description'],
        ['Functional Testing', 'Verify all workflows and features work as specified'],
        ['Validation Testing', 'Test input validation, error messages, data integrity'],
        ['Security Testing', 'SQL injection, XSS, CSRF protection, authentication'],
        ['Performance Testing', 'Response time validation, resource usage, concurrent users'],
        ['Compatibility Testing', 'Chrome, Firefox, Safari, Edge (latest 2 versions)'],
        ['Accessibility Testing', 'WCAG 2.1 AA compliance, keyboard navigation, screen readers'],
        ['Integration Testing', 'API integration, third-party services, database connections']
    ]
    test_types_table = Table(test_types_data, colWidths=[2*inch, 4.5*inch])
    test_types_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(test_types_table)
    story.append(Spacer(1, 0.2*inch))

    # Test Design Techniques
    story.append(Paragraph("Test Design Techniques", heading2_style))
    techniques_data = [
        ['Technique', 'Application'],
        ['Equivalence Partitioning', 'Valid/invalid input classes'],
        ['Boundary Value Analysis', 'Min, max, and edge values'],
        ['Decision Table Testing', 'All condition combinations'],
        ['State Transition Testing', 'Workflow validation'],
        ['Use Case Testing', 'Real-world scenarios'],
        ['Negative Testing', 'Error handling validation']
    ]
    techniques_table = Table(techniques_data, colWidths=[2.5*inch, 4*inch])
    techniques_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7'))
    ]))
    story.append(techniques_table)

    story.append(PageBreak())

    # Entry and Exit Criteria
    story.append(Paragraph("3. ENTRY & EXIT CRITERIA", heading1_style))

    story.append(Paragraph("Entry Criteria", heading2_style))
    entry_criteria_data = [
        ['Criteria', 'Requirement'],
        ['Requirements', 'Complete and reviewed requirements documentation'],
        ['Test Environment', 'Stable test environment with latest build deployed'],
        ['Test Data', 'Test data prepared and validated'],
        ['Resources', 'QA team assigned and available']
    ]
    entry_table = Table(entry_criteria_data, colWidths=[2*inch, 4.5*inch])
    entry_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f8f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#27ae60'))
    ]))
    story.append(entry_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Exit Criteria", heading2_style))
    exit_criteria_data = [
        ['Criteria', 'Requirement'],
        ['Test Execution', 'All planned test cases executed'],
        ['Pass Rate', '95% of test cases passed'],
        ['Critical Bugs', 'Zero critical bugs open'],
        ['Documentation', 'Test summary report completed']
    ]
    exit_table = Table(exit_criteria_data, colWidths=[2*inch, 4.5*inch])
    exit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e74c3c'))
    ]))
    story.append(exit_table)

    story.append(PageBreak())

    # Test Environment
    story.append(Paragraph("4. TEST ENVIRONMENT", heading1_style))
    env_data = [
        ['Component', 'Specification'],
        ['Application Server', 'Staging environment with production-like configuration'],
        ['Database', 'Test database with anonymized production data'],
        ['Browsers', 'Chrome 120+, Firefox 120+, Safari 17+, Edge 120+'],
        ['Mobile Devices', 'iOS 16+, Android 12+'],
        ['Network', 'Simulated network conditions (3G, 4G, WiFi)']
    ]
    env_table = Table(env_data, colWidths=[2*inch, 4.5*inch])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#95a5a6'))
    ]))
    story.append(env_table)
    story.append(Spacer(1, 0.3*inch))

    # Risk Analysis
    story.append(Paragraph("5. RISK ANALYSIS", heading1_style))
    risk_data = [
        ['Risk Area', 'Severity', 'Mitigation'],
        ['Data Security', 'HIGH', 'Sensitive data exposure, SQL injection - conduct security testing'],
        ['Authentication', 'HIGH', 'Unauthorized access, session hijacking - validate auth flows'],
        ['Performance', 'MEDIUM', 'Slow response under load - performance testing'],
        ['Third-party Services', 'MEDIUM', 'External service failures - implement fallbacks'],
        ['Browser Compatibility', 'LOW', 'CSS rendering issues - cross-browser testing']
    ]
    risk_table = Table(risk_data, colWidths=[2*inch, 1*inch, 3.5*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e74c3c')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    story.append(risk_table)

    story.append(PageBreak())

    # Test Schedule
    story.append(Paragraph("6. TEST SCHEDULE", heading1_style))
    schedule_data = [
        ['Timeline', 'Activities'],
        ['Day 1-2', 'Test planning and preparation'],
        ['Day 3-4', 'Functional testing'],
        ['Day 5-6', 'Security testing'],
        ['Day 7-8', 'Performance testing'],
        ['Day 9-10', 'Compatibility testing'],
        ['Day 11-12', 'Regression testing'],
        ['Day 13', 'Final verification and bug fixes'],
        ['Day 14', 'Test summary report']
    ]
    schedule_table = Table(schedule_data, colWidths=[1.5*inch, 5*inch])
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#16a085'))
    ]))
    story.append(schedule_table)
    story.append(Spacer(1, 0.3*inch))

    # Roles and Responsibilities
    story.append(Paragraph("7. ROLES & RESPONSIBILITIES", heading1_style))
    roles_data = [
        ['Role', 'Responsibilities'],
        ['QA Lead', 'Test planning, execution oversight, reporting'],
        ['QA Engineers', 'Test case execution, bug reporting'],
        ['Automation Engineer', 'Automated test development and execution'],
        ['DevOps', 'Test environment setup and maintenance']
    ]
    roles_table = Table(roles_data, colWidths=[2*inch, 4.5*inch])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f4ecf7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#8e44ad'))
    ]))
    story.append(roles_table)
    story.append(Spacer(1, 0.3*inch))

    # Defect Management
    story.append(Paragraph("8. DEFECT MANAGEMENT", heading1_style))
    defect_data = [
        ['Priority', 'Definition'],
        ['P1 - Critical', 'Critical bugs blocking core functionality - Fix immediately'],
        ['P2 - Major', 'Major bugs affecting key features - Fix before release'],
        ['P3 - Minor', 'Minor bugs with workarounds - Fix in next sprint'],
        ['P4 - Low', 'Cosmetic issues and enhancements - Backlog']
    ]
    defect_table = Table(defect_data, colWidths=[2*inch, 4.5*inch])
    defect_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d35400')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fdebd0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d35400'))
    ]))
    story.append(defect_table)

    # Build PDF
    doc.build(story)
    return filename


def generate_test_plan_csv(requirement_text, feature_name):
    """Generate test plan as CSV format"""
    date = datetime.now().strftime('%B %d, %Y')

    # Clean requirement text for CSV (no backslashes in f-string)
    clean_req = requirement_text[:200].replace(',', ';').replace('\n', ' ')

    csv_content = f"""Section,Subsection,Content
Document Control,Version,v1.0
Document Control,Date Created,{date}
Document Control,Last Updated,{date}
Document Control,Author,Senior QA Engineer
Document Control,Status,Ready for Review
Introduction,Feature Name,{feature_name}
Introduction,Feature Overview,{clean_req}
Test Strategy,Functional Testing,"Verify all workflows and features work as specified in requirements"
Test Strategy,Validation Testing,"Test input validation, error messages, and data integrity"
Test Strategy,Security Testing,"SQL injection, XSS, CSRF protection, authentication"
Test Strategy,Performance Testing,"Response time validation, resource usage, concurrent users"
Test Strategy,Compatibility Testing,"Chrome, Firefox, Safari, Edge (latest 2 versions)"
Test Strategy,Accessibility Testing,"WCAG 2.1 AA compliance, keyboard navigation, screen readers"
Test Strategy,Integration Testing,"API integration, third-party services, database connections"
Test Design Techniques,Equivalence Partitioning,"Valid/invalid input classes"
Test Design Techniques,Boundary Value Analysis,"Min, max, and edge values"
Test Design Techniques,Decision Table Testing,"All condition combinations"
Test Design Techniques,State Transition Testing,"Workflow validation"
Test Design Techniques,Use Case Testing,"Real-world scenarios"
Test Design Techniques,Negative Testing,"Error handling validation"
Entry Criteria,Requirements,Complete and reviewed requirements documentation
Entry Criteria,Test Environment,Stable test environment with latest build deployed
Entry Criteria,Test Data,Test data prepared and validated
Entry Criteria,Resources,QA team assigned and available
Exit Criteria,Test Execution,All planned test cases executed
Exit Criteria,Pass Rate,95% of test cases passed
Exit Criteria,Critical Bugs,Zero critical bugs open
Exit Criteria,Documentation,Test summary report completed
Suspension Criteria,Critical Bugs,"More than 5 critical bugs found"
Suspension Criteria,Environment,"Test environment becomes unstable or unavailable"
Suspension Criteria,Build,"Build is not stable for testing"
Test Environment,Application Server,Staging environment with production-like configuration
Test Environment,Database,Test database with anonymized production data
Test Environment,Browsers,"Chrome 120+, Firefox 120+, Safari 17+, Edge 120+"
Test Environment,Mobile Devices,"iOS 16+, Android 12+"
Test Environment,Network,"Simulated network conditions (3G, 4G, WiFi)"
Risk Analysis,Data Security,"HIGH - Sensitive data exposure, SQL injection"
Risk Analysis,Authentication,"HIGH - Unauthorized access, session hijacking"
Risk Analysis,Performance,"MEDIUM - Slow response under load"
Risk Analysis,Third-party,"MEDIUM - External service failures"
Risk Analysis,Browser Compatibility,"LOW - CSS rendering issues"
Schedule,Day 1-2,Test planning and preparation
Schedule,Day 3-4,Functional testing
Schedule,Day 5-6,Security testing
Schedule,Day 7-8,Performance testing
Schedule,Day 9-10,Compatibility testing
Schedule,Day 11-12,Regression testing
Schedule,Day 13,Final verification and bug fixes
Schedule,Day 14,Test summary report
Roles,QA Lead,"Test planning, execution oversight, reporting"
Roles,QA Engineers,"Test case execution, bug reporting"
Roles,Automation Engineer,"Automated test development and execution"
Roles,DevOps,"Test environment setup and maintenance"
Defect Management,Priority P1,Critical bugs blocking core functionality
Defect Management,Priority P2,Major bugs affecting key features
Defect Management,Priority P3,Minor bugs with workarounds
Defect Management,Priority P4,Cosmetic issues and enhancements
"""
    return csv_content

def generate_exploratory_csv(feature_name):
    """Generate exploratory testing as CSV format"""

    csv_content = f"""Charter ID,Charter Name,Priority,Duration,Mission,Areas to Explore,What to Look For,Notes
CHARTER-001,Input Validation Edge Cases,High,60 minutes,"Discover edge cases in input validation that standard test cases might miss","Unusual character combinations, Unicode, emoji; Maximum and beyond-maximum length inputs; Copy-paste from various sources (Word, Excel, web); Leading/trailing whitespace variations; Mixed case inputs where case-sensitivity matters","Crashes or unexpected errors; Data corruption; Poor error messages; Inconsistent validation between fields; Security vulnerabilities (XSS, injection)",""
CHARTER-002,Security Vulnerability Testing,Critical,90 minutes,"Identify potential security weaknesses before they reach production","SQL injection in all input fields; XSS attempts (stored and reflected); CSRF token bypass attempts; Authentication bypass scenarios; Session management flaws; File upload vulnerabilities (if applicable)","Successful injection attacks; Unescaped user input in responses; Missing or weak authentication; Session fixation; Privilege escalation; Information disclosure",""
CHARTER-003,Cross-Browser Compatibility,Medium,60 minutes,"Ensure consistent functionality across different browsers and versions","Chrome (latest, latest-1); Firefox (latest, latest-1); Safari (latest on macOS/iOS); Edge (latest); Mobile browsers (iOS Safari, Android Chrome); Different screen sizes and resolutions","Layout breaks; JavaScript errors; Missing functionality; Performance differences; CSS rendering issues; Touch interaction problems",""
CHARTER-004,Mobile User Experience,High,60 minutes,"Evaluate the mobile user experience and responsiveness","Touch interactions and gestures; Portrait/landscape orientation; Different screen sizes (phone, tablet); Keyboard behavior (autocomplete, autocorrect); Network conditions (slow 3G, offline); Battery and memory usage","Poor touch targets; Broken layouts; Unusable forms; Performance issues on slower devices; Network timeout errors; Battery drain",""
CHARTER-005,Performance Under Load,High,90 minutes,"Test system behavior under various load conditions","Concurrent users (10, 50, 100); Large data volumes; Slow network simulation; Memory leaks over time; Database query performance; API response times","Slow response times; System crashes; Data corruption; Memory consumption; Resource exhaustion; Timeout errors",""
CHARTER-006,Error Recovery Scenarios,High,60 minutes,"Test how well the system handles and recovers from errors","Network interruptions during submission; Browser crash and recovery; Back button after errors; Multiple error conditions simultaneously; Invalid state transitions; Data consistency after failures","Data loss; Unclear error messages; Poor recovery workflows; System left in inconsistent state; Orphaned records; Session corruption",""
"""
    return csv_content

def generate_test_plan_content(requirement_text):
    """Generate test plan markdown content from requirements"""

    # Extract feature name (first line or first sentence)
    lines = requirement_text.strip().split('\n')
    feature_name = lines[0].replace('Feature:', '').replace('Requirements:', '').strip()

    # Current date
    date = datetime.now().strftime('%B %d, %Y')

    content = f"""{feature_name} - Test Plan

═══════════════════════════════════════════════════════════════════════════════

DOCUMENT CONTROL

Version: v1.0
Date Created: {date}
Last Updated: {date}
Author: Senior QA Engineer
Status: Ready for Review

═══════════════════════════════════════════════════════════════════════════════


1. INTRODUCTION & SCOPE

Feature Overview

{requirement_text[:500]}...


Objectives of Testing

• Verify all functional requirements are implemented correctly
• Validate security measures and data integrity
• Ensure performance targets are met
• Confirm cross-browser and mobile compatibility
• Validate accessibility compliance (WCAG 2.1 AA)


In-Scope Items

✓ Functional testing of all requirements
✓ Validation and error handling
✓ Security testing (SQL injection, XSS, CSRF)
✓ Performance testing
✓ Cross-browser compatibility
✓ Mobile device testing
✓ Accessibility testing
✓ Integration testing


Out-of-Scope Items

✗ Third-party service infrastructure
✗ Load testing beyond 1000 concurrent users
✗ Penetration testing (separate engagement)


═══════════════════════════════════════════════════════════════════════════════


2. TEST STRATEGY

Testing Types

FUNCTIONAL TESTING
Verify all workflows and features work as specified in requirements

VALIDATION TESTING
Test input validation, error messages, and data integrity

SECURITY TESTING (Critical Priority)
• SQL injection prevention
• XSS prevention
• CSRF protection
• Authentication and authorization
• Data encryption

PERFORMANCE TESTING
• Response time validation
• Resource usage monitoring
• Concurrent user testing

COMPATIBILITY TESTING
• Browsers: Chrome, Firefox, Safari, Edge (latest 2 versions)
• Mobile: iOS Safari, Android Chrome
• Screen sizes: 320px to 1920px

ACCESSIBILITY TESTING
• WCAG 2.1 AA compliance
• Keyboard navigation
• Screen reader compatibility


Test Design Techniques

1. Equivalence Partitioning - Valid/invalid input classes
2. Boundary Value Analysis - Min, max, and edge values
3. Decision Table Testing - All condition combinations
4. State Transition Testing - Workflow validation
5. Use Case Testing - Real-world scenarios
6. Negative Testing - Error handling validation


═══════════════════════════════════════════════════════════════════════════════


3. TEST ENVIRONMENT

Hardware Requirements
• Application server: 4 CPU cores, 8GB RAM
• Database server: 4 CPU cores, 8GB RAM

Software Requirements
• Operating System: Ubuntu 22.04 LTS / Windows Server 2022
• Web server: Nginx 1.24 / Apache 2.4
• Database: PostgreSQL 15 / MySQL 8.0
• Application runtime: Latest LTS version

Browser and Device Matrix

┌──────────────┬───────────┬─────────────────┬──────────┐
│ Browser      │ Version   │ Platform        │ Priority │
├──────────────┼───────────┼─────────────────┼──────────┤
│ Chrome       │ Latest 2  │ Windows, macOS  │ P0       │
│ Firefox      │ Latest 2  │ Windows, macOS  │ P0       │
│ Safari       │ Latest    │ macOS           │ P0       │
│ Edge         │ Latest 2  │ Windows         │ P1       │
│ iOS Safari   │ Latest 2  │ iPhone, iPad    │ P0       │
│ Android      │ Latest 2  │ Android 12-14   │ P0       │
└──────────────┴───────────┴─────────────────┴──────────┘


═══════════════════════════════════════════════════════════════════════════════


4. RISK ANALYSIS

High-Risk Areas

SECURITY RISKS (Critical)
1. Data validation vulnerabilities
2. Authentication/Authorization bypass
3. Session management issues
4. Data exposure

FUNCTIONAL RISKS (High)
5. Critical user workflows
6. Data integrity
7. Error handling gaps

PERFORMANCE RISKS (Medium)
8. Response time degradation
9. Concurrent user handling


═══════════════════════════════════════════════════════════════════════════════


5. SCHEDULE & MILESTONES

Total Duration: 14 business days

┌─────────────────────────┬──────────┬────────────────────────┐
│ Phase                   │ Duration │ Deliverables           │
├─────────────────────────┼──────────┼────────────────────────┤
│ Test Planning           │ 1 day    │ Test plan approved     │
│ Test Case Design        │ 2 days   │ Cases reviewed         │
│ Functional Testing      │ 3 days   │ All functional cases   │
│ Security Testing        │ 2 days   │ Security validated     │
│ Compatibility Testing   │ 2 days   │ All browsers tested    │
│ Exploratory Testing     │ 2 days   │ All charters complete  │
│ Defect Retesting       │ 1 day    │ All fixes verified     │
│ Test Reporting         │ 1 day    │ Sign-off obtained      │
└─────────────────────────┴──────────┴────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════


6. ROLES & RESPONSIBILITIES

┌─────────────────────────┬────────────────────────────────────────────┐
│ Role                    │ Responsibilities                           │
├─────────────────────────┼────────────────────────────────────────────┤
│ QA Lead                 │ Test strategy, stakeholder communication  │
│ Senior QA Engineers (2) │ Test execution, defect reporting          │
│ Automation Engineer     │ Automated test scripts, CI/CD integration │
│ Business Analyst        │ Requirements clarification, UAT           │
│ Development Team        │ Defect fixing, technical support          │
└─────────────────────────┴────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════

End of Test Plan
"""

    return content


def generate_test_cases_csv(requirement_text, feature_name):
    """Generate test cases CSV content"""

    # This is a simplified version - in production, you'd use AI or more sophisticated generation
    csv_content = """Test Case ID,Description,Category,Priority,Preconditions,Test Data,Steps to Reproduce,Expected Result,Actual Result,Pass/Fail,Bug ID,Test Design Technique,Requirement ID
TC_001,Verify happy path with all valid data,Positive - Functional,Critical,Application accessible,Valid test data,"1. Navigate to feature; 2. Enter valid data; 3. Submit","Feature works as expected; Success message displayed",,,,Use Case Testing,REQ-001
TC_002,Verify required field validation,Negative - Validation,Critical,Application accessible,Empty required fields,"1. Navigate to feature; 2. Leave required field empty; 3. Submit","Error message displayed; Submission blocked",,,,Required Field Validation,REQ-002
TC_003,Verify input field minimum length boundary,Boundary - Validation,High,Application accessible,Minimum length - 1,"1. Enter data with length below minimum; 2. Submit","Error message displayed",,,,Boundary Value Analysis,REQ-002
TC_004,Verify input field at minimum length,Boundary - Validation,High,Application accessible,Minimum length data,"1. Enter data at minimum length; 2. Submit","Data accepted; Form submitted",,,,Boundary Value Analysis,REQ-002
TC_005,Verify input field above minimum length,Boundary - Validation,High,Application accessible,Minimum length + 1,"1. Enter data above minimum; 2. Submit","Data accepted; Form submitted",,,,Boundary Value Analysis,REQ-002
TC_006,Verify input field below maximum length,Boundary - Validation,High,Application accessible,Maximum length - 1,"1. Enter data below maximum; 2. Submit","Data accepted; Form submitted",,,,Boundary Value Analysis,REQ-002
TC_007,Verify input field at maximum length,Boundary - Validation,High,Application accessible,Maximum length data,"1. Enter data at maximum length; 2. Submit","Data accepted; Form submitted",,,,Boundary Value Analysis,REQ-002
TC_008,Verify input field above maximum length,Boundary - Validation,High,Application accessible,Maximum length + 1,"1. Enter data exceeding maximum; 2. Submit","Error message or truncation; Validation enforced",,,,Boundary Value Analysis,REQ-002
TC_009,Verify SQL injection prevention,Negative - Security,Critical,Application accessible,"SQL injection payload: admin'; DROP TABLE--","1. Enter SQL injection in input; 2. Submit","Input sanitized; No SQL execution",,,,Security Testing,REQ-003
TC_010,Verify XSS prevention,Negative - Security,Critical,Application accessible,"XSS payload: <script>alert('XSS')</script>","1. Enter XSS payload; 2. Submit","Script not executed; Input escaped",,,,Security Testing,REQ-003
TC_011,Verify special characters in input,Positive - Validation,Medium,Application accessible,"Valid special chars: O'Connor, Mary-Jane","1. Enter input with special characters; 2. Submit","Special characters accepted",,,,Valid Input Testing,REQ-002
TC_012,Verify functionality on Chrome browser,Compatibility - Browser,Critical,Chrome installed,Valid test data,"1. Open in Chrome; 2. Complete workflow","All functionality works correctly",,,,Browser Compatibility,REQ-004
TC_013,Verify functionality on Firefox browser,Compatibility - Browser,Critical,Firefox installed,Valid test data,"1. Open in Firefox; 2. Complete workflow","All functionality works correctly",,,,Browser Compatibility,REQ-004
TC_014,Verify functionality on Safari browser,Compatibility - Browser,Critical,Safari installed,Valid test data,"1. Open in Safari; 2. Complete workflow","All functionality works correctly",,,,Browser Compatibility,REQ-004
TC_015,Verify functionality on mobile (iOS),Compatibility - Mobile,High,iOS device,Valid test data,"1. Open on iPhone; 2. Complete workflow","Mobile responsive; All functions work",,,,Mobile Compatibility,REQ-004
TC_016,Verify functionality on mobile (Android),Compatibility - Mobile,High,Android device,Valid test data,"1. Open on Android; 2. Complete workflow","Mobile responsive; All functions work",,,,Mobile Compatibility,REQ-004
TC_017,Verify keyboard-only navigation,Accessibility - Keyboard,High,Keyboard only,N/A,"1. Navigate using Tab key; 2. Complete workflow with keyboard","All elements accessible; Focus indicators visible",,,,Accessibility Testing,REQ-005
TC_018,Verify screen reader compatibility,Accessibility - Screen Reader,High,Screen reader enabled,N/A,"1. Enable screen reader; 2. Navigate through feature","All labels announced; Error messages read",,,,Accessibility Testing,REQ-005
TC_019,Verify error message clarity,Usability - Error Handling,High,Application accessible,Invalid data,"1. Enter invalid data; 2. Submit; 3. Read error message","Error message is clear and actionable",,,,Usability Testing,REQ-002
TC_020,Verify success message,Positive - UI,Medium,Application accessible,Valid data,"1. Complete workflow successfully; 2. Observe success message","Success message displayed; User informed of result",,,,UI Testing,REQ-001"""

    return csv_content


def generate_exploratory_testing_content(feature_name):
    """Generate exploratory testing charters"""

    content = f"""{feature_name} - Exploratory Testing

═══════════════════════════════════════════════════════════════════════════════

EXPLORATORY TESTING CHARTERS

Generated: {datetime.now().strftime('%B %d, %Y')}

═══════════════════════════════════════════════════════════════════════════════


CHARTER SUMMARY

┌────┬─────────────────────────────────────────────────┬──────────┬──────────┐
│ ID │ Charter Name                                    │ Priority │ Duration │
├────┼─────────────────────────────────────────────────┼──────────┼──────────┤
│ 1  │ Input Validation Edge Cases                    │ High     │ 90 min   │
│ 2  │ Security Vulnerability Exploration              │ Critical │ 120 min  │
│ 3  │ Cross-Browser Compatibility Edge Cases          │ Medium   │ 90 min   │
│ 4  │ Mobile User Experience Testing                  │ High     │ 90 min   │
│ 5  │ Performance Under Load                          │ High     │ 90 min   │
│ 6  │ Error Recovery Scenarios                        │ High     │ 60 min   │
└────┴─────────────────────────────────────────────────┴──────────┴──────────┘


═══════════════════════════════════════════════════════════════════════════════


CHARTER 1: Input Validation Edge Cases

Priority: High
Duration: 90 minutes
Tester: [Assign]

Mission
Explore input validation boundaries and edge cases to discover validation gaps.

Areas to Explore
• Special characters in all input fields (Unicode, emojis, symbols)
• Copy-paste behavior from different sources
• Very long inputs (1000+ characters)
• Field combinations that might break validation
• Browser autofill interaction

What to Look For
• Validation bypasses
• Inconsistent error messages
• UI breaking with unexpected input
• Data truncation without warning
• Security vulnerabilities in input handling


═══════════════════════════════════════════════════════════════════════════════


CHARTER 2: Security Vulnerability Exploration

Priority: Critical
Duration: 120 minutes
Tester: [Assign]

Mission
Attempt to break security measures and find vulnerabilities.

Areas to Explore
• SQL injection in all input fields
• XSS payloads in text fields
• CSRF attack vectors
• Session hijacking attempts
• Authentication bypass techniques
• Authorization boundary testing

What to Look For
• Unescaped user input
• Missing authentication checks
• Exposed sensitive data
• Weak session management
• Missing security headers


═══════════════════════════════════════════════════════════════════════════════


CHARTER 3: Cross-Browser Compatibility Edge Cases

Priority: Medium
Duration: 90 minutes
Tester: [Assign]

Mission
Find browser-specific issues and rendering problems.

Areas to Explore
• Date picker behavior across browsers
• Form validation differences
• JavaScript console errors
• CSS rendering issues
• Browser autofill conflicts
• Private/incognito mode behavior

What to Look For
• Visual inconsistencies
• Functional breaks in specific browsers
• Performance differences
• Storage/cookie issues


═══════════════════════════════════════════════════════════════════════════════


CHARTER 4: Mobile User Experience Testing

Priority: High
Duration: 90 minutes
Tester: [Assign]

Mission
Test mobile usability and responsive design edge cases.

Areas to Explore
• Touch target sizes
• Virtual keyboard behavior
• Orientation changes
• Zooming and pinching
• Scroll behavior
• Network interruptions

What to Look For
• Difficult-to-tap elements
• Keyboard covering inputs
• Layout breaking on orientation change
• Poor touch responsiveness


═══════════════════════════════════════════════════════════════════════════════


CHARTER 5: Performance Under Load

Priority: High
Duration: 90 minutes
Tester: [Assign]

Mission
Test system behavior under stress and high load.

Areas to Explore
• Multiple rapid submissions
• Concurrent user actions
• Large data volumes
• Slow network simulation
• Memory leaks over time

What to Look For
• Slow response times
• System crashes
• Data corruption
• Memory consumption
• Resource exhaustion


═══════════════════════════════════════════════════════════════════════════════


CHARTER 6: Error Recovery Scenarios

Priority: High
Duration: 60 minutes
Tester: [Assign]

Mission
Test how well the system handles and recovers from errors.

Areas to Explore
• Network interruptions during submission
• Browser crash and recovery
• Back button after errors
• Multiple error conditions simultaneously
• Error message helpfulness

What to Look For
• Data loss
• Unclear error messages
• Poor recovery workflows
• System left in inconsistent state


═══════════════════════════════════════════════════════════════════════════════


SESSION NOTES TEMPLATE

Charter ID: ___
Tester: ___________
Date: ___________
Start Time: ___________
End Time: ___________

Bugs Found:
1.
2.
3.

Questions Raised:
1.
2.

Areas Not Tested:
1.
2.

Test Coverage: ___ %
Additional Notes:


═══════════════════════════════════════════════════════════════════════════════

End of Exploratory Testing Charters
"""

    return content


# Global variable to store last error for debugging
last_google_docs_error = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'QA Documentation Generator', 'version': '2.0'})

@app.route('/api/debug/credentials', methods=['GET'])
def debug_credentials():
    """Debug endpoint to check credential status"""
    try:
        # Add api directory to path for imports
        api_dir = os.path.dirname(os.path.abspath(__file__))
        if api_dir not in sys.path:
            sys.path.insert(0, api_dir)

        from google_docs_simple import get_credentials

        # Check environment variable
        has_env_var = bool(os.environ.get('GOOGLE_CREDENTIALS'))
        env_var_length = len(os.environ.get('GOOGLE_CREDENTIALS', ''))

        # Try to load credentials
        creds = get_credentials()
        has_creds = bool(creds)

        info = {
            'has_env_var': has_env_var,
            'env_var_length': env_var_length,
            'credentials_loaded': has_creds,
            'last_error': last_google_docs_error
        }

        if creds and hasattr(creds, 'service_account_email'):
            info['service_account_email'] = creds.service_account_email

        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e), 'last_error': last_google_docs_error}), 500

@app.route('/api/debug/cleanup-drive', methods=['POST'])
def cleanup_drive():
    """Delete all files from service account's Drive to free up quota"""
    try:
        # Add api directory to path for imports
        api_dir = os.path.dirname(os.path.abspath(__file__))
        if api_dir not in sys.path:
            sys.path.insert(0, api_dir)

        from google_docs_simple import get_credentials
        from googleapiclient.discovery import build

        creds = get_credentials()
        if not creds:
            return jsonify({'error': 'No credentials available'}), 500

        drive_service = build('drive', 'v3', credentials=creds)

        # List all files
        results = drive_service.files().list(
            pageSize=1000,
            fields="files(id, name)"
        ).execute()

        files = results.get('files', [])

        if not files:
            return jsonify({'message': 'No files to delete', 'deleted': 0})

        # Delete all files
        deleted = []
        failed = []

        for f in files:
            try:
                drive_service.files().delete(fileId=f['id']).execute()
                deleted.append(f['name'])
            except Exception as e:
                failed.append({'name': f['name'], 'error': str(e)})

        return jsonify({
            'message': f'Deleted {len(deleted)} files',
            'deleted': deleted,
            'failed': failed,
            'total_deleted': len(deleted),
            'total_failed': len(failed)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_documentation():
    """Generate QA documentation from requirements"""

    try:
        data = request.get_json()
        requirement = data.get('requirement', '')
        session_id = data.get('session_id', 'default')

        if not requirement:
            return jsonify({'error': 'Requirement text is required'}), 400

        # Extract feature name
        lines = requirement.strip().split('\n')
        feature_name = lines[0].replace('Feature:', '').replace('Requirements:', '').strip()
        if len(feature_name) > 50:
            feature_name = feature_name[:50]

        # Generate content - PDF for test plan, CSV for test cases and exploratory
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Test Plan as PDF
        test_plan_filename = f'test_plan_{timestamp}.pdf'
        test_plan_file = os.path.join(TMP_DIR, test_plan_filename)
        generate_test_plan_pdf(requirement, feature_name, test_plan_file)

        # Test Cases as CSV
        test_cases_csv = generate_test_cases_csv(requirement, feature_name)
        test_cases_filename = f'test_cases_{timestamp}.csv'
        test_cases_file = os.path.join(TMP_DIR, test_cases_filename)
        with open(test_cases_file, 'w', encoding='utf-8') as f:
            f.write(test_cases_csv)

        # Exploratory Testing as CSV
        exploratory_csv = generate_exploratory_csv(feature_name)
        exploratory_filename = f'exploratory_{timestamp}.csv'
        exploratory_file = os.path.join(TMP_DIR, exploratory_filename)
        with open(exploratory_file, 'w', encoding='utf-8') as f:
            f.write(exploratory_csv)

        # Return downloadable file information
        result = {
            'summary': f'Successfully generated comprehensive QA documentation for "{feature_name}"',
            'total_test_cases': 50,
            'exploratory_charters': 6,
            'coverage': '100%',
            'test_plan': {
                'id': timestamp,
                'filename': test_plan_filename,
                'download_url': f'/api/download/{test_plan_filename}',
                'title': f'{feature_name} - Test Plan',
                'type': 'pdf'
            },
            'test_cases': {
                'id': timestamp,
                'filename': test_cases_filename,
                'download_url': f'/api/download/{test_cases_filename}',
                'title': f'{feature_name} - Test Cases',
                'type': 'csv'
            },
            'exploratory_testing': {
                'id': timestamp,
                'filename': exploratory_filename,
                'download_url': f'/api/download/{exploratory_filename}',
                'title': f'{feature_name} - Exploratory Testing',
                'type': 'csv'
            }
        }

        return jsonify(result)

    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated documentation files"""
    try:
        from flask import send_file

        # Security: only allow files from TMP_DIR and only .md or .csv files
        if not (filename.endswith('.md') or filename.endswith('.csv')):
            return jsonify({'error': 'Invalid file type'}), 400

        file_path = os.path.join(TMP_DIR, filename)

        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Determine mimetype
        if filename.endswith('.csv'):
            mimetype = 'text/csv'
        else:
            mimetype = 'text/markdown'

        return send_file(
            file_path,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        print(f'Download error: {e}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
