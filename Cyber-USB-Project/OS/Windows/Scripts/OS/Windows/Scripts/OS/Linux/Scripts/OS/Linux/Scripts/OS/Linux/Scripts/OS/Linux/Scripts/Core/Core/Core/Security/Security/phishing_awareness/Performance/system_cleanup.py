# System cleanup module for Cyber USB

import os
import shutil
import tempfile
import platform
from pathlib import Path

class SystemCleanup:
    def __init__(self):
        self.system = platform.system()
        self.temp_dirs = []
        self.cache_dirs = []
        
        if self.system == "Windows":
            self.setup_windows_paths()
        elif self.system == "Linux":
            self.setup_linux_paths()
    
    def setup_windows_paths(self):
        # Windows specific paths
        self.temp_dirs = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            r'C:\Windows\Temp',
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp')
        ]
        
        self.cache_dirs = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles')
        ]
    
    def setup_linux_paths(self):
        # Linux specific paths
        self.temp_dirs = [
            '/tmp',
            '/var/tmp',
            str(Path.home() / '.cache'),
            str(Path.home() / '.tmp')
        ]
        
        self.cache_dirs = [
            str(Path.home() / '.cache'),
            str(Path.home() / '.thumbnails'),
            '/var/cache'
        ]
    
    def clean_temp_files(self):
        # Clean temporary files
        cleaned = 0
        total_size = 0
        
        for temp_dir in self.temp_dirs:
            if os.path.exists(temp_dir):
                print(f"Cleaning: {temp_dir}")
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                filepath = os.path.join(root, file)
                                size = os.path.getsize(filepath)
                                os.remove(filepath)
                                cleaned += 1
                                total_size += size
                            except:
                                continue
                except:
                    print(f"Could not clean: {temp_dir}")
        
        return cleaned, total_size
    
    def clear_cache(self):
        # Clear system and application cache
        cleared = 0
        total_size = 0
        
        for cache_dir in self.cache_dirs:
            if os.path.exists(cache_dir):
                print(f"Clearing cache: {cache_dir}")
                try:
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            try:
                                filepath = os.path.join(root, file)
                                size = os.path.getsize(filepath)
                                os.remove(filepath)
                                cleared += 1
                                total_size += size
                            except:
                                continue
                except:
                    print(f"Could not clear cache: {cache_dir}")
        
        return cleared, total_size
    
    def get_disk_usage(self, path='/'):
        # Get disk usage information
        try:
            usage = shutil.disk_usage(path)
            return {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent_used': (usage.used / usage.total) * 100
            }
        except:
            return None
    
    def format_size(self, bytes):
        # Format bytes to human readable size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def find_large_files(self, directory, threshold_mb=100):
        # Find large files for manual cleanup
        large_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    
                    if size_mb > threshold_mb:
                        large_files.append({
                            'path': filepath,
                            'size_mb': round(size_mb, 2)
                        })
                except:
                    continue
        
        # Sort by size (largest first)
        large_files.sort(key=lambda x: x['size_mb'], reverse=True)
        return large_files[:10]  # Return top 10 largest files
    
    def run_cleanup(self):
        # Main cleanup function
        print("Starting system cleanup...")
        
        # Clean temp files
        print("\n1. Cleaning temporary files...")
        temp_cleaned, temp_size = self.clean_temp_files()
        print(f"   Removed {temp_cleaned} temp files ({self.format_size(temp_size)})")
        
        # Clear cache
        print("\n2. Clearing cache...")
        cache_cleared, cache_size = self.clear_cache()
        print(f"   Cleared {cache_cleared} cache files ({self.format_size(cache_size)})")
        
        # Check disk usage
        print("\n3. Checking disk usage...")
        disk_info = self.get_disk_usage()
        if disk_info:
            print(f"   Total: {self.format_size(disk_info['total'])}")
            print(f"   Used: {self.format_size(disk_info['used'])} ({disk_info['percent_used']:.1f}%)")
            print(f"   Free: {self.format_size(disk_info['free'])}")
        
        # Find large files (optional)
        print("\n4. Finding large files (optional cleanup)...")
        home_dir = str(Path.home())
        large_files = self.find_large_files(home_dir)
        
        if large_files:
            print("   Top large files found:")
            for file_info in large_files:
                print(f"   - {file_info['path']}: {file_info['size_mb']} MB")
        
        total_freed = temp_size + cache_size
        print(f"\n✓ Cleanup completed! Total space freed: {self.format_size(total_freed)}")

if __name__ == "__main__":
    cleaner = SystemCleanup()
    cleaner.run_cleanup()