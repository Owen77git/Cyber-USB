#!/bin/bash
# Bash script for Linux performance optimization

echo "=== Linux Performance Optimization ==="

disable_unnecessary_services() {
    # Disable unnecessary startup services
    echo "Disabling unnecessary services..."
    
    # Example services to disable (adjust based on system)
    services_to_disable=("bluetooth" "cups" "avahi-daemon")
    
    for service in "${services_to_disable[@]}"; do
        if systemctl is-enabled "$service" &> /dev/null; then
            sudo systemctl disable "$service"
            echo "Disabled: $service"
        fi
    done
}

optimize_swappiness() {
    # Optimize swappiness for better performance
    echo "Optimizing swappiness..."
    echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
    echo "Swappiness optimized to 10"
}

check_startup_apps() {
    # Check startup applications
    echo "=== Startup Applications ==="
    if command -v systemctl &> /dev/null; then
        systemctl list-unit-files --type=service | grep enabled
    fi
}

# Main execution
disable_unnecessary_services
optimize_swappiness
check_startup_apps
echo "Performance optimization completed"