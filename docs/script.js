// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5000/api'
    : 'https://web-production-f4c75.up.railway.app/api';

// DOM Elements
const requirementInput = document.getElementById('requirementInput');
const sendBtn = document.getElementById('sendBtn');
const messagesContainer = document.getElementById('messages');
const welcomeScreen = document.getElementById('welcomeScreen');
const newChatBtn = document.getElementById('newChatBtn');
const historyList = document.getElementById('historyList');

// State
let currentSessionId = generateSessionId();
let isGenerating = false;

// Example requirements
const examples = {
    'password-reset': `Password Reset Feature

Business Requirements:
- Users who forget their password should be able to reset it via email
- The reset process should be secure and time-limited
- Users should receive confirmation after successful password reset

Functional Requirements:
1. Request Password Reset:
   - User enters registered email address
   - System sends reset link to email
   - Link expires after 15 minutes

2. Reset Password:
   - User clicks link from email
   - User enters new password (8+ characters, 1 uppercase, 1 number)
   - User confirms new password
   - System validates and updates password

3. Security:
   - Token should be single-use
   - Old password should be invalidated
   - All active sessions should be terminated`,

    'login': `Login Authentication Feature

Business Requirements:
- Users should be able to securely log into the system
- Login should work on web and mobile platforms
- Failed login attempts should be tracked

Functional Requirements:
1. Login Form:
   - Email field (required, format validation)
   - Password field (required, masked)
   - "Remember me" checkbox (optional)
   - "Forgot password?" link
   - "Login" button

2. Validation:
   - Email format validation
   - Password minimum length: 8 characters
   - Show error messages for invalid credentials

3. Success Flow:
   - Redirect to dashboard after successful login
   - Create session token
   - Set session cookie if "Remember me" is checked

4. Security:
   - Lock account after 5 failed attempts
   - Implement CAPTCHA after 3 failed attempts
   - Log all login attempts with IP address`,

    'checkout': `E-commerce Checkout Feature

Business Requirements:
- Users should be able to complete purchases securely
- Support multiple payment methods
- Provide order confirmation

Functional Requirements:
1. Checkout Steps:
   - Step 1: Shipping Information (Name, Address, Phone)
   - Step 2: Payment Method (Credit Card, PayPal, Apple Pay)
   - Step 3: Review Order
   - Step 4: Confirm and Pay

2. Shipping Form:
   - Full Name (required)
   - Address (required)
   - City, State, ZIP (required)
   - Phone Number (required, format validation)
   - Save address for future orders (checkbox)

3. Payment:
   - Credit card number (16 digits)
   - Expiry date (MM/YY format)
   - CVV (3-4 digits)
   - Billing address same as shipping (checkbox)

4. Order Review:
   - Show cart items with quantities
   - Display shipping address
   - Show payment method (last 4 digits)
   - Calculate total with tax and shipping

5. Success:
   - Generate unique order number
   - Send confirmation email
   - Redirect to order tracking page`
};

// Initialize
function init() {
    loadHistory();

    // Auto-resize textarea
    requirementInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';

        // Enable/disable send button
        sendBtn.disabled = this.value.trim() === '';
    });

    // Send on Enter (but allow Shift+Enter for new line)
    requirementInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                handleSubmit();
            }
        }
    });

    // Send button click
    sendBtn.addEventListener('click', handleSubmit);

    // New chat button
    newChatBtn.addEventListener('click', startNewChat);

    // Example buttons
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const exampleKey = this.dataset.example;
            requirementInput.value = examples[exampleKey];
            requirementInput.dispatchEvent(new Event('input'));
            handleSubmit();
        });
    });
}

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Start new chat
function startNewChat() {
    currentSessionId = generateSessionId();
    messagesContainer.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    requirementInput.value = '';
    requirementInput.style.height = 'auto';
    sendBtn.disabled = true;
}

// Handle submit
async function handleSubmit() {
    if (isGenerating) return;

    const requirement = requirementInput.value.trim();
    if (!requirement) return;

    // Hide welcome screen
    welcomeScreen.style.display = 'none';

    // Add user message
    addMessage('user', requirement);

    // Clear input
    requirementInput.value = '';
    requirementInput.style.height = 'auto';
    sendBtn.disabled = true;

    // Show loading
    const loadingId = addLoadingMessage();

    // Set generating state
    isGenerating = true;

    try {
        let data;

        try {
            // Try to call the backend API first
            const response = await fetch(`${API_BASE_URL}/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    requirement: requirement,
                    session_id: currentSessionId
                })
            });

            if (!response.ok) {
                throw new Error('Backend not available');
            }

            data = await response.json();

        } catch (apiError) {
            // Fallback to demo mode if API fails
            console.log('API not available, using demo mode:', apiError);

            await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate delay

            const featureName = requirement.split('\n')[0].substring(0, 50);
            data = {
                summary: `Successfully generated comprehensive QA documentation for "${featureName}"`,
                total_test_cases: 85,
                exploratory_charters: 6,
                coverage: '100%',
                test_plan: {
                    url: 'https://docs.google.com/document/d/demo',
                    title: `${featureName} - Test Plan`
                },
                test_cases: {
                    url: 'https://docs.google.com/spreadsheets/d/demo',
                    title: `${featureName} - Test Cases`
                },
                exploratory_testing: {
                    url: 'https://docs.google.com/document/d/demo',
                    title: `${featureName} - Exploratory Testing`
                }
            };

            // Add demo mode notice
            removeLoadingMessage(loadingId);
            addMessage('assistant', '⚠️ Demo Mode: Backend API is not deployed. Showing preview with sample data.\n\nTo generate real Google Docs, deploy the backend (see DEPLOYMENT_GUIDE.md).');
        }

        // Remove loading message and show results
        removeLoadingMessage(loadingId);
        addResultMessage(data);
        saveToHistory(requirement, data);

    } catch (error) {
        console.error('Error:', error);
        removeLoadingMessage(loadingId);
        addMessage('assistant', 'Sorry, there was an error generating the documentation. Please try again.\n\nIf the backend is not deployed yet, the app will run in demo mode.');
    } finally {
        isGenerating = false;
    }
}

// Add message
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const avatar = role === 'user' ? '👤' : '🤖';
    const name = role === 'user' ? 'You' : 'QA Generator';

    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar ${role}">${avatar}</div>
            <div class="message-name">${name}</div>
        </div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(content)}</div>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    return messageDiv;
}

// Add loading message
function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    const loadingId = 'loading_' + Date.now();
    messageDiv.id = loadingId;

    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar assistant">🤖</div>
            <div class="message-name">QA Generator</div>
        </div>
        <div class="message-content">
            <div class="loading">
                <span>Generating documentation</span>
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    return loadingId;
}

// Remove loading message
function removeLoadingMessage(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Add result message
function addResultMessage(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const summary = data.summary || 'Documentation generated successfully';
    const testPlan = data.test_plan || {};
    const testCases = data.test_cases || {};
    const exploratory = data.exploratory_testing || {};

    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar assistant">🤖</div>
            <div class="message-name">QA Generator</div>
        </div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(summary)}</div>

            <div class="result-card">
                <div class="result-header">
                    <h3 class="result-title">✅ Documentation Generated</h3>
                </div>

                <div class="result-stats">
                    <div class="stat-item">
                        <div class="stat-value">${data.total_test_cases || 0}</div>
                        <div class="stat-label">Test Cases</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${data.exploratory_charters || 0}</div>
                        <div class="stat-label">Exploratory Charters</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${data.coverage || '100%'}</div>
                        <div class="stat-label">Coverage</div>
                    </div>
                </div>

                <div class="result-links">
                    ${testPlan.download_url ? `
                    <a href="${API_BASE_URL.replace('/api', '')}${testPlan.download_url}" download="${testPlan.filename}" class="doc-link">
                        <div class="doc-link-content">
                            <div class="doc-icon">📄</div>
                            <div class="doc-info">
                                <h4>Test Plan</h4>
                                <p>Comprehensive test strategy, scope, and schedule (.csv)</p>
                            </div>
                        </div>
                        <div class="doc-arrow">⬇</div>
                    </a>
                    ` : ''}

                    ${testCases.download_url ? `
                    <a href="${API_BASE_URL.replace('/api', '')}${testCases.download_url}" download="${testCases.filename}" class="doc-link">
                        <div class="doc-link-content">
                            <div class="doc-icon">✅</div>
                            <div class="doc-info">
                                <h4>Test Cases (${data.total_test_cases || 0} cases)</h4>
                                <p>Detailed test cases with boundary value analysis (.csv)</p>
                            </div>
                        </div>
                        <div class="doc-arrow">⬇</div>
                    </a>
                    ` : ''}

                    ${exploratory.download_url ? `
                    <a href="${API_BASE_URL.replace('/api', '')}${exploratory.download_url}" download="${exploratory.filename}" class="doc-link">
                        <div class="doc-link-content">
                            <div class="doc-icon">🔍</div>
                            <div class="doc-info">
                                <h4>Exploratory Testing (${data.exploratory_charters || 0} charters)</h4>
                                <p>Session-based testing charters for edge cases (.csv)</p>
                            </div>
                        </div>
                        <div class="doc-arrow">⬇</div>
                    </a>
                    ` : ''}
                </div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
}

// Save to history
function saveToHistory(requirement, data) {
    const history = getHistory();

    const historyItem = {
        id: currentSessionId,
        requirement: requirement.substring(0, 100),
        timestamp: Date.now(),
        data: data
    };

    history.unshift(historyItem);

    // Keep only last 10 items
    if (history.length > 10) {
        history.pop();
    }

    localStorage.setItem('qa_generator_history', JSON.stringify(history));
    loadHistory();
}

// Load history
function loadHistory() {
    const history = getHistory();
    historyList.innerHTML = '';

    if (history.length === 0) {
        historyList.innerHTML = '<div class="history-item" style="color: rgba(255,255,255,0.5); cursor: default;">No recent generations</div>';
        return;
    }

    history.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';

        const textSpan = document.createElement('span');
        textSpan.textContent = item.requirement;
        textSpan.title = item.requirement;
        textSpan.style.flex = '1';
        textSpan.style.cursor = 'pointer';

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '×';
        deleteBtn.className = 'delete-history-btn';
        deleteBtn.title = 'Delete';
        deleteBtn.style.cssText = 'margin-left: 8px; padding: 2px 8px; background: rgba(255,255,255,0.1); border: none; border-radius: 4px; color: white; cursor: pointer; font-size: 18px; opacity: 0.7; transition: opacity 0.2s;';

        deleteBtn.addEventListener('mouseenter', () => {
            deleteBtn.style.opacity = '1';
            deleteBtn.style.background = 'rgba(255,255,255,0.2)';
        });

        deleteBtn.addEventListener('mouseleave', () => {
            deleteBtn.style.opacity = '0.7';
            deleteBtn.style.background = 'rgba(255,255,255,0.1)';
        });

        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteHistoryItem(index);
        });

        textSpan.addEventListener('click', () => {
            loadHistoryItem(item);
        });

        historyItem.appendChild(textSpan);
        historyItem.appendChild(deleteBtn);
        historyList.appendChild(historyItem);
    });
}

// Get history from localStorage
function getHistory() {
    const historyStr = localStorage.getItem('qa_generator_history');
    return historyStr ? JSON.parse(historyStr) : [];
}

// Load history item
function loadHistoryItem(item) {
    welcomeScreen.style.display = 'none';
    messagesContainer.innerHTML = '';

    addMessage('user', item.requirement);
    addResultMessage(item.data);

    currentSessionId = item.id;
}

// Delete history item
function deleteHistoryItem(index) {
    const history = getHistory();
    history.splice(index, 1);
    localStorage.setItem('qa_generator_history', JSON.stringify(history));
    loadHistory();
}

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
