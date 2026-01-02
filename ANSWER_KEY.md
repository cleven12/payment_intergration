# 🎓 Exercise Answer Key

## Exercise 1: Authentication

### TODO 1: Base URLs
```python
if environment == 'sandbox':
    self.base_url = "https://cybqa.pesapal.com/pesapalv3"
else:
    self.base_url = "https://pay.pesapal.com/v3"
```

### TODO 3: Payload
```python
payload = {
    "consumer_key": self.consumer_key,
    "consumer_secret": self.consumer_secret
}
```

### TODO 4: Headers
```python
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
```

### TODO 6: Extract Token
```python
self.token = data.get('token')
```

### TODO 7: Token Validation
```python
return now < (expiry - buffer)
```

### Challenge Answers

**Q1: Why short-lived tokens?**
> Security! If a token is stolen, the attacker only has 5 minutes to use it. This limits the damage from compromised credentials and follows the principle of least privilege.

**Q2: What if we don't check expiry?**
> Our API calls will fail with 401 Unauthorized errors. The application will break, and users won't be able to make payments. Always check and refresh tokens proactively!

**Q3: Redis caching?**
```python
import redis

class RedisTokenManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
    
    def save_token(self, token, expiry):
        # Calculate TTL (time to live)
        ttl = int((expiry - datetime.now()).total_seconds())
        self.redis.setex('pesapal_token', ttl, token)
    
    def get_token(self):
        token = self.redis.get('pesapal_token')
        return token.decode() if token else None
```

**Q4: GET vs POST?**
> - **GET**: Retrieves data, parameters in URL, can be cached, safe/idempotent
> - **POST**: Sends data, parameters in body, not cached, can modify server state

**Q5: raise_for_status()?**
> It raises an HTTPError exception for 4xx/5xx status codes. This helps catch API errors early instead of treating them as successful responses.

---

## Exercise 2: IPN Handler

### TODO 1: Extract Parameters
```python
if request.method == 'POST':
    data = json.loads(request.body)
else:  # GET
    data = {
        'OrderTrackingId': request.GET.get('OrderTrackingId'),
        'OrderMerchantReference': request.GET.get('OrderMerchantReference'),
        'OrderNotificationType': request.GET.get('OrderNotificationType')
    }
```

### TODO 2: Verify Payment
```python
status_data = self.api.get_transaction_status(order_tracking_id)
```

### TODO 3: Extract Payment Details
```python
status = payment_data.get('payment_status_description')
payment_method = payment_data.get('payment_method')
confirmation_code = payment_data.get('confirmation_code')
```

### TODO 6: Create Response
```python
'status': 200 if success else 500
```

### Challenge Answers

**Q1: Why verify instead of trusting IPN?**
> Security! Someone could fake an IPN request to mark unpaid orders as completed. Always verify directly with Pesapal's API - it's the single source of truth.

**Q2: IPNCHANGE vs CALLBACKURL?**
> - **IPNCHANGE**: Server-to-server notification (IPN), runs in background
> - **CALLBACKURL**: Customer's browser redirect, shows them a page
> IPN is more reliable because it doesn't depend on the customer's internet connection.

**Q3: Why idempotent?**
> Pesapal may retry IPN calls if they don't get a 200 response. Your endpoint should handle the same notification multiple times without creating duplicate records or double-charging customers.

**Q4: Prevent duplicate processing?**
```python
# Check if already processed
processed = ProcessedIPN.objects.filter(
    order_tracking_id=tracking_id
).exists()

if processed:
    return JsonResponse({'status': 200})  # Already handled

# Process and mark as done
process_payment(tracking_id)
ProcessedIPN.objects.create(order_tracking_id=tracking_id)
```

**Q5: Pesapal retry on 500?**
> Yes! Pesapal will retry IPN calls if they get 500 errors or timeouts. This is good - it ensures you don't miss payment notifications even if your server is temporarily down.

---

## Exercise 3: Complete Integration

### TODO 1: Create Table
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant_reference TEXT UNIQUE NOT NULL,
        order_tracking_id TEXT,
        amount REAL NOT NULL,
        currency TEXT NOT NULL,
        customer_name TEXT,
        customer_email TEXT,
        customer_phone TEXT,
        description TEXT,
        status TEXT DEFAULT 'PENDING',
        payment_method TEXT,
        confirmation_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
```

### TODO 2: Insert Payment
```python
cursor.execute('''
    INSERT INTO payments 
    (merchant_reference, order_tracking_id, amount, currency, 
     customer_name, customer_email, customer_phone, description, 
     status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
''', (
    kwargs['merchant_reference'],
    kwargs['order_tracking_id'],
    kwargs['amount'],
    kwargs['currency'],
    kwargs['customer_name'],
    kwargs['customer_email'],
    kwargs['customer_phone'],
    kwargs['description'],
    'PENDING'
))
```

### TODO 3: Update Payment
```python
def update_payment(self, order_tracking_id, status, payment_method, confirmation_code):
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE payments 
        SET status = ?, payment_method = ?, confirmation_code = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE order_tracking_id = ?
    ''', (status, payment_method, confirmation_code, order_tracking_id))
    
    conn.commit()
    conn.close()
```

### TODO 9: Order Payload
```python
# Split name
name_parts = customer_name.split(' ', 1)
first_name = name_parts[0]
last_name = name_parts[1] if len(name_parts) > 1 else ''

order_payload = {
    "id": merchant_reference,
    "currency": currency,
    "amount": float(amount),
    "description": description,
    "callback_url": callback_url,
    "notification_id": ipn_id,
    "billing_address": {
        "email_address": customer_email,
        "phone_number": customer_phone,
        "country_code": "TZ",  # Or get from user
        "first_name": first_name,
        "last_name": last_name,
        "line_1": "Safari Tour Booking",
        "city": "Dar es Salaam"
    }
}
```

---

## Bonus: Production-Ready Code Template

```python
"""
Production-Ready Pesapal Integration
====================================
"""

import os
import logging
from functools import wraps
import requests
from datetime import datetime, timedelta
from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pesapal.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=3, delay=2):
    """Decorator to retry failed API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        logger.error(f"{func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    
                    wait_time = delay * (2 ** attempt)
                    logger.warning(f"{func.__name__} attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator


class PesapalService:
    """Production-ready Pesapal service"""
    
    def __init__(self):
        # Load from environment
        self.consumer_key = config('PESAPAL_CONSUMER_KEY')
        self.consumer_secret = config('PESAPAL_CONSUMER_SECRET')
        self.environment = config('PESAPAL_ENVIRONMENT', default='sandbox')
        
        # Set base URL
        if self.environment == 'live':
            self.base_url = "https://pay.pesapal.com/v3"
        else:
            self.base_url = "https://cybqa.pesapal.com/pesapalv3"
        
        self.token = None
        self.token_expiry = None
        
        logger.info(f"Initialized Pesapal service (environment: {self.environment})")
    
    @retry_on_failure(max_retries=3)
    def authenticate(self):
        """Authenticate with retry logic"""
        url = f"{self.base_url}/api/Auth/RequestToken"
        
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        logger.info("Authenticating with Pesapal...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') == '200':
            self.token = data.get('token')
            expiry_str = data.get('expiryDate')
            self.token_expiry = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            
            logger.info(f"Authentication successful, token expires at {self.token_expiry}")
            return self.token
        else:
            error_msg = data.get('message', 'Unknown error')
            logger.error(f"Authentication failed: {error_msg}")
            raise Exception(f"Authentication failed: {error_msg}")
    
    def get_headers(self):
        """Get headers with valid token"""
        # Check if token needs refresh
        if not self.token or not self.token_expiry:
            self.authenticate()
        elif datetime.now() >= (self.token_expiry.replace(tzinfo=None) - timedelta(seconds=30)):
            logger.info("Token expired, refreshing...")
            self.authenticate()
        
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    @retry_on_failure(max_retries=3)
    def submit_order(self, order_data):
        """Submit order with retry and logging"""
        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        
        logger.info(f"Submitting order: {order_data.get('id')}")
        
        try:
            response = requests.post(
                url,
                json=order_data,
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '200':
                logger.info(f"Order submitted successfully: {data.get('order_tracking_id')}")
                return data
            else:
                error_msg = data.get('message', 'Unknown error')
                logger.error(f"Order submission failed: {error_msg}")
                return None
                
        except Exception as e:
            logger.error(f"Order submission error: {str(e)}")
            raise
    
    def get_transaction_status(self, order_tracking_id):
        """Get transaction status with logging"""
        url = f"{self.base_url}/api/Transactions/GetTransactionStatus"
        
        params = {"orderTrackingId": order_tracking_id}
        
        logger.info(f"Checking status for: {order_tracking_id}")
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.get_headers(),
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '200':
                status = data.get('payment_status_description')
                logger.info(f"Transaction status: {status}")
                return data
            else:
                logger.error(f"Status check failed for {order_tracking_id}")
                return None
                
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return None


# Usage
if __name__ == "__main__":
    service = PesapalService()
    
    # Create order
    order = {
        "id": f"TOUR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "amount": 1500.00,
        "currency": "KES",
        # ... rest of order data
    }
    
    result = service.submit_order(order)
    
    if result:
        print(f"Payment URL: {result['redirect_url']}")
```

---

## Key Takeaways

1. **Always validate input** - Never trust user input or external data
2. **Use environment variables** - Never hardcode credentials
3. **Implement retry logic** - Network failures happen
4. **Log everything** - Future you will thank present you
5. **Handle errors gracefully** - Don't let users see stack traces
6. **Verify with source of truth** - Always check with Pesapal API
7. **Make it idempotent** - Same request = same result
8. **Test edge cases** - Expired tokens, network failures, duplicates
9. **Monitor in production** - Track success rates and errors
10. **Document your code** - Help your team understand it

---

**You're now ready to build production-grade payment integrations! 🚀**
