#!/bin/bash
# Bash script for Linux system cleanup

echo "=== Linux System Cleanup ==="

clean_temp_files() {
    # Remove temporary files
    echo "Cleaning temporary files..."
    sudo rm -rf /tmp/*
    sudo rm -rf /var/tmp/*
    echo "Temporary files cleaned"
}

clear_cache() {
    # Clear system cache
    echo "Clearing cache..."
    sudo sync
    echo 3 | sudo tee /proc/sys/vm/drop_caches
    echo "Cache cleared"
}

clean_package_cache() {
    # Clean package manager cache
    echo "Cleaning package cache..."
    if command -v apt &> /dev/null; then
        sudo apt clean
        sudo apt autoremove -y
    elif command -v yum &> /dev/null; then
        sudo yum clean all
    elif command -v dnf &> /dev/null; then
        sudo dnf clean all
    fi
    echo "Package cache cleaned"
}

check_disk_space() {
    # Check disk space usage
    echo "=== Disk Space Usage ==="
    df -h
}

# Main execution
clean_temp_files
clear_cache
clean_package_cache
check_disk_space
echo "Cleanup completed successfully"