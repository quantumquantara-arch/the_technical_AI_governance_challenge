# Dioptra Benchmark Runner - 100 Adversarial Prompts
# Integrates with MLflow tracking at localhost:35000

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = $PWD

# Dot-source detection modules
. "$root\src\detection.ps1"
. "$root\src\zero_return.ps1"

# MLflow configuration
$MLFLOW_TRACKING_URI = "http://localhost:35000"
$EXPERIMENT_NAME = "AI_Governance_Adversarial_Benchmark"
$RUN_NAME = "adversarial_100_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

Write-Host "`n=== DIOPTRA ADVERSARIAL BENCHMARK ===" -ForegroundColor Cyan
Write-Host "MLflow Tracking: $MLFLOW_TRACKING_URI" -ForegroundColor Cyan
Write-Host "Experiment: $EXPERIMENT_NAME" -ForegroundColor Cyan
Write-Host "Run: $RUN_NAME`n" -ForegroundColor Cyan

# Load adversarial test suite
if (-not (Test-Path "adversarial_test_suite.json")) {
    Write-Host "ERROR: adversarial_test_suite.json not found" -ForegroundColor Red
    Write-Host "Run create_adversarial_suite.ps1 first" -ForegroundColor Red
    exit 1
}

$tests = Get-Content "adversarial_test_suite.json" | ConvertFrom-Json

# Create experiment in MLflow
Write-Host "Initializing MLflow experiment..." -ForegroundColor Yellow
try {
    $expBody = @{
        name = $EXPERIMENT_NAME
    } | ConvertTo-Json

    $expResponse = Invoke-RestMethod -Uri "$MLFLOW_TRACKING_URI/api/2.0/mlflow/experiments/create" `
        -Method Post `
        -ContentType "application/json" `
        -Body $expBody `
        -ErrorAction SilentlyContinue

    $experimentId = $expResponse.experiment_id
    Write-Host "? Created experiment ID: $experimentId" -ForegroundColor Green
} catch {
    # Experiment might already exist, get it by listing all
    try {
        $listResponse = Invoke-RestMethod -Uri "$MLFLOW_TRACKING_URI/api/2.0/mlflow/experiments/list" `
            -Method Get

        $experiment = $listResponse.experiments | Where-Object { $_.name -eq $EXPERIMENT_NAME } | Select-Object -First 1
        if ($experiment) {
            $experimentId = $experiment.experiment_id
            Write-Host "? Using existing experiment ID: $experimentId" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Could not create or find experiment" -ForegroundColor Red
            Write-Host "Creating with default ID 0" -ForegroundColor Yellow
            $experimentId = "0"
        }
    } catch {
        Write-Host "WARNING: MLflow API error, using default experiment ID 0" -ForegroundColor Yellow
        $experimentId = "0"
    }
}

# Create MLflow run
$runBody = @{
    experiment_id = $experimentId
    start_time = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds
    tags = @(
        @{ key = "mlflow.runName"; value = $RUN_NAME },
        @{ key = "system"; value = "ASIOS_Governance" },
        @{ key = "version"; value = "1.0" },
        @{ key = "test_count"; value = "100" }
    )
} | ConvertTo-Json -Depth 5

try {
    $runResponse = Invoke-RestMethod -Uri "$MLFLOW_TRACKING_URI/api/2.0/mlflow/runs/create" `
        -Method Post `
        -ContentType "application/json" `
        -Body $runBody

    $runId = $runResponse.run.info.run_id
    Write-Host "? Created run ID: $runId`n" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not create MLflow run, continuing without tracking" -ForegroundColor Yellow
    $runId = $null
}

# Initialize counters
$results = @()
$categoryResults = @{}
$confusionMatrix = @{
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
}

# Decision band mapping
function Map-ToDecisionBand {
    param([string]$Decision)
    switch ($Decision) {
        "SAFE" { return "negative" }
        "MODERATE" { return "moderate" }
        "HIGH" { return "positive" }
        "CRITICAL" { return "positive" }
        default { return "unknown" }
    }
}

# Process each test
$testNum = 0
foreach ($test in $tests) {
    $testNum++
    Write-Host "[$testNum/100] Testing $($test.id)... " -NoNewline
    
    # Call detection
    $res = Detect-DualUse -InputText $test.text
    
    # Extract values
    $risk_score = $res.risk_score
    $kappa = $res.kappa
    $tau = $res.tau
    $detected_terms = $res.detected_terms
    $interrupt_level = $res.interrupt_level
    $base_decision = $res.decision
    $hasDefensive = $res.has_defensive
    $hasOffensive = $res.has_offensive
    
    # Context checks
    $hasThreat = $test.text -match '\b(bioweapon|weapon|virus|pathogen|synthesis|exploit|malware|bomb|explosive|toxin)\b'
    
    # Obfuscation check
    $obfuscationTerms = @('novel','breakthrough','unprecedented','capabilities','sensitive','domains','rapid','cutting-edge','advanced','state-of-the-art','revolutionary','transformative','disruptive','paradigm-shifting','next-generation','emerging','strategic','competitive','proprietary','classified','asymmetric','contested')
    $isObfuscation = $detected_terms.Count -gt 0
    foreach ($term in $detected_terms) {
        if ($term -notin $obfuscationTerms) {
            $isObfuscation = $false
            break
        }
    }
    
    # Decision mapping
    $decision = if ($base_decision -eq "HAZARD") {
        # Strong defensive context override
        if ($hasDefensive -and $hasThreat -and -not $hasOffensive) {
            "SAFE"
        }
        # Obfuscation = HIGH (not CRITICAL)
        elseif ($isObfuscation -and $detected_terms.Count -ge 3) {
            "HIGH"
        }
        # Critical threats
        elseif ($interrupt_level -ge 3 -and $detected_terms.Count -ge 4 -and -not $isObfuscation) {
            "CRITICAL"
        }
        else {
            "HIGH"
        }
    } else {
        if ($detected_terms.Count -eq 0) { "SAFE" }
        else { "MODERATE" }
    }
    
    # Check correctness
    $pass = ($decision -eq $test.expected)
    
    # Update confusion matrix
    $predicted_band = Map-ToDecisionBand $decision
    $expected_band = Map-ToDecisionBand $test.expected
    
    if ($expected_band -eq "positive" -and $predicted_band -eq "positive") {
        $confusionMatrix.true_positive++
    } elseif ($expected_band -eq "negative" -and $predicted_band -eq "negative") {
        $confusionMatrix.true_negative++
    } elseif ($expected_band -eq "negative" -and $predicted_band -eq "positive") {
        $confusionMatrix.false_positive++
    } elseif ($expected_band -eq "positive" -and $predicted_band -eq "negative") {
        $confusionMatrix.false_negative++
    }
    
    # Category tracking
    if (-not $categoryResults.ContainsKey($test.category)) {
        $categoryResults[$test.category] = @{ total = 0; correct = 0 }
    }
    $categoryResults[$test.category].total++
    if ($pass) { $categoryResults[$test.category].correct++ }
    
    # Store result
    $result = @{
        test_id = $test.id
        category = $test.category
        text_preview = $test.text.Substring(0, [Math]::Min(50, $test.text.Length))
        decision = $decision
        expected = $test.expected
        pass = $pass
        risk_score = $risk_score
        detected_terms_count = $detected_terms.Count
        interrupt_level = $interrupt_level
    }
    $results += $result
    
    # Print result
    if ($pass) {
        Write-Host "PASS ($decision)" -ForegroundColor Green
    } else {
        Write-Host "FAIL ($decision vs $($test.expected))" -ForegroundColor Red
    }
}

# Calculate metrics
$total_tests = $tests.Count
$correct = ($results | Where-Object { $_.pass }).Count
$accuracy = [Math]::Round($correct / $total_tests, 4)

$tp = $confusionMatrix.true_positive
$tn = $confusionMatrix.true_negative
$fp = $confusionMatrix.false_positive
$fn = $confusionMatrix.false_negative

$precision = if (($tp + $fp) -gt 0) { [Math]::Round($tp / ($tp + $fp), 4) } else { 0 }
$recall = if (($tp + $fn) -gt 0) { [Math]::Round($tp / ($tp + $fn), 4) } else { 0 }
$f1_score = if (($precision + $recall) -gt 0) { [Math]::Round(2 * $precision * $recall / ($precision + $recall), 4) } else { 0 }

# Log metrics to MLflow if available
if ($runId) {
    Write-Host "`n=== LOGGING METRICS TO MLFLOW ===" -ForegroundColor Cyan

    $metrics = @(
        @{ key = "accuracy"; value = $accuracy; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "precision"; value = $precision; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "recall"; value = $recall; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "f1_score"; value = $f1_score; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "true_positives"; value = $tp; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "true_negatives"; value = $tn; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "false_positives"; value = $fp; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 },
        @{ key = "false_negatives"; value = $fn; timestamp = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds; step = 0 }
    )

    $metricsBody = @{
        run_id = $runId
        metrics = $metrics
    } | ConvertTo-Json -Depth 5

    try {
        Invoke-RestMethod -Uri "$MLFLOW_TRACKING_URI/api/2.0/mlflow/runs/log-batch" `
            -Method Post `
            -ContentType "application/json" `
            -Body $metricsBody | Out-Null
        Write-Host "? Logged overall metrics" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Could not log metrics to MLflow" -ForegroundColor Yellow
    }

    # End MLflow run
    $endBody = @{
        run_id = $runId
        end_time = [long]([datetime]::UtcNow - [datetime]'1970-01-01').TotalMilliseconds
        status = "FINISHED"
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "$MLFLOW_TRACKING_URI/api/2.0/mlflow/runs/update" `
            -Method Post `
            -ContentType "application/json" `
            -Body $endBody | Out-Null
    } catch {}
}

# Generate final report
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportDir = "$root\artifacts\dioptra_benchmark_$timestamp"
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null

$report = @{
    run_id = $runId
    timestamp = $timestamp
    mlflow_uri = $MLFLOW_TRACKING_URI
    experiment_name = $EXPERIMENT_NAME
    overall_metrics = @{
        total_tests = $total_tests
        correct = $correct
        accuracy = $accuracy
        precision = $precision
        recall = $recall
        f1_score = $f1_score
    }
    confusion_matrix = $confusionMatrix
    category_results = $categoryResults
    detailed_results = $results
}

$report | ConvertTo-Json -Depth 10 | Set-Content -Path "$reportDir\benchmark_report.json" -Encoding UTF8

# Print summary
Write-Host "`n=== BENCHMARK SUMMARY ===" -ForegroundColor Cyan
Write-Host "Total Tests: $total_tests" -ForegroundColor White
Write-Host "Correct: $correct" -ForegroundColor $(if ($correct -ge 70) { "Green" } elseif ($correct -ge 50) { "Yellow" } else { "Red" })
Write-Host "Accuracy: $($accuracy * 100)%" -ForegroundColor $(if ($accuracy -ge 0.7) { "Green" } elseif ($accuracy -ge 0.5) { "Yellow" } else { "Red" })
Write-Host "Precision: $($precision * 100)%" -ForegroundColor White
Write-Host "Recall: $($recall * 100)%" -ForegroundColor White
Write-Host "F1 Score: $($f1_score * 100)%" -ForegroundColor White
Write-Host "`nConfusion Matrix:" -ForegroundColor Cyan
Write-Host "  True Positives: $tp" -ForegroundColor Green
Write-Host "  True Negatives: $tn" -ForegroundColor Green
Write-Host "  False Positives: $fp" -ForegroundColor Red
Write-Host "  False Negatives: $fn" -ForegroundColor Red
Write-Host "`nCategory Breakdown:" -ForegroundColor Cyan
foreach ($cat in $categoryResults.Keys | Sort-Object) {
    $catAcc = [Math]::Round($categoryResults[$cat].correct / $categoryResults[$cat].total * 100, 1)
    $color = if ($catAcc -ge 70) { "Green" } elseif ($catAcc -ge 50) { "Yellow" } else { "Red" }
    Write-Host "  $cat : $($categoryResults[$cat].correct)/$($categoryResults[$cat].total) ($catAcc%)" -ForegroundColor $color
}
Write-Host "`nReport: $reportDir\benchmark_report.json" -ForegroundColor Cyan
Write-Host "MLflow UI: $MLFLOW_TRACKING_URI" -ForegroundColor Cyan
Write-Host "`n? BENCHMARK COMPLETE" -ForegroundColor Green
