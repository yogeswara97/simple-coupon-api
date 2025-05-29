from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
COUPONS_FILE = 'coupons.json'


# Helper
def load_coupons():
    if not os.path.exists(COUPONS_FILE):
        return []
    with open(COUPONS_FILE, 'r') as f:
        return json.load(f)

def save_coupons(coupons):
    with open(COUPONS_FILE, 'w') as f:
        json.dump(coupons, f, indent=2)

# Routes

@app.route('/admin/create-coupon', methods=['POST'])
def create_coupon():
    new_coupon = request.json
    coupons = load_coupons()

    if any(c['code'] == new_coupon['code'] for c in coupons):
        return jsonify({"error": "Coupon code already exists"}), 400

    new_coupon['used'] = 0
    coupons.append(new_coupon)
    save_coupons(coupons)
    return jsonify({"message": "Coupon created successfully"})

@app.route('/admin/coupons', methods=['GET'])
def list_coupons():
    coupons = load_coupons()
    return jsonify(coupons)

@app.route('/apply-coupon', methods=['POST'])
def apply_coupon():
    data = request.json
    coupons = load_coupons()
    code = data.get("code")
    amount = data.get("amount")

    coupon = next((c for c in coupons if c["code"] == code), None)
    print(coupon)
    if not coupon:
        return jsonify({"valid": False, "reason": "Coupon not found"})

    if datetime.strptime(coupon["expires_at"], "%Y-%m-%dT%H:%M:%S") < datetime.now():
        return jsonify({"valid": False, "reason": "Coupon expired"})

    if coupon.get("usage_limit") is not None and coupon["used"] >= coupon["usage_limit"]:
        return jsonify({"valid": False, "reason": "Usage limit reached"})

    if coupon["discount_type"] == "percentage":
        discount = amount * (coupon["value"] / 100)
    elif coupon["discount_type"] == "fixed":
        discount = coupon["value"]
    else:
        return jsonify({"valid": False, "reason": "Invalid discount type"})

    final_amount = max(amount - discount, 0)
    coupon["used"] += 1
    save_coupons(coupons)

    return jsonify({
        "valid": True,
        "original_amount": amount,
        "final_amount": final_amount,
        "applied_discount": discount
    })

if __name__ == '__main__':
    app.run(debug=True)
