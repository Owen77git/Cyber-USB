# Threat detection module for Cyber USB

import os
import re
import hashlib
import subprocess
from pathlib import Path

class ThreatDetector:
    def __init__(self):
        self.malware_signatures = [
            r"malware",
            r"trojan",
            r"virus",
            r"ransomware",
            r"backdoor",
            r"keylogger",
            r"spyware"
        ]
        
        self.suspicious_extensions = [
            '.exe', '.bat', '.cmd', '.vbs', '.js',
            '.ps1', '.sh', '.pyc', '.dll'
        ]
    
    def scan_directory(self, directory):
        # Scan directory for potential threats
        threats_found = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                
                # Check file extension
                if any(file.endswith(ext) for ext in self.suspicious_extensions):
                    # Check file content for signatures
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(4096)  # Read first 4KB
                            
                            for signature in self.malware_signatures:
                                if re.search(signature, content, re.IGNORECASE):
                                    threats_found.append({
                                        "file": filepath,
                                        "reason": f"Contains '{signature}' signature",
                                        "severity": "high"
                                    })
                                    break
                    except:
                        continue
        
        return threats_found
    
    def check_suspicious_processes(self):
        # Check for suspicious running processes
        suspicious = []
        
        try:
            import psutil
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    for signature in self.malware_signatures:
                        if signature in cmdline.lower():
                            suspicious.append({
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "reason": f"Process contains '{signature}'",
                                "severity": "high"
                            })
                            break
                except:
                    continue
                    
        except ImportError:
            print("psutil not installed. Install with: pip install psutil")
        
        return suspicious
    
    def calculate_file_hash(self, filepath):
        # Calculate MD5 hash of a file
        try:
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            return file_hash.hexdigest()
        except:
            return None
    
    def run_clamav_scan(self, directory):
        # Run ClamAV scan if available
        try:
            result = subprocess.run(
                ['clamscan', '-r', '--bell', '-i', directory],
                capture_output=True,
                text=True
            )
            return result.stdout
        except FileNotFoundError:
            return "ClamAV not installed"
        except Exception as e:
            return f"Error running ClamAV: {e}"
    
    def generate_report(self, threats, suspicious_processes):
        # Generate threat detection report
        report = []
        
        report.append("="*60)
        report.append("THREAT DETECTION REPORT")
        report.append("="*60)
        
        report.append(f"\nSuspicious Files Found: {len(threats)}")
        for threat in threats:
            report.append(f"  - {threat['file']}")
            report.append(f"    Reason: {threat['reason']}")
            report.append(f"    Severity: {threat['severity']}")
        
        report.append(f"\nSuspicious Processes Found: {len(suspicious_processes)}")
        for proc in suspicious_processes:
            report.append(f"  - PID {proc['pid']}: {proc['name']}")
            report.append(f"    Reason: {proc['reason']}")
        
        return "\n".join(report)

if __name__ == "__main__":
    detector = ThreatDetector()
    
    # Scan home directory
    home_dir = str(Path.home())
    threats = detector.scan_directory(home_dir)
    
    # Check processes
    suspicious_processes = detector.check_suspicious_processes()
    
    # Generate report
    report = detector.generate_report(threats, suspicious_processes)
    print(report)