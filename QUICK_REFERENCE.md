# 🎓 Pesapal Quick Reference Guide

## For Quick Lookup During Development

---

## 🔑 API Endpoints

### Sandbox (Testing)
```
Base URL: https://cybqa.pesapal.com/pesapalv3
```

### Production (Live)
```
Base URL: https://pay.pesapal.com/v3
```

### Endpoint List
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/Auth/RequestToken` | POST | Get access token |
| `/api/URLSetup/RegisterIPN` | POST | Register IPN URL |
| `/api/URLSetup/GetIpnList` | GET | List registered IPNs |
| `/api/Transactions/SubmitOrderRequest` | POST | Create payment order |
| `/api/Transactions/GetTransactionStatus` | GET | Check payment status |
| `/api/Transactions/RefundRequest` | POST | Request refund |
| `/api/Transactions/CancelOrder` | POST | Cancel order |

---

## 🔐 Authentication

### Request
```python
url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "consumer_key": "YOUR_KEY",
    "consumer_secret": "YOUR_SECRET"
}

response = requests.post(url, json=payload, headers=headers)
```

### Response
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiryDate": "2026-01-01T12:30:00.000Z",
    "status": "200",
    "message": "Request processed successfully"
}
```

### Using Token
```python
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
```

**⚠️ Important**: Token expires in 5 minutes!

---

## 📡 IPN Registration

### Request
```python
url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"

payload = {
    "url": "https://yourdomain.com/ipn",
    "ipn_notification_type": "POST"  # or "GET"
}

response = requests.post(url, json=payload, headers=headers)
```

### Response
```json
{
    "url": "https://yourdomain.com/ipn",
    "ipn_id": "84740ab4-3cd9-47da-8a4f-dd1db53494b5",
    "ipn_notification_type_description": "POST",
    "status": "200"
}
```

**💾 Save the `ipn_id`** - you'll need it for every order!

---

## 💳 Submit Order

### Request
```python
url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"

payload = {
    "id": "TOUR-20260101123456",  # YOUR unique reference
    "currency": "KES",
    "amount": 1500.00,
    "description": "Kilimanjaro 7-Day Trek",
    "callback_url": "https://yourdomain.com/callback",
    "notification_id": "84740ab4-3cd9-47da-8a4f-dd1db53494b5",  # IPN ID
    "billing_address": {
        "email_address": "customer@example.com",
        "phone_number": "+254712345678",
        "country_code": "KE",
        "first_name": "John",
        "last_name": "Doe"
    }
}

response = requests.post(url, json=payload, headers=headers)
```

### Response
```json
{
    "order_tracking_id": "b945e4af-80a5-4ec1-8706-e03f8332fb04",
    "merchant_reference": "TOUR-20260101123456",
    "redirect_url": "https://cybqa.pesapal.com/pesapaliframe/...",
    "status": "200"
}
```

**👉 Redirect customer to `redirect_url` to complete payment**

---

## ✅ Check Payment Status

### Request
```python
url = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus"

params = {
    "orderTrackingId": "b945e4af-80a5-4ec1-8706-e03f8332fb04"
}

response = requests.get(url, params=params, headers=headers)
```

### Response
```json
{
    "payment_method": "M-Pesa",
    "amount": 1500,
    "created_date": "2026-01-01T12:41:09.763",
    "confirmation_code": "ABC123XYZ789",
    "payment_status_description": "Completed",
    "status_code": 1,
    "merchant_reference": "TOUR-20260101123456",
    "currency": "KES",
    "status": "200"
}
```

---

## 🔔 IPN Notification

### What Pesapal Sends (GET)
```
https://yourdomain.com/ipn?OrderTrackingId=b945e4af-80a5-4ec1-8706-e03f8332fb04&OrderMerchantReference=TOUR-20260101123456&OrderNotificationType=IPNCHANGE
```

### What Pesapal Sends (POST)
```json
{
    "OrderTrackingId": "b945e4af-80a5-4ec1-8706-e03f8332fb04",
    "OrderMerchantReference": "TOUR-20260101123456",
    "OrderNotificationType": "IPNCHANGE"
}
```

### What You Should Respond
```json
{
    "orderNotificationType": "IPNCHANGE",
    "orderTrackingId": "b945e4af-80a5-4ec1-8706-e03f8332fb04",
    "orderMerchantReference": "TOUR-20260101123456",
    "status": 200
}
```

**⚠️ Always verify status with Pesapal API - don't trust IPN parameters alone!**

---

## 📊 Payment Status Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | INVALID | Something went wrong |
| 1 | COMPLETED | ✅ Payment successful |
| 2 | FAILED | ❌ Payment rejected |
| 3 | REVERSED | 🔄 Payment refunded |

---

## 🌍 Test Credentials

### Kenya Merchant
```python
consumer_key = "qkio1BGGYAXTu2JOfm7XSXNruoZsrqEW"
consumer_secret = "osGQ364R49cXKeOYSpaOnT++rHs="
```

### Tanzania Merchant
```python
consumer_key = "ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8"
consumer_secret = "q27RChYs5UkypdcNYKzuUw460Dg="
```

### Uganda Merchant
```python
consumer_key = "TDpigBOOhs+zAl8cwH2Fl82jJGyD8xev"
consumer_secret = "1KpqkfsMaihIcOlhnBo/gBZ5smw="
```

**🚨 These are for SANDBOX only - never use in production!**

---

## 💰 Currency Codes

| Country | Code |
|---------|------|
| Kenya | KES |
| Tanzania | TZS |
| Uganda | UGX |
| Rwanda | RWF |
| Malawi | MWK |
| Zambia | ZMW |
| Zimbabwe | ZWL |
| US Dollar | USD |

---

## 🌐 Country Codes (ISO 3166-1)

| Country | Code |
|---------|------|
| Kenya | KE |
| Tanzania | TZ |
| Uganda | UG |
| Rwanda | RW |
| Malawi | MW |
| Zambia | ZM |
| Zimbabwe | ZW |

---

## 🔧 Testing with ngrok

### Install ngrok
```bash
# Download from https://ngrok.com/download
# Or use snap on Linux
sudo snap install ngrok
```

### Start ngrok tunnel
```bash
ngrok http 8000
```

### Output
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

**Use the HTTPS URL for IPN and callback URLs!**

---

## 🐛 Common Errors & Solutions

### Error: "Invalid consumer credentials"
**Solution**: Check your consumer_key and consumer_secret

### Error: "Token expired"
**Solution**: Re-authenticate before making API calls

### Error: "Invalid IPN ID"
**Solution**: Register IPN URL first, use the returned ipn_id

### Error: "Duplicate merchant reference"
**Solution**: Each order must have a unique merchant reference

### Error: "IPN URL not reachable"
**Solution**: 
- Use public URL (ngrok for local testing)
- Use HTTPS (not HTTP)
- Ensure no firewall blocking Pesapal

### Error: "Amount must be positive"
**Solution**: Check amount is float/decimal and > 0

---

## 📝 Code Snippets

### Generate Unique Merchant Reference
```python
from datetime import datetime
import uuid

# Option 1: Timestamp-based
merchant_ref = f"TOUR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
# Result: TOUR-20260101123456

# Option 2: UUID-based
merchant_ref = f"TOUR-{uuid.uuid4().hex[:10].upper()}"
# Result: TOUR-A1B2C3D4E5
```

### Token Management
```python
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry = None
    
    def is_valid(self):
        if not self.token or not self.expiry:
            return False
        return datetime.now() < (self.expiry - timedelta(seconds=30))
    
    def get_token(self):
        if not self.is_valid():
            self.refresh_token()
        return self.token
```

### IPN Handler Template
```python
@csrf_exempt
def ipn_handler(request):
    # 1. Extract parameters
    if request.method == 'POST':
        data = json.loads(request.body)
    else:
        data = request.GET
    
    tracking_id = data.get('OrderTrackingId')
    
    # 2. Verify with Pesapal
    status = check_payment_status(tracking_id)
    
    # 3. Update database
    update_payment(tracking_id, status)
    
    # 4. Respond
    return JsonResponse({
        'orderTrackingId': tracking_id,
        'status': 200
    })
```

### Database Model (Django)
```python
class Payment(models.Model):
    merchant_reference = models.CharField(max_length=50, unique=True)
    order_tracking_id = models.CharField(max_length=100, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, default='PENDING')
    confirmation_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 📞 Support Resources

- **Documentation**: https://developer.pesapal.com
- **Postman**: https://documenter.getpostman.com/view/6715320/UyxepTv1
- **Forum**: https://developer.pesapal.com/forum
- **Email**: developers@pesapal.com

---

## ✅ Pre-Production Checklist

- [ ] Switch to production credentials
- [ ] Change base_url to live environment
- [ ] Use HTTPS for all URLs (IPN, callback)
- [ ] Register production IPN URL
- [ ] Test with small amount first
- [ ] Set up error logging
- [ ] Set up monitoring/alerts
- [ ] Document API credentials location
- [ ] Review security (no credentials in code)
- [ ] Test error scenarios

---

## 🎯 Key Concepts to Master

1. **Authentication Flow**: Token-based, 5-minute expiry
2. **IPN vs Callback**: Server-to-server vs client-side
3. **Payment Lifecycle**: PENDING → COMPLETED/FAILED → REVERSED
4. **Idempotency**: Same request multiple times = same result
5. **Status Verification**: Always verify with Pesapal API
6. **Error Handling**: Retry logic, graceful degradation
7. **Security**: HTTPS, input validation, no credentials in code

---

**Last Updated**: January 2026  
**Version**: 1.0
