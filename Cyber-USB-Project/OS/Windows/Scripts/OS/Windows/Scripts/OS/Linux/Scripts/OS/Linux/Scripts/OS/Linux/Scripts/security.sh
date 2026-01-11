#!/bin/bash
# Bash script for Linux security tasks

echo "=== Linux Security Hardening ==="

check_firewall() {
    # Check firewall status
    echo "Checking firewall..."
    if command -v ufw &> /dev/null; then
        sudo ufw status verbose
    elif command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --list-all
    else
        echo "No known firewall manager found"
    fi
}

scan_malware() {
    # Simple malware scan using ClamAV if available
    echo "Running malware scan..."
    if command -v clamscan &> /dev/null; then
        echo "Scanning /home directory..."
        clamscan -r --bell -i /home
    else
        echo "ClamAV not installed. Install with: sudo apt install clamav"
    fi
}

check_suspicious_processes() {
    # Check for suspicious processes
    echo "=== Running Processes Check ==="
    ps aux | grep -E "(crypt|miner|backdoor|shell)" | grep -v grep || echo "No suspicious processes found"
}

# Main execution
check_firewall
scan_malware
check_suspicious_processes
echo "Security check completed"