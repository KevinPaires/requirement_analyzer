# Directive: Generate Test Cases

## Goal
Create detailed, comprehensive test cases in Google Docs format with complete traceability and coverage of all test design techniques.

## Inputs
- **Requirement specification**: Feature description or user story
- **Test Plan**: Reference to the corresponding test plan
- **Requirement analysis**: Understanding of business rules, validations, user flows

## Process

### 1. Requirement Decomposition
Break down the requirement into testable components:
- **Inputs:** All fields, parameters, API endpoints
- **Outputs:** Expected responses, UI changes, data changes
- **Business rules:** Validations, calculations, workflows
- **Integration points:** External systems, databases, APIs
- **User roles:** Different permission levels and access patterns

### 2. Test Case Design Using Multiple Techniques

#### Equivalence Partitioning
Divide input domains into valid and invalid equivalence classes:
- **Valid classes:** Inputs that should be accepted
- **Invalid classes:** Inputs that should be rejected
- Test at least one value from each class

#### Boundary Value Analysis
For each input with boundaries, test:
- **Minimum boundary:** Smallest valid value
- **Just below minimum:** Invalid (min - 1)
- **Maximum boundary:** Largest valid value
- **Just above maximum:** Invalid (max + 1)
- **Typical value:** Mid-range valid value

Apply to:
- Numeric fields (age, quantity, price)
- Date fields (start date, end date, valid ranges)
- String length (username: 3-20 chars, description: 0-500 chars)
- File size (max upload: 5MB)

#### Positive Testing
Test normal, expected user behavior:
- Happy path scenarios
- Valid inputs with correct format
- Successful workflows from start to finish
- Typical user journeys

#### Negative Testing
Test abnormal inputs and error handling:
- **Invalid data types:** String where number expected, null values
- **Missing required fields:** Submit form with empty mandatory fields
- **Invalid formats:** Wrong email format, invalid phone number
- **SQL Injection attempts:** `'; DROP TABLE users; --`
- **XSS attempts:** `<script>alert('XSS')</script>`
- **Path traversal:** `../../etc/passwd`
- **Authorization violations:** Access resources without permission
- **Special characters:** `!@#$%^&*()`, Unicode characters, emojis
- **Concurrent operations:** Multiple users editing same resource
- **Rate limiting:** Excessive API requests

#### Decision Table Testing
For complex business rules with multiple conditions:
- Create table with all condition combinations
- Ensure all rules are covered
- Test each unique combination

Example: Discount calculation
| Premium Member | Order > $100 | First Purchase | Discount |
|----------------|--------------|----------------|----------|
| Yes            | Yes          | Yes            | 25%      |
| Yes            | Yes          | No             | 20%      |
| Yes            | No           | Yes            | 15%      |
| No             | Yes          | Yes            | 10%      |

#### State Transition Testing
For features with multiple states:
- Map all valid state transitions
- Test each valid transition
- Test invalid transitions (should be blocked)

Example: Order states
- Draft → Submitted → Processing → Shipped → Delivered
- Test: Draft → Delivered (invalid, should fail)

### 3. Test Case Documentation

Each test case must include:

**Test Case ID Format:** `TC_[FEATURE]_[NUMBER]`
- Example: `TC_LOGIN_001`, `TC_PAYMENT_045`

**Required Fields:**
1. **Test Case ID:** Unique identifier
2. **Description:** Clear, concise summary (e.g., "Verify login with valid credentials")
3. **Test Category:**
   - Positive/Negative
   - Functional/Integration/Regression
   - Security/Performance/Usability
4. **Preconditions:** What must be set up before test execution
   - Example: "User account exists in database with email: test@example.com"
5. **Test Data:** Specific values to use
   - Example: "Username: testuser@example.com, Password: Test@123!"
6. **Steps to Reproduce:** Numbered, detailed steps
   - Example:
     1. Navigate to https://app.example.com/login
     2. Enter username in "Email" field
     3. Enter password in "Password" field
     4. Click "Login" button
7. **Expected Result:** What should happen
   - Example: "User redirected to dashboard, welcome message displays with user's name"
8. **Actual Result:** [To be filled during execution]
9. **Pass/Fail:** [To be filled during execution]
10. **Bug Report ID:** [To be filled if defects found]
11. **Priority:** Critical/High/Medium/Low
12. **Test Design Technique:** Equivalence Partitioning/BVA/Decision Table/State Transition

### 4. Coverage Checklist

Ensure test cases cover:
- [ ] All functional requirements
- [ ] All input fields with valid/invalid/boundary values
- [ ] All buttons and links
- [ ] All user roles and permissions
- [ ] All error messages
- [ ] All success messages
- [ ] Form validation (client-side and server-side)
- [ ] Data persistence (save, retrieve, update, delete)
- [ ] Integration with external systems
- [ ] Browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsiveness
- [ ] Accessibility (keyboard navigation, screen reader)
- [ ] Security (authentication, authorization, input sanitization)
- [ ] Performance (page load time, API response time)

### 5. Test Case Grouping

Organize test cases into logical sections:
1. **Authentication Test Cases** (TC_AUTH_001 - TC_AUTH_050)
2. **User Management Test Cases** (TC_USER_001 - TC_USER_050)
3. **Payment Processing Test Cases** (TC_PAY_001 - TC_PAY_100)
4. **Reporting Test Cases** (TC_REPORT_001 - TC_REPORT_030)
5. **Integration Test Cases** (TC_INT_001 - TC_INT_050)
6. **Security Test Cases** (TC_SEC_001 - TC_SEC_050)

## Tools to Use
- `execution/create_google_doc.py` - Creates Google Doc with test case table
- `execution/generate_test_cases.py` - Generates test case data from requirement analysis
- `execution/format_test_table.py` - Formats test case table with proper styling

## Outputs
- **Google Docs URL** with formatted test case table
- **Traceability matrix:** Maps test cases to requirements
- **Local backup:** `.tmp/test_cases_YYYYMMDD_HHMMSS.json`

## Edge Cases
- **Complex workflows:** Break into multiple smaller test cases
- **Data-driven scenarios:** Create template test case with data variations table
- **API testing:** Include request/response examples, status codes, headers
- **File upload:** Test various file types, sizes, corrupted files
- **Multi-step wizards:** Test forward/backward navigation, data persistence
- **Real-time features:** Test WebSocket connections, push notifications
- **Offline functionality:** Test app behavior without network

## Example Test Case

| TC ID | Description | Category | Precondition | Test Data | Steps to Reproduce | Expected Result | Actual Result | Pass/Fail | Bug ID | Priority | Technique |
|-------|-------------|----------|--------------|-----------|-------------------|-----------------|---------------|-----------|---------|----------|-----------|
| TC_LOGIN_001 | Verify login with valid credentials | Positive - Functional | User account exists in system | Email: testuser@example.com<br>Password: Test@123! | 1. Navigate to login page<br>2. Enter email in "Email" field<br>3. Enter password in "Password" field<br>4. Click "Login" button | 1. User redirected to dashboard<br>2. Welcome message displays: "Welcome, Test User"<br>3. Session cookie created<br>4. Last login timestamp updated | | | | High | Valid Equivalence Class |
| TC_LOGIN_002 | Verify login with invalid email format | Negative - Validation | None | Email: invalidemail<br>Password: Test@123! | 1. Navigate to login page<br>2. Enter invalid email format<br>3. Enter valid password<br>4. Click "Login" button | 1. Error message displays: "Please enter a valid email address"<br>2. Login button remains enabled<br>3. User remains on login page<br>4. No backend request sent | | | | High | Invalid Equivalence Class |
| TC_LOGIN_003 | Verify login with empty password | Negative - Required Field | User account exists | Email: testuser@example.com<br>Password: [empty] | 1. Navigate to login page<br>2. Enter valid email<br>3. Leave password field empty<br>4. Click "Login" button | 1. Error message displays: "Password is required"<br>2. Password field highlighted in red<br>3. User remains on login page | | | | High | Missing Required Field |
| TC_LOGIN_004 | Verify SQL injection in login | Negative - Security | Database with user table exists | Email: admin' OR '1'='1<br>Password: anything | 1. Navigate to login page<br>2. Enter SQL injection string in email<br>3. Enter any password<br>4. Click "Login" button | 1. Login fails<br>2. Error message: "Invalid credentials"<br>3. No database error exposed<br>4. Attempt logged in security log | | | | Critical | Security Testing |
| TC_LOGIN_005 | Verify password minimum length boundary | Negative - BVA | None | Email: testuser@example.com<br>Password: Test@12 (7 chars) | 1. Navigate to login page<br>2. Enter valid email<br>3. Enter 7-character password (min is 8)<br>4. Click "Login" button | 1. Error message: "Password must be at least 8 characters"<br>2. Login does not proceed | | | | Medium | Boundary Value Analysis (below minimum) |

## Success Criteria
- All test design techniques applied appropriately
- Test cases are detailed enough for any tester to execute
- Traceability to requirements is clear
- Both positive and negative scenarios covered
- Security testing included
- Test data is realistic and specific
- Table is properly formatted and professional

## Update History
- 2026-01-27: Initial directive created
