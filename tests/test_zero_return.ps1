. .\src\zero_return.ps1

Write-Host "--- TESTING ZERO RETURN LOGIC ---" -ForegroundColor Green

# Test 1: High risk (should trigger)
try {
    Write-Host "Test 1: RiskScore = 0.4 (Threshold 0.7)"
    $triggered = Zero-Return -RiskScore 0.4
    Write-Host "Triggered: $triggered"
} catch {
    Write-Host "Test 1 failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Low risk (should not trigger)
try {
    Write-Host "Test 2: RiskScore = 0.9 (Threshold 0.7)"
    $triggered = Zero-Return -RiskScore 0.9
    Write-Host "Triggered: $triggered"
} catch {
    Write-Host "Test 2 failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Additional Test 3: Edge case (exactly threshold)
try {
    Write-Host "Test 3: RiskScore = 0.7 (Threshold 0.7)"
    $triggered = Zero-Return -RiskScore 0.7
    Write-Host "Triggered: $triggered"  # Should be False (assuming >= threshold is safe)
} catch {
    Write-Host "Test 3 failed: $($_.Exception.Message)" -ForegroundColor Red
}
# Additional Test 4: Invalid input (should handle gracefully)
try {
    Write-Host "Test 4: Invalid RiskScore = ''abc'' (Threshold 0.7)"
    $triggered = Zero-Return -RiskScore 'abc'  # Will error, but catch handles it
    Write-Host "Triggered: $triggered"
} catch {
    Write-Host "Test 4 handled error: $($_.Exception.Message)" -ForegroundColor Yellow
}
