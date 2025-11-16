# Complete Step-by-Step Guide: Payment Integration with Python Requests

I'll give you a structured, progressive learning path. Follow each step in order.

---

## **PHASE 1: Understanding HTTP & Requests Library (Week 1)**

### Step 1: Install and Setup (Day 1)

```bash
# Open terminal on Kali Linux
mkdir ~/payment_integration_learning
cd ~/payment_integration_learning

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install requests python-decouple

# Create project structure
mkdir exercises
mkdir notes
touch notes/learning_log.txt
```

---

### Step 2: HTTP Basics (Day 1-2)

**Create: `exercises/01_http_basics.py`**

```python
"""
Understanding HTTP Methods:
- GET: Retrieve data (like checking booking status)
- POST: Send data (like creating a payment)
- PUT: Update data
- DELETE: Remove data
"""

import requests

# Test 1: Simple GET request
print("=== TEST 1: Basic GET ===")
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
print(f"Status Code: {response.status_code}")
print(f"Response Type: {type(response)}")
print(f"Response Text (first 100 chars): {response.text[:100]}")

# Test 2: Understanding response object
print("\n=== TEST 2: Response Object Properties ===")
print(f"Headers: {response.headers['content-type']}")
print(f"Encoding: {response.encoding}")
print(f"Status OK? {response.ok}")  # True if status < 400

# Test 3: JSON response
print("\n=== TEST 3: JSON Parsing ===")
data = response.json()  # Converts JSON string to Python dict
print(f"Type: {type(data)}")
print(f"Title: {data['title']}")
print(f"User ID: {data['userId']}")
```

**Run it:**
```bash
python exercises/01_http_basics.py
```

**Task:** Write in `notes/learning_log.txt`:
- What does status code 200 mean?
- What's the difference between `response.text` and `response.json()`?
- What happens if you call `.json()` on non-JSON content?

---

### Step 3: GET Requests with Parameters (Day 2-3)

**Create: `exercises/02_get_with_params.py`**

```python
"""
URL Parameters: Used to filter, search, or specify what data you want
Example: https://api.com/search?query=hotel&city=nairobi&page=1
"""

import requests

# Test 1: Manual URL parameters (BAD practice)
print("=== TEST 1: Manual Parameters ===")
url = "https://jsonplaceholder.typicode.com/comments?postId=1"
response = requests.get(url)
comments = response.json()
print(f"Found {len(comments)} comments")

# Test 2: Using params dict (GOOD practice)
print("\n=== TEST 2: Using params Dict ===")
base_url = "https://jsonplaceholder.typicode.com/comments"
params = {
    'postId': 1,
    'id': 1
}
response = requests.get(base_url, params=params)
print(f"Actual URL called: {response.url}")
print(f"Response: {response.json()}")

# Test 3: Multiple parameters
print("\n=== TEST 3: Complex Parameters ===")
params = {
    'userId': 1,
    '_limit': 5  # Limit results to 5
}
response = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)
posts = response.json()
print(f"Retrieved {len(posts)} posts")
for post in posts:
    print(f"- {post['title'][:50]}...")

# Test 4: Payment gateway style parameters
print("\n=== TEST 4: Payment Status Check Simulation ===")
# This is how you'd check payment status with Pesapal
payment_check_params = {
    'orderTrackingId': 'TRK123456',
    'merchantReference': 'BOOK001'
}
# In real scenario: response = requests.get(pesapal_status_url, params=payment_check_params)
print(f"Would check status with params: {payment_check_params}")
```

**Run and observe:**
```bash
python exercises/02_get_with_params.py
```

**Task:** Modify the script to:
1. Get posts for userId=2
2. Limit results to 3
3. Print only the titles

---

### Step 4: POST Requests - Sending Data (Day 3-4)

**Create: `exercises/03_post_requests.py`**

```python
"""
POST requests: Used to CREATE new resources
- Creating a payment
- Creating a booking
- Submitting a form
"""

import requests
import json

# Test 1: Simple POST with JSON
print("=== TEST 1: Creating a Post (JSON) ===")
new_post = {
    'title': 'Test Payment',
    'body': 'Learning to send data',
    'userId': 1
}

response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=new_post  # 'json=' automatically sets Content-Type header
)

print(f"Status: {response.status_code}")  # 201 = Created
print(f"Created resource: {response.json()}")

# Test 2: Understanding Content-Type
print("\n=== TEST 2: JSON vs Form Data ===")

# Method A: JSON (for APIs)
json_data = {'name': 'John', 'amount': 5000}
response_json = requests.post(
    'https://httpbin.org/post',
    json=json_data
)
print("JSON Content-Type:", response_json.request.headers['Content-Type'])

# Method B: Form data (for traditional forms)
form_data = {'name': 'John', 'amount': 5000}
response_form = requests.post(
    'https://httpbin.org/post',
    data=form_data
)
print("Form Content-Type:", response_form.request.headers['Content-Type'])

# Test 3: Simulating payment creation
print("\n=== TEST 3: Payment Request Simulation ===")
payment_request = {
    'id': 'BOOK12345',
    'currency': 'KES',
    'amount': 10000,
    'description': 'Hotel Booking - 3 nights',
    'callback_url': 'https://myhotel.com/payment/callback',
    'notification_id': 'IPN123',
    'billing_address': {
        'email_address': 'customer@example.com',
        'phone_number': '+254700000000',
        'country_code': 'KE',
        'first_name': 'John',
        'last_name': 'Doe'
    }
}

# This structure is similar to Pesapal's SubmitOrderRequest
print("Payment Payload:")
print(json.dumps(payment_request, indent=2))

# In real scenario:
# response = requests.post(pesapal_submit_url, json=payment_request, headers=headers)
response = requests.post('https://httpbin.org/post', json=payment_request)
print(f"\nStatus: {response.status_code}")
```

**Run it:**
```bash
python exercises/03_post_requests.py
```

**Task:** Create your own booking payload with:
- Customer details
- Booking dates
- Amount
- Service description

---

### Step 5: Headers and Authentication (Day 4-5)

**Create: `exercises/04_headers_auth.py`**

```python
"""
Headers: Metadata sent with requests
- Authentication tokens
- Content type
- User agent
- Custom headers
"""

import requests
import json
from datetime import datetime

# Test 1: Understanding Headers
print("=== TEST 1: Basic Headers ===")
headers = {
    'User-Agent': 'PaymentApp/1.0',
    'Accept': 'application/json',
    'X-Custom-Header': 'MyValue'
}

response = requests.get('https://httpbin.org/headers', headers=headers)
print("Headers sent:")
print(json.dumps(response.json(), indent=2))

# Test 2: Bearer Token Authentication (Most APIs use this)
print("\n=== TEST 2: Bearer Token Authentication ===")
# This is how Pesapal and most payment gateways work
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example.token"
auth_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.get('https://httpbin.org/bearer', headers=auth_headers)
print(f"Authenticated: {response.json()['authenticated']}")
print(f"Token: {response.json()['token'][:20]}...")

# Test 3: Basic Authentication
print("\n=== TEST 3: Basic Authentication ===")
response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    auth=('user', 'pass')  # requests handles encoding
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 4: Simulating Pesapal OAuth Flow
print("\n=== TEST 4: Pesapal-Style Authentication ===")

def get_pesapal_token(consumer_key, consumer_secret):
    """
    Simulates getting OAuth token from Pesapal
    Real endpoint: https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken
    """
    auth_url = "https://httpbin.org/post"  # Using httpbin for simulation
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    credentials = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret
    }
    
    print("Requesting token...")
    response = requests.post(auth_url, headers=headers, json=credentials)
    
    if response.status_code == 200:
        print("✅ Token received")
        # In real Pesapal: return response.json()['token']
        return "fake_token_for_practice"
    else:
        print("❌ Authentication failed")
        return None

# Simulate getting token
token = get_pesapal_token('fake_consumer_key', 'fake_consumer_secret')
print(f"Token: {token}")

# Test 5: Using token for subsequent requests
print("\n=== TEST 5: Using Token in Requests ===")
if token:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Now you can make authenticated requests
    payment_data = {
        'amount': 5000,
        'currency': 'KES'
    }
    
    response = requests.post(
        'https://httpbin.org/post',
        headers=headers,
        json=payment_data
    )
    print(f"Request successful: {response.status_code == 200}")
```

**Run it:**
```bash
python exercises/04_headers_auth.py
```

**Task:** 
1. What's the difference between Bearer token and Basic auth?
2. Where do you put the token in the request?
3. Write a function that stores and reuses a token

---

### Step 6: Error Handling (Day 5-6)

**Create: `exercises/05_error_handling.py`**

```python
"""
Error Handling: Critical for production payment systems
- Network errors
- Timeouts
- HTTP errors (4xx, 5xx)
- Invalid JSON
- Rate limiting
"""

import requests
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
    HTTPError,
    TooManyRedirects
)
import time

# Test 1: Handling Timeouts
print("=== TEST 1: Timeout Handling ===")
try:
    # This endpoint delays response by 5 seconds
    response = requests.get('https://httpbin.org/delay/5', timeout=2)
    print("Response received")
except Timeout:
    print("❌ Request timed out! Payment gateway is slow.")
    print("Action: Retry or inform user to wait")

# Test 2: Handling HTTP Errors
print("\n=== TEST 2: HTTP Error Handling ===")
try:
    response = requests.get('https://httpbin.org/status/404')
    response.raise_for_status()  # Raises HTTPError for bad status
    print("Success")
except HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    print(f"Status Code: {e.response.status_code}")
    if e.response.status_code == 404:
        print("Action: Endpoint not found, check URL")
    elif e.response.status_code == 401:
        print("Action: Re-authenticate")
    elif e.response.status_code == 500:
        print("Action: Payment gateway error, retry later")

# Test 3: Connection Errors
print("\n=== TEST 3: Connection Error Handling ===")
try:
    response = requests.get('https://thissitedoesnotexist12345.com', timeout=3)
except ConnectionError as e:
    print("❌ Connection Error: Cannot reach server")
    print("Action: Check internet connection or gateway status")

# Test 4: JSON Parsing Errors
print("\n=== TEST 4: JSON Parsing Error ===")
try:
    response = requests.get('https://httpbin.org/html')
    data = response.json()  # This will fail - response is HTML
except ValueError as e:
    print("❌ JSON Decode Error: Response is not valid JSON")
    print("Action: Check API documentation, log response text")

# Test 5: Complete Error Handling Pattern
print("\n=== TEST 5: Complete Error Handling ===")

def safe_api_call(url, method='GET', **kwargs):
    """
    Robust API call with complete error handling
    This is how you should call payment APIs
    """
    try:
        # Set default timeout if not provided
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
        
        # Make request
        if method == 'GET':
            response = requests.get(url, **kwargs)
        elif method == 'POST':
            response = requests.post(url, **kwargs)
        
        # Check status
        response.raise_for_status()
        
        # Try to parse JSON
        try:
            return {'success': True, 'data': response.json()}
        except ValueError:
            return {'success': True, 'data': response.text}
            
    except Timeout:
        return {'success': False, 'error': 'timeout', 'message': 'Request timed out'}
    
    except ConnectionError:
        return {'success': False, 'error': 'connection', 'message': 'Cannot connect to server'}
    
    except HTTPError as e:
        return {
            'success': False,
            'error': 'http_error',
            'status_code': e.response.status_code,
            'message': str(e)
        }
    
    except Exception as e:
        return {'success': False, 'error': 'unknown', 'message': str(e)}

# Test the safe function
print("\nTesting safe_api_call...")

# Success case
result = safe_api_call('https://jsonplaceholder.typicode.com/posts/1')
print(f"✅ Success: {result['success']}")

# Timeout case
result = safe_api_call('https://httpbin.org/delay/10', timeout=2)
print(f"❌ Timeout: {result}")

# 404 case
result = safe_api_call('https://httpbin.org/status/404')
print(f"❌ Not Found: {result}")

# Test 6: Retry Logic (Important for payments)
print("\n=== TEST 6: Retry Logic ===")

def api_call_with_retry(url, max_retries=3, delay=2):
    """
    Retry failed requests (useful for temporary network issues)
    """
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        
        except (Timeout, ConnectionError) as e:
            if attempt < max_retries - 1:
                print(f"Failed, retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return {'success': False, 'error': 'max_retries_exceeded'}
        
        except HTTPError as e:
            # Don't retry for client errors (4xx)
            if 400 <= e.response.status_code < 500:
                return {'success': False, 'error': 'client_error', 'status': e.response.status_code}
            # Retry for server errors (5xx)
            if attempt < max_retries - 1:
                print(f"Server error, retrying...")
                time.sleep(delay)
            else:
                return {'success': False, 'error': 'server_error'}

# Test retry with a flaky endpoint
result = api_call_with_retry('https://httpbin.org/status/200')
print(f"Result: {result['success']}")
```

**Run it:**
```bash
python exercises/05_error_handling.py
```

**Task:** 
1. Which errors should you retry?
2. Which errors should NOT be retried?
3. Write error handling for a payment timeout scenario

---

### Step 7: Complete Practice Script (Day 6-7)

**Create: `exercises/06_payment_simulation.py`**

```python
"""
Complete Payment Gateway Simulation
Combines everything you've learned
"""

import requests
import json
import uuid
from datetime import datetime
from typing import Dict, Optional

class PaymentGatewayClient:
    """
    Generic payment gateway client
    Demonstrates patterns used by Pesapal, DPO, Stripe, etc.
    """
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox
        self.base_url = self._get_base_url()
        self.token = None
        self.token_expiry = None
    
    def _get_base_url(self) -> str:
        """Different URLs for sandbox vs production"""
        if self.sandbox:
            return "https://httpbin.org"  # Using httpbin for practice
        return "https://api.production.com"
    
    def authenticate(self) -> bool:
        """
        Step 1: Get authentication token
        All payment gateways require this
        """
        print("\n🔐 Authenticating...")
        
        auth_url = f"{self.base_url}/post"  # Simulating auth endpoint
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        credentials = {
            'consumer_key': self.api_key,
            'consumer_secret': self.api_secret
        }
        
        try:
            response = requests.post(
                auth_url,
                headers=headers,
                json=credentials,
                timeout=10
            )
            response.raise_for_status()
            
            # In real Pesapal: self.token = response.json()['token']
            self.token = f"token_{uuid.uuid4().hex[:16]}"
            self.token_expiry = datetime.now()
            
            print(f"✅ Authenticated successfully")
            print(f"Token: {self.token}")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def create_payment(self, booking_data: Dict) -> Optional[Dict]:
        """
        Step 2: Create payment request
        Returns payment URL for customer
        """
        print("\n💳 Creating payment request...")
        
        if not self.token:
            print("❌ Not authenticated. Call authenticate() first")
            return None
        
        # Prepare payment payload
        payment_payload = {
            'id': str(uuid.uuid4()),
            'currency': booking_data.get('currency', 'KES'),
            'amount': booking_data['amount'],
            'description': booking_data['description'],
            'callback_url': booking_data['callback_url'],
            'notification_id': str(uuid.uuid4()),
            'billing_address': {
                'email_address': booking_data['customer_email'],
                'phone_number': booking_data.get('customer_phone'),
                'first_name': booking_data.get('customer_name', '').split()[0],
                'last_name': booking_data.get('customer_name', '').split()[-1] if ' ' in booking_data.get('customer_name', '') else '',
                'country_code': booking_data.get('country_code', 'KE')
            }
        }
        
        print(f"Payload:\n{json.dumps(payment_payload, indent=2)}")
        
        # Make API call
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/post",  # Simulating submit order endpoint
                headers=headers,
                json=payment_payload,
                timeout=15
            )
            response.raise_for_status()
            
            # Simulate response
            order_tracking_id = f"TRK_{uuid.uuid4().hex[:12].upper()}"
            merchant_reference = payment_payload['id']
            payment_url = f"https://sandbox.gateway.com/pay?id={order_tracking_id}"
            
            result = {
                'order_tracking_id': order_tracking_id,
                'merchant_reference': merchant_reference,
                'redirect_url': payment_url,
                'status': 'pending'
            }
            
            print(f"✅ Payment request created")
            print(f"Order Tracking ID: {order_tracking_id}")
            print(f"Payment URL: {payment_url}")
            
            return result
            
        except Exception as e:
            print(f"❌ Payment creation failed: {e}")
            return None
    
    def check_payment_status(self, order_tracking_id: str) -> Optional[Dict]:
        """
        Step 3: Check payment status
        Called after customer completes payment
        """
        print(f"\n🔍 Checking payment status for {order_tracking_id}...")
        
        if not self.token:
            print("❌ Not authenticated")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
        
        params = {
            'orderTrackingId': order_tracking_id
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/get",  # Simulating status endpoint
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            # Simulate successful payment
            status_result = {
                'order_tracking_id': order_tracking_id,
                'payment_status_description': 'Completed',
                'payment_method': 'M-Pesa',
                'amount': 10000,
                'currency': 'KES',
                'created_date': datetime.now().isoformat(),
                'confirmation_code': f"MPM{uuid.uuid4().hex[:10].upper()}"
            }
            
            print(f"✅ Status: {status_result['payment_status_description']}")
            print(f"Confirmation: {status_result['confirmation_code']}")
            
            return status_result
            
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return None
    
    def handle_callback(self, callback_data: Dict) -> Dict:
        """
        Step 4: Handle IPN/Callback
        Called by payment gateway after payment
        """
        print("\n📢 Received payment callback...")
        print(f"Callback data:\n{json.dumps(callback_data, indent=2)}")
        
        # Verify the callback (important for security)
        order_tracking_id = callback_data.get('OrderTrackingId')
        
        if not order_tracking_id:
            return {'verified': False, 'message': 'Missing tracking ID'}
        
        # Check actual status with gateway
        status = self.check_payment_status(order_tracking_id)
        
        if status and status['payment_status_description'] == 'Completed':
            return {
                'verified': True,
                'status': 'completed',
                'order_tracking_id': order_tracking_id
            }
        
        return {'verified': False, 'message': 'Payment not confirmed'}


# === MAIN SIMULATION ===
def main():
    print("=" * 60)
    print("PAYMENT GATEWAY INTEGRATION SIMULATION")
    print("=" * 60)
    
    # Initialize client
    gateway = PaymentGatewayClient(
        api_key='test_consumer_key_123',
        api_secret='test_consumer_secret_456',
        sandbox=True
    )
    
    # Step 1: Authenticate
    if not gateway.authenticate():
        print("Failed to authenticate. Exiting.")
        return
    
    # Step 2: Create payment
    booking = {
        'amount': 10000,
        'currency': 'KES',
        'description': 'Hotel Booking - Deluxe Room - 3 Nights',
        'callback_url': 'https://myhotel.com/api/payment/callback',
        'customer_email': 'john.doe@example.com',
        'customer_phone': '+254700000000',
        'customer_name': 'John Doe',
        'country_code': 'KE'
    }
    
    payment_result = gateway.create_payment(booking)
    
    if not payment_result:
        print("Failed to create payment. Exiting.")
        return
    
    # Step 3: Simulate user paying
    print("\n👤 Customer redirected to payment page...")
    print(f"URL: {payment_result['redirect_url']}")
    print("(User enters M-Pesa PIN and completes payment)")
    
    # Step 4: Simulate callback from gateway
    print("\n" + "=" * 60)
    callback_data = {
        'OrderTrackingId': payment_result['order_tracking_id'],
        'OrderMerchantReference': payment_result['merchant_reference'],
        'OrderNotificationType': 'IPNCHANGE',
        'OrderNotificationStatus': 'COMPLETED'
    }
    
    callback_result = gateway.handle_callback(callback_data)
    
    # Step 5: Final result
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    if callback_result['verified']:
        print("✅ Payment verified and completed!")
        print(f"Order ID: {callback_result['order_tracking_id']}")
        print("\nNext steps:")
        print("1. Update booking status in database")
        print("2. Send confirmation email to customer")
        print("3. Generate booking receipt/voucher")
    else:
        print("❌ Payment verification failed")
        print(f"Reason: {callback_result.get('message')}")
        print("\nNext steps:")
        print("1. Log the failure")
        print("2. Notify admin")
        print("3. Contact customer")

if __name__ == "__main__":
    main()
```

**Run it:**
```bash
python exercises/06_payment_simulation.py
```

---

## **PHASE 2: Real Pesapal Integration (Week 2)**

Now that you understand requests, let's work with real Pesapal API.

### Step 8: Pesapal Registration Setup (Day 8)

**Create: `exercises/07_pesapal_setup.py`**

```python
"""
Pesapal Sandbox Setup Check
Before integrating, verify your credentials work
"""

import requests
import json

# Your Pesapal sandbox credentials
PESAPAL_CONSUMER_KEY = "your_consumer_key_here"
PESAPAL_CONSUMER_SECRET = "your_consumer_secret_here"

# Pesapal sandbox URLs
AUTH_URL = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
REGISTER_IPN_URL = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"

def test_pesapal_auth():
    """Test if your credentials work"""
    print("Testing Pesapal Authentication...")
    print(f"Consumer Key: {PESAPAL_CONSUMER_KEY[:10]}...")
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'consumer_key': PESAPAL_CONSUMER_KEY,
        'consumer_secret': PESAPAL_CONSUMER_SECRET
    }
    
    try:
        response = requests.post(AUTH_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        token = data.get('token')
        
        if token:
            print("✅ Authentication successful!")
            print(f"Token (first 20 chars): {token[:20]}...")
            print(f"Token Type: {data.get('token_type')}")
            print(f"Expires In: {data.get('expiryDate')}")
            return token
        else:
            print("❌ No token received")
            return None
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("PESAPAL SANDBOX CONNECTION TEST")
    print("=" * 60)
    print("\n⚠️  Before running:")
    print("1. Register at https://developer.pesapal.com")
    print("2. Get your sandbox Consumer Key and Secret")
    print("3. Update them in this script\n")
    
    input("Press Enter to test connection...")
    
    token = test_pesapal_auth()
    
    if token:
        print("\n✅ You're ready for integration!")
        print("\nNext steps:")
        print("1. Register your IPN URL")
        print("2. Submit test payments")
        print("3. Handle callbacks")
    else:
        print("\n❌ Setup incomplete")
        print("Check:")
        print("- Are credentials correct?")
        print("- Is sandbox mode enabled in Pesapal dashboard?")
        print("- Internet connection working?")
```

**Task:**
1. Register at https://developer.pesapal.com
2. Get sandbox credentials
3. Update script with your credentials
4. Run the test

```bash
python exercises/07_pesapal_setup.py
```

---

**Want me to continue with:**
- Step 9: Register IPN URL
- Step 10: Create actual payment
- Step 11: Handle callbacks
- Step 12: Database integration with Django

Let me know if this step-by-step format works better