# PowerShell script for Windows security audit

function Check-FirewallStatus {
    # Check Windows Firewall status
    $fw = Get-NetFirewallProfile
    
    Write-Host "=== Firewall Status ===" -ForegroundColor Cyan
    foreach ($profile in $fw) {
        Write-Host "$($profile.Name): $($profile.Enabled)" -ForegroundColor Yellow
    }
}

function Scan-OpenPorts {
    # Scan for open ports on localhost
    Write-Host "=== Open Ports Scan ===" -ForegroundColor Cyan
    $ports = @(21, 22, 23, 80, 443, 3389, 8080)
    
    foreach ($port in $ports) {
        $connection = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
        if ($connection.TcpTestSucceeded) {
            Write-Host "Port $port is OPEN" -ForegroundColor Red
        } else {
            Write-Host "Port $port is closed" -ForegroundColor Green
        }
    }
}

function Check-UserAccounts {
    # Check for insecure user accounts
    Write-Host "=== User Account Check ===" -ForegroundColor Cyan
    $users = Get-LocalUser
    
    foreach ($user in $users) {
        if ($user.PasswordRequired -eq $false) {
            Write-Host "WARNING: $($user.Name) has no password requirement" -ForegroundColor Red
        }
    }
}

# Main execution
Write-Host "=== Windows Security Audit ===" -ForegroundColor Cyan
Check-FirewallStatus
Scan-OpenPorts
Check-UserAccounts