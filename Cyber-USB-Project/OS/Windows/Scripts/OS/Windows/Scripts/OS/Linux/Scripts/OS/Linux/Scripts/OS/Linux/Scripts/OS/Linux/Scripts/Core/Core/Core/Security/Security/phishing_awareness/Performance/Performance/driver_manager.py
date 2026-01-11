# Driver management module for Cyber USB

import platform
import subprocess
import re
from datetime import datetime

class DriverManager:
    def __init__(self):
        self.system = platform.system()
        
    def get_windows_drivers(self):
        # Get Windows driver information using PowerShell
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName, DriverVersion, DriverDate | ConvertTo-Json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                import json
                drivers = json.loads(result.stdout)
                
                # Convert to list if single driver
                if isinstance(drivers, dict):
                    drivers = [drivers]
                
                return drivers
            else:
                print("Could not retrieve driver information")
                return []
                
        except Exception as e:
            print(f"Error getting drivers: {e}")
            return []
    
    def get_linux_drivers(self):
        # Get Linux driver/kernel module information
        drivers = []
        
        try:
            # Get loaded modules
            modules_result = subprocess.run(
                ['lsmod'],
                capture_output=True,
                text=True
            )
            
            if modules_result.returncode == 0:
                lines = modules_result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 3:
                        drivers.append({
                            'name': parts[0],
                            'size': parts[1],
                            'used_by': parts[2] if len(parts) > 2 else ''
                        })
            
            # Get kernel version
            kernel_result = subprocess.run(
                ['uname', '-r'],
                capture_output=True,
                text=True
            )
            
            if kernel_result.returncode == 0:
                drivers.append({
                    'name': 'Kernel',
                    'version': kernel_result.stdout.strip(),
                    'type': 'system'
                })
                
        except Exception as e:
            print(f"Error getting Linux drivers: {e}")
        
        return drivers
    
    def check_outdated_drivers(self, drivers):
        # Check for outdated drivers (Windows specific)
        outdated = []
        
        if self.system != "Windows":
            return outdated
        
        for driver in drivers:
            if 'DriverDate' in driver and driver['DriverDate']:
                try:
                    # Parse date string
                    date_str = driver['DriverDate'].split('.')[0]  # Remove fractional seconds
                    driver_date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
                    
                    # Check if older than 6 months
                    six_months_ago = datetime.now().replace(month=datetime.now().month-6)
                    if driver_date < six_months_ago:
                        outdated.append({
                            'name': driver.get('DeviceName', 'Unknown'),
                            'version': driver.get('DriverVersion', 'Unknown'),
                            'date': driver_date.strftime('%Y-%m-%d'),
                            'reason': 'Older than 6 months'
                        })
                except:
                    continue
        
        return outdated
    
    def update_windows_drivers(self):
        # Assist in updating Windows drivers
        print("Checking for Windows driver updates...")
        
        try:
            # Method 1: Check Windows Update
            result = subprocess.run(
                ['powershell', '-Command', '$Session = New-Object -ComObject Microsoft.Update.Session; $Searcher = $Session.CreateUpdateSearcher(); $Result = $Searcher.Search("IsInstalled=0 and Type=\'Driver\'"); Write-Host $Result.Updates.Count'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                update_count = int(result.stdout.strip())
                print(f"Found {update_count} driver updates available via Windows Update")
                
                if update_count > 0:
                    response = input("Would you like to install these updates? (y/n): ")
                    if response.lower() == 'y':
                        print("Note: Driver updates will be installed through Windows Update")
                        print("Please run Windows Update from Settings for complete installation")
            
            # Method 2: Check device manager
            print("\nChecking Device Manager for driver issues...")
            result = subprocess.run(
                ['powershell', '-Command', 'Get-PnpDevice | Where-Object {$_.Problem -ne $null} | Select-Object FriendlyName, Problem | ConvertTo-Json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                problem_devices = json.loads(result.stdout)
                
                if isinstance(problem_devices, dict):
                    problem_devices = [problem_devices]
                
                if problem_devices:
                    print(f"Found {len(problem_devices)} devices with issues:")
                    for device in problem_devices:
                        print(f"  - {device.get('FriendlyName', 'Unknown')}: Problem code {device.get('Problem', 'Unknown')}")
            
        except Exception as e:
            print(f"Error checking for updates: {e}")
    
    def check_missing_drivers(self):
        # Check for missing drivers (Windows specific)
        if self.system != "Windows":
            return []
        
        missing = []
        
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-PnpDevice | Where-Object {$_.Status -eq "Unknown"} | Select-Object FriendlyName, Class | ConvertTo-Json'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                unknown_devices = json.loads(result.stdout)
                
                if isinstance(unknown_devices, dict):
                    unknown_devices = [unknown_devices]
                
                for device in unknown_devices:
                    missing.append({
                        'name': device.get('FriendlyName', 'Unknown Device'),
                        'class': device.get('Class', 'Unknown'),
                        'status': 'Driver missing or unknown'
                    })
        
        except Exception as e:
            print(f"Error checking missing drivers: {e}")
        
        return missing
    
    def generate_driver_report(self):
        # Generate driver status report
        print("="*60)
        print("DRIVER STATUS REPORT")
        print("="*60)
        
        if self.system == "Windows":
            drivers = self.get_windows_drivers()
            outdated = self.check_outdated_drivers(drivers)
            missing = self.check_missing_drivers()
            
            print(f"\nTotal Drivers Found: {len(drivers)}")
            print(f"Outdated Drivers: {len(outdated)}")
            print(f"Missing Drivers: {len(missing)}")
            
            if outdated:
                print("\nOutdated Drivers (older than 6 months):")
                for driver in outdated[:5]:  # Show first 5
                    print(f"  - {driver['name']}")
                    print(f"    Version: {driver['version']}, Date: {driver['date']}")
            
            if missing:
                print("\nDevices with Missing Drivers:")
                for device in missing:
                    print(f"  - {device['name']} ({device['class']})")
            
            # Offer to update
            if outdated or missing:
                print("\n" + "="*60)
                self.update_windows_drivers()
        
        elif self.system == "Linux":
            drivers = self.get_linux_drivers()
            print(f"\nLoaded Kernel Modules: {len(drivers)}")
            print("\nSystem Information:")
            for driver in drivers:
                if isinstance(driver, dict):
                    print(f"  - {driver.get('name', 'Unknown')}: {driver.get('version', '')}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    manager = DriverManager()
    manager.generate_driver_report()