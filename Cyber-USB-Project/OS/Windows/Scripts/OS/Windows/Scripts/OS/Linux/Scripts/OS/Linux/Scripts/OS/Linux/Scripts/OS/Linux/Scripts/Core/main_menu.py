#!/usr/bin/env python3
# Main menu controller for Cyber USB

import os
import sys
import subprocess
import json

class CyberUSBMenu:
    def __init__(self):
        self.config = self.load_config()
        self.current_os = self.detect_os()
        
    def load_config(self):
        # Load configuration from JSON file
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"auto_update": False, "log_level": "info"}
    
    def detect_os(self):
        # Detect current operating system
        if sys.platform == "win32":
            return "windows"
        elif sys.platform == "linux":
            # Check if Kali Linux
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release", "r") as f:
                    content = f.read()
                    if "kali" in content.lower():
                        return "kali"
            return "linux"
        else:
            return "unknown"
    
    def show_main_menu(self):
        # Display main menu based on OS
        print("\n" + "="*50)
        print("        CYBER USB TOOLKIT")
        print("="*50)
        print(f"Detected OS: {self.current_os.upper()}")
        print("\nMain Menu:")
        print("1. System Performance")
        print("2. System Security")
        print("3. Run All Functions")
        print("4. Settings")
        print("5. Exit")
        print("="*50)
        
        choice = input("Select option (1-5): ").strip()
        return choice
    
    def show_performance_menu(self):
        # Display performance optimization menu
        print("\n" + "="*50)
        print("    SYSTEM PERFORMANCE OPTIMIZATION")
        print("="*50)
        print("1. System Cleanup")
        print("2. Driver Management")
        print("3. Windows Update & Repair")
        print("4. Performance Boost")
        print("5. Disk Management")
        print("6. Battery & Power Optimization")
        print("7. Back to Main Menu")
        print("="*50)
        
        choice = input("Select option (1-7): ").strip()
        return choice
    
    def show_security_menu(self):
        # Display security menu
        print("\n" + "="*50)
        print("        SYSTEM SECURITY")
        print("="*50)
        print("1. Threat Detection")
        print("2. System Hardening")
        print("3. Password & Credential Audit")
        print("4. Network & Port Security")
        print("5. Phishing Defense & Awareness")
        print("6. Ethical Hacking Tools")
        print("7. Back to Main Menu")
        print("="*50)
        
        choice = input("Select option (1-7): ").strip()
        return choice
    
    def execute_function(self, category, function):
        # Execute selected function based on OS
        scripts = {
            "windows": {
                "cleanup": "OS/Windows/Scripts/cleanup.ps1",
                "drivers": "OS/Windows/Scripts/drivers.ps1",
                "updates": "OS/Windows/Scripts/updates.ps1",
                "security": "OS/Windows/Scripts/security_audit.ps1"
            },
            "linux": {
                "cleanup": "OS/Linux/Scripts/cleanup.sh",
                "performance": "OS/Linux/Scripts/performance.sh",
                "security": "OS/Linux/Scripts/security.sh",
                "network": "OS/Linux/Scripts/network_scan.sh"
            }
        }
        
        if self.current_os in scripts and function in scripts[self.current_os]:
            script_path = scripts[self.current_os][function]
            return self.run_script(script_path)
        else:
            print(f"Function not available for {self.current_os}")
            return False
    
    def run_script(self, script_path):
        # Run script based on file extension
        full_path = os.path.join(os.path.dirname(__file__), "..", script_path)
        
        if not os.path.exists(full_path):
            print(f"Script not found: {full_path}")
            return False
        
        try:
            if script_path.endswith('.ps1'):
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", full_path])
            elif script_path.endswith('.sh'):
                subprocess.run(["bash", full_path])
            elif script_path.endswith('.py'):
                subprocess.run([sys.executable, full_path])
            return True
        except Exception as e:
            print(f"Error running script: {e}")
            return False
    
    def run_all_performance(self):
        # Run all performance functions
        print("Running all performance optimizations...")
        functions = ["cleanup", "drivers", "updates"]
        for func in functions:
            self.execute_function("performance", func)
    
    def run_all_security(self):
        # Run all security functions
        print("Running all security checks...")
        functions = ["security", "network"]
        for func in functions:
            self.execute_function("security", func)
    
    def main_loop(self):
        # Main program loop
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                # Performance menu
                perf_choice = self.show_performance_menu()
                if perf_choice == "1":
                    self.execute_function("performance", "cleanup")
                elif perf_choice == "2":
                    self.execute_function("performance", "drivers")
                elif perf_choice == "7":
                    continue
                    
            elif choice == "2":
                # Security menu
                sec_choice = self.show_security_menu()
                if sec_choice == "1":
                    self.execute_function("security", "security")
                elif sec_choice == "4":
                    self.execute_function("security", "network")
                elif sec_choice == "7":
                    continue
                    
            elif choice == "3":
                # Run all functions
                print("Running all functions...")
                self.run_all_performance()
                self.run_all_security()
                
            elif choice == "5":
                # Exit
                print("Thank you for using Cyber USB Toolkit!")
                break

if __name__ == "__main__":
    menu = CyberUSBMenu()
    menu.main_loop()