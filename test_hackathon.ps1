# PowerShell script to test the RAG API with full hackathon questions
param(
    [string]$Url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run",
    [int]$TimeoutSeconds = 600
)

Write-Host "=== Testing RAG API with Full Hackathon Questions ===" -ForegroundColor Green

# Test health endpoint first
Write-Host "`n1. Testing health endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "https://bajajhack-production-cf2c.up.railway.app/health" -Method GET -TimeoutSec 10
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Health check passed" -ForegroundColor Green
        Write-Host "Response: $($healthResponse.Content)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Health check failed: $($healthResponse.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Health check error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test main API endpoint with full 10 questions
Write-Host "`n2. Testing with full 10 hackathon questions..." -ForegroundColor Yellow

$headers = @{
    "accept" = "application/json"
    "Authorization" = "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d"
    "Content-Type" = "application/json"
}

$body = @{
    documents = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    questions = @(
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "What are the coverage limits for different types of medical expenses under this policy?",
        "What is the policy term and renewal process for the National Parivar Mediclaim Plus Policy?",
        "What are the exclusions and limitations of coverage under this health insurance policy?",
        "What is the claim settlement process and required documentation for this policy?",
        "What are the premium payment options and frequency available under this policy?",
        "What is the coverage for hospitalization expenses and room rent limits?",
        "What are the benefits and coverage for outpatient treatment under this policy?",
        "What is the process for adding or removing family members from the policy coverage?"
    )
} | ConvertTo-Json -Depth 10

Write-Host "Testing with 10 questions and $TimeoutSeconds second timeout..." -ForegroundColor Cyan
Write-Host "URL: $Url" -ForegroundColor Cyan
Write-Host "Questions: $($body.questions.Count)" -ForegroundColor Cyan

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

try {
    $response = Invoke-WebRequest -Uri $Url -Method POST -Headers $headers -Body $body -TimeoutSec $TimeoutSeconds
    
    $stopwatch.Stop()
    $totalTime = $stopwatch.Elapsed.TotalSeconds
    $avgTimePerQuestion = $totalTime / 10
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Success!" -ForegroundColor Green
        Write-Host "Total processing time: $($totalTime.ToString('F2')) seconds" -ForegroundColor Green
        Write-Host "Average time per question: $($avgTimePerQuestion.ToString('F2')) seconds" -ForegroundColor Green
        Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Error: $($response.StatusCode)" -ForegroundColor Red
        Write-Host "Response: $($response.Content)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Message -like "*timeout*") {
        Write-Host "The request timed out after $TimeoutSeconds seconds. The system may need optimization for 10 questions." -ForegroundColor Yellow
    }
} finally {
    $stopwatch.Stop()
} 