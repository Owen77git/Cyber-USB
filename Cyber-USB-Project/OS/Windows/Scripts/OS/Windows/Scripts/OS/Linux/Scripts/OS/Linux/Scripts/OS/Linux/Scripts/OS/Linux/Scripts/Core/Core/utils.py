# Utility functions for Cyber USB

import os
import sys
import logging
import platform
from datetime import datetime

def setup_logging():
    # Set up logging for the application
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"cyberusb_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def get_system_info():
    # Get system information
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }
    return info

def check_dependencies():
    # Check if required dependencies are installed
    required_packages = []
    
    if sys.platform == "win32":
        required_packages = ["powershell"]
    elif sys.platform == "linux":
        required_packages = ["bash", "python3"]
    
    missing = []
    for pkg in required_packages:
        if not check_command_exists(pkg):
            missing.append(pkg)
    
    return missing

def check_command_exists(command):
    # Check if a command exists in the system
    import shutil
    return shutil.which(command) is not None

def get_disk_usage():
    # Get disk usage information
    import shutil
    
    try:
        usage = shutil.disk_usage("/")
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2),
            "percent_used": round((usage.used / usage.total) * 100, 2)
        }
    except:
        return None

def get_memory_info():
    # Get memory information
    import psutil
    
    try:
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "percent_used": memory.percent
        }
    except:
        return None

def format_size(bytes):
    # Format bytes to human readable size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"