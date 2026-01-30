# Directive: Generate Test Plan

## Goal
Create a comprehensive, professional Test Plan document in Google Docs for a given requirement or feature specification.

## Inputs
- **Requirement specification**: User-provided feature description or requirement document
- **Requirement analysis**: Platform, user roles, integrations, performance needs, security requirements, compliance needs
- **Project context**: Project name, version, timeline (if provided)

## Process

### 1. Requirement Analysis
Before generating the test plan, gather the following information:
- Target platform (web, mobile, API, desktop)
- User roles and permissions involved
- Integration points with other systems
- Performance expectations
- Security requirements
- Compliance needs (GDPR, HIPAA, SOC2, etc.)

If any critical information is missing, ask the user for clarification.

### 2. Generate Test Plan Content
The test plan must include these sections:

#### Document Control
- Document version (start with v1.0)
- Date created (current date)
- Last updated (current date)
- Author (QA Team or specific name if provided)

#### Introduction & Scope
- Feature/requirement overview (clear summary of what's being tested)
- Objectives of testing (what quality goals we're achieving)
- In-scope items (what will be tested)
- Out-of-scope items (what won't be tested in this phase)

#### Test Strategy
- **Testing types to perform:**
  - Functional testing
  - Integration testing
  - Regression testing
  - Performance testing (if applicable)
  - Security testing
  - Usability testing
  - Accessibility testing (WCAG 2.1 AA compliance)

- **Test design techniques:**
  - Equivalence Partitioning
  - Boundary Value Analysis
  - Decision Table Testing
  - State Transition Testing
  - Use Case Testing

- **Entry criteria:** What must be true before testing starts
- **Exit criteria:** What must be achieved to consider testing complete
- **Suspension criteria:** Under what conditions testing will pause
- **Resumption criteria:** What's needed to restart suspended testing

#### Test Environment
- **Hardware requirements:** Servers, devices, network setup
- **Software requirements:** OS versions, browsers, databases, third-party tools
- **Test data requirements:** Production-like data, anonymized data needs, volume
- **Browser/device matrix:** (if web/mobile testing)
  - Desktop browsers: Chrome (latest 2 versions), Firefox (latest 2), Safari (latest), Edge (latest)
  - Mobile devices: iOS (latest 2 versions), Android (latest 3 versions)
  - Screen sizes: Mobile (320px-767px), Tablet (768px-1024px), Desktop (1025px+)

#### Risk Analysis
- **High-risk areas identified:**
  - Complex business logic
  - Integration points with external systems
  - Security-sensitive operations (authentication, authorization, payment)
  - Data migration or transformation
  - Performance bottlenecks

- **Mitigation strategies:**
  - Increased test coverage for high-risk areas
  - Automated regression testing
  - Performance baseline establishment
  - Security penetration testing
  - Staged rollout approach

#### Test Deliverables
- Test Plan document (this document)
- Test Cases document with traceability matrix
- Exploratory Testing Charters
- Test execution reports (daily/weekly)
- Defect reports with severity classification
- Test summary report
- Sign-off documentation

#### Schedule & Milestones
Create a realistic timeline with these phases:
- **Test planning:** X days
- **Test design:** X days
- **Test environment setup:** X days
- **Test execution - Functional:** X days
- **Test execution - Integration:** X days
- **Test execution - Regression:** X days
- **Test execution - Performance:** X days (if applicable)
- **Defect retesting:** X days
- **Test reporting & closure:** X days

#### Roles & Responsibilities
- **QA Lead:** Test strategy, team coordination, stakeholder communication
- **QA Engineers:** Test case design, test execution, defect reporting
- **Automation Engineers:** Test automation framework, automated test development
- **Performance Engineers:** Performance test design, load testing execution
- **Security Testers:** Security vulnerability assessment, penetration testing
- **DevOps:** Test environment provisioning, CI/CD pipeline integration

## Tools to Use
- `execution/create_google_doc.py` - Creates the Google Doc with formatted content
- `execution/format_test_plan.py` - Applies professional formatting (headers, tables, styles)

## Outputs
- **Google Docs URL** for the Test Plan
- **Local backup** in `.tmp/test_plan_YYYYMMDD_HHMMSS.json` (structured data for reference)

## Edge Cases
- **Missing requirement details:** Explicitly note assumptions and areas needing clarification
- **Regulatory compliance:** If healthcare/finance/PII involved, add specific compliance testing sections
- **Legacy system integration:** Include data format validation and backward compatibility testing
- **Multi-region deployment:** Add localization, timezone, and internationalization considerations
- **Mobile-first requirement:** Prioritize mobile testing, include offline functionality testing

## Example Usage
```
User: "I need a test plan for a login feature with email/password and OAuth (Google, Facebook)"

Agent workflow:
1. Analyze requirement (authentication feature, web platform)
2. Ask clarifying questions about MFA, password policies, session management
3. Call execution/create_google_doc.py with test plan structure
4. Return Google Docs link to user
```

## Success Criteria
- Test plan covers all functional and non-functional aspects
- Risk areas clearly identified with mitigation
- Timeline is realistic and accounts for defect fixing cycles
- Document is professional, print-ready, and stakeholder-friendly
- All testing types relevant to the requirement are included

## Update History
- 2026-01-27: Initial directive created
