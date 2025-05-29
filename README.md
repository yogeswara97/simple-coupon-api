# Coupon Promo Service

## Overview
A lightweight Flask API for managing e-commerce promotion coupons. Admins create coupons; users apply them at checkout. Supports expiration dates and usage limits (-1 for unlimited).

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yogeswara97/simlple-coupon-api.git
   cd coupon-promo-service
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
   API runs at: `http://localhost:5000`

## API Endpoints

### 1. Create Coupon (Admin)
- **URL**: `/admin/create-coupon`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body Example**:
  ```json
  {
    "code": "SUMMER2025",
    "discount_type": "percentage",
    "value": 15,
    "expires_at": "2025-08-31T23:59:59",
    "usage_limit": 10
  }
  ```
- **Success Response**:
  ```json
  {
    "message": "Coupon created successfully"
  }
  ```

### 2. Apply Coupon (User)
- **URL**: `/apply-coupon`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body Example**:
  ```json
  {
    "amount": 50000,
    "code": "SUMMER2025"
  }
  ```
- **Success Response**:
  ```json
  {
    "valid": true,
    "original_amount": 50000,
    "final_amount": 42500,
    "applied_discount": 7500
  }
  ```
- **Failure Response** (example):
  ```json
  {
    "valid": false,
    "reason": "Coupon expired"
  }
  ```

## Data Storage
- Coupons stored locally in `coupons.json` as a JSON array.
- No external database required.

## Notes
- Use `"usage_limit": -1` for unlimited coupon usage.
- Supported discount types: `"percentage"`, `"fixed"`.
