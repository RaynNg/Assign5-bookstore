# Test all API endpoints through API Gateway
Write-Host "Testing Admin Dashboard API Endpoints..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$endpoints = @(
    @{Name="Catalogs"; Path="/api/catalogs/catalogs/"},
    @{Name="Books"; Path="/api/books/books/"},
    @{Name="Customers"; Path="/api/customers/customers/"},
    @{Name="Staff"; Path="/api/staff/staff/"},
    @{Name="Managers"; Path="/api/managers/managers/"},
    @{Name="Carts"; Path="/api/carts/carts/"},
    @{Name="Orders"; Path="/api/orders/orders/"},
    @{Name="Payments"; Path="/api/payments/payments/"},
    @{Name="Shipments"; Path="/api/shipments/shipments/"},
    @{Name="Comments"; Path="/api/comments/comments/"}
)

$baseUrl = "http://localhost:8000"
$success = 0
$failed = 0

foreach ($endpoint in $endpoints) {
    Write-Host "Testing $($endpoint.Name) ($($endpoint.Path))... " -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri "$baseUrl$($endpoint.Path)" -Method Get -TimeoutSec 5 -ErrorAction Stop
        
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ OK" -ForegroundColor Green
            $success++
        } else {
            Write-Host "❌ FAILED (HTTP $($response.StatusCode))" -ForegroundColor Red
            $failed++
        }
    }
    catch {
        Write-Host "❌ FAILED ($($_.Exception.Message))" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Results: $success passed, $failed failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "=========================================" -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host "✅ All API endpoints are working!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Some endpoints failed. Please check the logs." -ForegroundColor Red
    exit 1
}
