#!/bin/bash
# Bash script for network scanning

echo "=== Network Security Scan ==="

scan_local_network() {
    # Scan local network for devices
    echo "Scanning local network..."
    if command -v nmap &> /dev/null; then
        local_ip=$(hostname -I | awk '{print $1}')
        network="${local_ip%.*}.0/24"
        echo "Scanning network: $network"
        sudo nmap -sn $network
    else
        echo "nmap not installed. Install with: sudo apt install nmap"
    fi
}

check_open_ports() {
    # Check open ports on local system
    echo "=== Open Ports on Local System ==="
    if command -v ss &> /dev/null; then
        ss -tuln
    elif command -v netstat &> /dev/null; then
        netstat -tuln
    fi
}

check_dns_config() {
    # Check DNS configuration
    echo "=== DNS Configuration ==="
    cat /etc/resolv.conf
}

# Main execution
scan_local_network
check_open_ports
check_dns_config
echo "Network scan completed"