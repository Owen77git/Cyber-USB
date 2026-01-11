// Cyber USB Toolkit - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
    
    // Setup event listeners
    setupEventListeners();
    
    // Update system info
    updateSystemInfo();
    
    // Start live updates
    startLiveUpdates();
});

function initApp() {
    // Initialize application settings
    console.log('Cyber USB Toolkit initialized');
    
    // Check for OS
    detectOS();
    
    // Load saved settings
    loadSettings();
}

function setupEventListeners() {
    // Tab navigation
    const navItems = document.querySelectorAll('.nav-menu li');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            switchTab(tabId);
            
            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Quick action cards
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            executeQuickAction(action);
        });
    });
    
    // Modal close buttons
    const closeButtons = document.querySelectorAll('.close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            modal.style.display = 'none';
        });
    });
    
    // Click outside modal to close
    window.addEventListener('click', function(event) {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Run tool buttons
    const runButtons = document.querySelectorAll('.run-btn');
    runButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent card click event
        });
    });
}

function detectOS() {
    // Detect operating system
    const userAgent = navigator.userAgent;
    let os = 'Unknown OS';
    
    if (userAgent.indexOf('Win') !== -1) os = 'Windows';
    if (userAgent.indexOf('Mac') !== -1) os = 'macOS';
    if (userAgent.indexOf('Linux') !== -1) os = 'Linux';
    if (userAgent.indexOf('Android') !== -1) os = 'Android';
    if (userAgent.indexOf('like Mac') !== -1) os = 'iOS';
    
    document.getElementById('os-info').textContent = `OS: ${os}`;
    return os;
}

function updateSystemInfo() {
    // Update time display
    updateTime();
    
    // Update system status (simulated for now)
    updateSystemStatus();
}

function updateTime() {
    // Update current time
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour12: true,
        hour: '2-digit',
        minute: '2-digit'
    });
    
    document.getElementById('time').textContent = timeString;
}

function updateSystemStatus() {
    // Update system status indicators (simulated)
    const cpu = Math.floor(Math.random() * 30) + 40; // 40-70%
    const memory = Math.floor(Math.random() * 35) + 50; // 50-85%
    const disk = Math.floor(Math.random() * 40) + 40; // 40-80%
    
    document.getElementById('cpu-usage').style.width = `${cpu}%`;
    document.getElementById('cpu-text').textContent = `${cpu}%`;
    
    document.getElementById('memory-usage').style.width = `${memory}%`;
    document.getElementById('memory-text').textContent = `${memory}%`;
    
    document.getElementById('disk-usage').style.width = `${disk}%`;
    document.getElementById('disk-text').textContent = `${disk}%`;
}

function startLiveUpdates() {
    // Update time every minute
    setInterval(updateTime, 60000);
    
    // Update system status every 30 seconds
    setInterval(updateSystemStatus, 30000);
}

function switchTab(tabId) {
    // Switch between tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.add('active');
    }
}

function executeQuickAction(action) {
    // Execute quick actions
    const actions = {
        'cleanup': 'Starting system cleanup...',
        'security-scan': 'Starting security scan...',
        'driver-check': 'Checking driver status...',
        'network-scan': 'Starting network scan...'
    };
    
    if (actions[action]) {
        logToConsole(actions[action]);
        
        // Simulate action execution
        setTimeout(() => {
            logToConsole(`${action} completed successfully`);
            showNotification(`${action.replace('-', ' ')} completed`, 'success');
        }, 2000);
    }
}

function runTool(tool) {
    // Run a specific tool
    const toolMessages = {
        'cleanup': 'Running system cleanup...',
        'drivers': 'Checking and updating drivers...',
        'disk': 'Analyzing disk health...',
        'power': 'Optimizing power settings...',
        'threat': 'Scanning for threats...',
        'firewall': 'Checking firewall status...',
        'password': 'Auditing passwords...',
        'network': 'Scanning network...'
    };
    
    if (toolMessages[tool]) {
        logToConsole(toolMessages[tool]);
        
        // Simulate tool execution
        setTimeout(() => {
            logToConsole(`${tool} tool completed`);
            showNotification(`${tool} completed`, 'info');
        }, 3000);
    }
}

function logToConsole(message, type = 'info') {
    // Log messages to console output
    const consoleOutput = document.getElementById('console-output');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('div');
    logEntry.className = `console-line log-${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    
    consoleOutput.appendChild(logEntry);
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

function clearConsole() {
    // Clear console output
    const consoleOutput = document.getElementById('console-output');
    consoleOutput.innerHTML = '<div class="console-line">Console cleared</div>';
}

function saveLogs() {
    // Save logs to file (simulated)
    const consoleOutput = document.getElementById('console-output');
    const logs = consoleOutput.textContent;
    
    logToConsole('Saving logs to file...');
    
    // In a real implementation, this would save to a file
    setTimeout(() => {
        logToConsole('Logs saved to cyberusb_log.txt', 'success');
        showNotification('Logs saved successfully', 'success');
    }, 1000);
}

function showPhishingExamples() {
    // Show phishing examples
    logToConsole('Loading phishing examples...');
    
    const examples = [
        'Example 1: Fake login page - Check URL for misspellings',
        'Example 2: Urgent email - Verify sender email address',
        'Example 3: Too good to be true offers - Always verify legitimacy'
    ];
    
    setTimeout(() => {
        logToConsole('Phishing Examples:');
        examples.forEach(example => {
            logToConsole(`  • ${example}`, 'warning');
        });
    }, 1000);
}

function showNotification(message, type = 'info') {
    // Show notification toast
    const toast = document.createElement('div');
    toast.className = `notification toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#00adb5' : '#2d4059'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Modal functions
function showAbout() {
    document.getElementById('about-modal').style.display = 'flex';
}

function showHelp() {
    logToConsole('Opening help documentation...');
    showNotification('Help documentation loaded', 'info');
}

function showLicense() {
    logToConsole('Displaying license information...');
    logToConsole('Cyber USB Toolkit - MIT License', 'info');
    logToConsole('For educational and defensive use only', 'warning');
}

// Load settings from localStorage
function loadSettings() {
    const darkMode = localStorage.getItem('cyberusb-darkmode') !== 'false';
    if (darkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .log-info { color: #8d8d8d; }
    .log-success { color: #00adb5; }
    .log-warning { color: #ff9800; }
    .log-error { color: #f44336; }
    
    .notification {
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
`;
document.head.appendChild(style);