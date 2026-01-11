# PowerShell script for Windows updates and repair

function Check-WindowsUpdates {
    # Trigger Windows update checks
    Write-Host "Checking for Windows updates..." -ForegroundColor Cyan
    
    $updateSession = New-Object -ComObject Microsoft.Update.Session
    $updateSearcher = $updateSession.CreateUpdateSearcher()
    
    try {
        $searchResult = $updateSearcher.Search("IsInstalled=0")
        Write-Host "Found $($searchResult.Updates.Count) available updates" -ForegroundColor Yellow
        
        foreach ($update in $searchResult.Updates) {
            Write-Host "  - $($update.Title)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "Failed to check for updates" -ForegroundColor Red
    }
}

function Repair-SystemFiles {
    # Repair corrupted system files using SFC and DISM
    Write-Host "Repairing system files..." -ForegroundColor Cyan
    
    # Run System File Checker
    Write-Host "Running SFC (System File Checker)..." -ForegroundColor Yellow
    sfc /scannow
    
    # Run DISM for additional repairs
    Write-Host "Running DISM (Deployment Image Servicing)..." -ForegroundColor Yellow
    DISM /Online /Cleanup-Image /RestoreHealth
    
    Write-Host "System repair completed" -ForegroundColor Green
}

# Main execution
Write-Host "=== Windows Update & Repair ===" -ForegroundColor Cyan
Check-WindowsUpdates
Repair-SystemFiles