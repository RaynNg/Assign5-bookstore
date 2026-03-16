#!/bin/bash
# Test all API endpoints through API Gateway

echo "Testing Admin Dashboard API Endpoints..."
echo "========================================="

# Array of endpoints to test
endpoints=(
    "/api/catalogs/catalogs/"
    "/api/books/books/"
    "/api/customers/customers/"
    "/api/staff/staff/"
    "/api/managers/managers/"
    "/api/carts/carts/"
    "/api/orders/orders/"
    "/api/payments/payments/"
    "/api/shipments/shipments/"
    "/api/comments/comments/"
)

names=(
    "Catalogs"
    "Books"
    "Customers"
    "Staff"
    "Managers"
    "Carts"
    "Orders"
    "Payments"
    "Shipments"
    "Comments"
)

BASE_URL="http://localhost:8000"
success=0
failed=0

for i in "${!endpoints[@]}"; do
    endpoint="${endpoints[$i]}"
    name="${names[$i]}"
    
    echo -n "Testing $name ($endpoint)... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${endpoint}")
    
    if [ "$response" -eq 200 ]; then
        echo "✅ OK"
        ((success++))
    else
        echo "❌ FAILED (HTTP $response)"
        ((failed++))
    fi
done

echo ""
echo "========================================="
echo "Results: $success passed, $failed failed"
echo "========================================="

if [ $failed -eq 0 ]; then
    echo "✅ All API endpoints are working!"
    exit 0
else
    echo "❌ Some endpoints failed. Please check the logs."
    exit 1
fi
