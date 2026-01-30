# Directive: Generate Exploratory Testing Suggestions

## Goal
Create a comprehensive exploratory testing charter document in Google Docs that guides testers to uncover hidden defects, edge cases, and unexpected behaviors beyond scripted test cases.

## Inputs
- **Requirement specification**: Feature or system to be explored
- **Test Plan & Test Cases**: Understanding of what's already covered
- **System architecture**: Knowledge of components, integrations, data flows
- **Known risk areas**: Complex logic, recent changes, legacy integrations

## Process

### 1. Risk-Based Analysis
Identify high-risk areas that deserve exploratory focus:

#### Complexity Indicators
- Complex business logic with multiple conditions
- State-dependent behavior
- Calculations involving multiple variables
- Recursive or nested operations
- Caching mechanisms

#### Integration Risk Points
- Third-party API dependencies
- Database transactions
- Message queues
- File system operations
- External service calls
- Microservices communication

#### Recent Changes
- New features (most likely to have defects)
- Refactored code
- Performance optimizations
- Security patches
- Database schema changes

#### Historical Defect Patterns
- Areas with high bug density in the past
- Previously reported edge cases
- Customer-reported issues
- Production incidents

### 2. Session-Based Test Charter Design

Create focused exploration sessions, each with:

#### Charter Structure
**Charter ID:** `ETC_[AREA]_[NUMBER]`
Example: `ETC_AUTH_001`

**Charter Title:** Brief, descriptive name
Example: "Explore authentication edge cases under concurrent login attempts"

**Mission Statement:** Clear goal for the session
Example: "Investigate how the system handles multiple simultaneous login attempts from the same user account across different devices and browsers"

**Duration:** Realistic time box
- Short session: 60 minutes
- Standard session: 90 minutes
- Deep dive: 120 minutes

**Areas to Focus:** Specific features/components
Example:
- Login endpoint behavior
- Session management
- Token generation and validation
- Database connection pooling under load

**Risks to Investigate:** What could go wrong
Example:
- Race conditions in session creation
- Token collision
- Database deadlocks
- Memory leaks from unclosed sessions
- Session hijacking vulnerabilities

**Test Ideas:** Specific scenarios to try
Example:
1. Open 5 browser tabs, attempt login simultaneously
2. Login from desktop, then immediately from mobile
3. Login → Logout → Login rapidly 20 times
4. Login with correct password, then wrong password 10 times
5. Login halfway, kill browser, login again from different device

**Data Variations:** Edge data to use
Example:
- Very long usernames (500+ characters)
- Unicode characters: 测试用户, مستخدم, テスト
- Special characters: `admin'; DROP TABLE users;--`
- Case sensitivity: Admin vs admin vs ADMIN
- Leading/trailing spaces in credentials

### 3. Edge Case Scenario Categories

#### Unusual User Behaviors
- Clicking submit button multiple times rapidly
- Using browser back button during multi-step flows
- Refreshing page during processing
- Opening same form in multiple tabs
- Editing data while background save is happening
- Navigating away before operation completes
- Using keyboard shortcuts unexpectedly
- Right-click → "Open in new tab" on AJAX buttons

#### Data Edge Cases
- **Empty/Null:** Empty strings, null values, undefined
- **Size extremes:** 0 items, 1 item, max items, max+1 items
- **String lengths:** 0 chars, 1 char, max length, max+1 length
- **Special characters:** Emojis (😀), right-to-left (RTL) languages, zero-width characters
- **Number extremes:** -∞, -1, 0, 1, max int, max int + 1, decimals with many places
- **Date/time:** Year 2000, leap years, Feb 29, timezone boundaries, DST transitions, unix epoch, year 2038 problem
- **File uploads:** 0 bytes, 1 byte, max size, corrupted files, wrong extensions, executable files

#### Concurrent Operations
- Two users editing same record
- User A deletes while User B is viewing
- Batch operations overlapping with individual edits
- Background jobs running during user operations
- System maintenance during active usage
- Multiple browser tabs syncing data

#### Performance Degradation
- Large dataset handling (10,000+ records in dropdown)
- Slow network simulation (3G, 2G, offline)
- Low memory conditions
- High CPU load scenarios
- Database query timeouts
- API response delays (30+ seconds)

#### State Transition Edge Cases
- Skipping steps in wizard
- Going directly to step 3 of 5 via URL manipulation
- Invalid state transitions (Draft → Completed, skipping Approval)
- Reverting to previous state after partial completion
- State conflicts (two workflows trying to change same entity's state)

#### Security-Focused Exploration
- **Authentication bypass:** Direct URL access, session manipulation, token tampering
- **Authorization escalation:** Standard user accessing admin functions
- **Input sanitization:** XSS, SQL injection, NoSQL injection, XML injection
- **IDOR (Insecure Direct Object Reference):** Changing IDs in URL to access other users' data
- **CSRF (Cross-Site Request Forgery):** Submitting forms from external sites
- **Rate limiting:** API abuse, brute force attempts
- **Data exposure:** Sensitive data in logs, error messages, API responses
- **File upload vulnerabilities:** PHP shells, malicious PDFs, XXE attacks

### 4. Persona-Based Exploration

Test from different user perspectives:

#### Novice User
- Doesn't read instructions
- Tries unusual input methods
- Gets confused by technical jargon
- Makes mistakes frequently
- Needs clear error messages

#### Power User
- Uses keyboard shortcuts extensively
- Expects efficiency and speed
- Tries bulk operations
- Wants customization options
- Frustrated by limitations

#### Accessibility User
- Navigates with keyboard only (Tab, Enter, Space)
- Uses screen reader (NVDA, JAWS, VoiceOver)
- Needs proper ARIA labels
- Requires sufficient color contrast
- Needs focus indicators

#### Mobile User
- Touch interactions (tap, swipe, pinch-to-zoom)
- Portrait and landscape orientations
- Offline and poor connectivity
- Small screen real estate
- Different input methods (voice, camera)

#### Malicious User
- Actively trying to break the system
- Automated scripts and bots
- SQL injection, XSS attempts
- Reverse engineering API calls
- Bypassing client-side validations

### 5. Integration & Compatibility Exploration

#### Third-Party Service Scenarios
- API returns 500 error
- API timeout after 30 seconds
- API returns malformed data
- API rate limit exceeded
- OAuth provider unavailable
- Payment gateway failure mid-transaction
- Email service down (can user still complete action?)

#### Browser/Device Matrix
- **Browsers:** Chrome, Firefox, Safari, Edge (latest and previous version)
- **Mobile devices:** iOS 16, 17; Android 12, 13, 14
- **Screen sizes:** 320px (iPhone SE), 768px (iPad), 1920px (desktop), 4K displays
- **Browser features disabled:** Cookies off, JavaScript off, local storage disabled

#### Network Conditions
- Fast 3G (750ms latency)
- Slow 3G (2000ms latency)
- Offline mode
- Intermittent connectivity (WiFi drops)
- High packet loss

## Tools to Use
- `execution/create_google_doc.py` - Creates exploratory testing charter document
- `execution/format_charter.py` - Formats charter with proper sections and styling

## Outputs
- **Google Docs URL** with exploratory testing charters
- **Session notes template:** For testers to record findings during sessions
- **Local backup:** `.tmp/exploratory_charters_YYYYMMDD_HHMMSS.json`

## Example Charter

---

### Charter: ETC_PAYMENT_001
**Title:** Explore payment processing under adverse network conditions

**Mission:**
Investigate how the payment flow behaves when network conditions are poor, intermittent, or when external payment gateway experiences failures.

**Duration:** 90 minutes

**Areas to Focus:**
- Payment form submission
- Payment gateway integration
- Transaction status updates
- Error handling and retry logic
- User feedback mechanisms

**Risks to Investigate:**
- Double-charging due to retry logic
- Incomplete transactions leaving system in inconsistent state
- Sensitive data exposure in error messages
- User confusion when payment status is unclear
- Timeout handling

**Test Ideas:**
1. Submit payment, kill network before response received
2. Submit payment, slow network to 3G, observe timeout behavior
3. Submit payment, payment gateway returns 500 error
4. Submit payment twice rapidly (double-click button)
5. Submit payment, gateway timeout after 25 seconds
6. Submit payment, close browser tab before confirmation
7. Submit payment, navigate to different page during processing
8. Submit payment with expired credit card (soft failure)
9. Submit payment with invalid CVV (hard failure)
10. Submit payment, gateway returns success but transaction ID is null

**Data Variations:**
- Payment amounts: $0.01, $0.99, $1.00, $999.99, $1000.00, $9999.99, $10000.00
- Credit card numbers: Valid Visa, Mastercard, Amex, Discover, invalid Luhn check
- Expiry dates: Current month, next month, last month (expired), far future (2050)
- CVV: 123, 000, 999, empty, 12 (too short), 1234 (too long)
- Billing addresses: US, Canada, UK, Australia, addresses with Unicode characters
- Special characters in name: O'Brien, José García, 李明

**Expected Findings:**
- Identify weak spots in error handling
- Discover race conditions in payment processing
- Uncover data consistency issues
- Find UX problems in error messaging
- Reveal security concerns in data handling

---

## Success Criteria
- Charters cover high-risk areas not thoroughly tested in scripted tests
- Each charter has clear mission and specific test ideas
- Security considerations are prominent
- Realistic edge cases based on production failures are included
- Charters are actionable and time-boxed
- Persona-based exploration ensures diverse user perspectives

## Update History
- 2026-01-27: Initial directive created
