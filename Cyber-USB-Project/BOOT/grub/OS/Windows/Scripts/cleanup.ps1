# PowerShell script for Windows system cleanup

function Clean-TemporaryFiles {
    # Remove temporary files from various locations
    Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$env:LOCALAPPDATA\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Temporary files cleaned" -ForegroundColor Green
}

function Clear-WindowsCache {
    # Clear Windows cache and junk files
    CleanMgr /sagerun:1
    Write-Host "Windows cache cleared" -ForegroundColor Green
}

function Free-DiskSpace {
    # Analyze and free up disk space
    $drive = Get-PSDrive C
    $freeSpace = [math]::Round($drive.Free / 1GB, 2)
    Write-Host "Free space on C: $freeSpace GB" -ForegroundColor Yellow
    
    # Optional: Run disk cleanup
    Write-Host "Running disk cleanup..." -ForegroundColor Cyan
}

# Main execution
Write-Host "=== Windows System Cleanup ===" -ForegroundColor Cyan
Clean-TemporaryFiles
Clear-WindowsCache
Free-DiskSpace
Write-Host "Cleanup completed" -ForegroundColor Green