# PowerShell script to test the RAG API
param(
    [string]$Url = "https://bajajhack-production-cf2c.up.railway.app/hackrx/run",
    [int]$TimeoutSeconds = 300
)

Write-Host "=== Testing RAG API with PowerShell ===" -ForegroundColor Green

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

# Test main API endpoint
Write-Host "`n2. Testing main API endpoint..." -ForegroundColor Yellow

$headers = @{
    "accept" = "application/json"
    "Authorization" = "Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d"
    "Content-Type" = "application/json"
}

$body = @{
    documents = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    questions = @(
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
    )
} | ConvertTo-Json -Depth 10

Write-Host "Testing with 1 question and $TimeoutSeconds second timeout..." -ForegroundColor Cyan
Write-Host "URL: $Url" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri $Url -Method POST -Headers $headers -Body $body -TimeoutSec $TimeoutSeconds
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Success!" -ForegroundColor Green
        Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Error: $($response.StatusCode)" -ForegroundColor Red
        Write-Host "Response: $($response.Content)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Message -like "*timeout*") {
        Write-Host "The request timed out after $TimeoutSeconds seconds. Try increasing the timeout or reducing the number of questions." -ForegroundColor Yellow
    }
} 