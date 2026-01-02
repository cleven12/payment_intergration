# 🚀 Complete Pesapal Payment Integration Tutorial
## From Beginner to Senior Developer Level

**Author**: Your Learning Guide  
**Date**: January 2026  
**Target**: CS Students with Django, Python, MySQL & Web Dev Skills

---

## 📚 Table of Contents

1. [What is Pesapal?](#what-is-pesapal)
2. [Core Concepts You Must Understand](#core-concepts)
3. [The 5-Step Payment Flow](#payment-flow)
4. [Hands-On: Building Your First Integration](#hands-on)
5. [Advanced Topics](#advanced-topics)
6. [Common Interview Questions](#interview-questions)
7. [Real-World Scenarios](#real-world-scenarios)

---

## 🎯 What is Pesapal?

### Simple Explanation
Imagine you're selling safari tour packages online. Your customer wants to pay with:
- M-Pesa (Kenya)
- Airtel Money (Tanzania)
- Visa/Mastercard

**Pesapal is the middleman** that handles ALL these payment methods for you. You don't need separate integrations for each payment type!

### Why East Africa Loves Pesapal
- ✅ Supports **mobile money** (M-Pesa, Airtel, Tigo, MTN)
- ✅ Supports **international cards** (Visa, Mastercard)
- ✅ Works in **7+ countries** (Kenya, Tanzania, Uganda, Rwanda, etc.)
- ✅ PCI-DSS compliant (bank-level security)
- ✅ Handles currency conversion automatically

### Real-World Example
```
Your Tour Website → Pesapal → Payment Provider (M-Pesa/Bank) → Customer's Account
                        ↓
                   Money to YOUR account
```

---

## 🧠 Core Concepts You Must Understand

### 1. **Authentication vs Authorization**
This confuses many juniors!

**Authentication** = "Who are you?"  
**Authorization** = "What can you do?"

```python
# Authentication: Prove you're a valid merchant
credentials = {
    "consumer_key": "your_key",
    "consumer_secret": "your_secret"
}
# Pesapal says: "OK, you're merchant ABC123"

# Authorization: Get permission to make API calls
token = authenticate(credentials)
# Pesapal says: "Here's a token. Use it for 5 minutes to call our APIs"
```

**Key Point**: Tokens expire in 5 minutes! Always check before making API calls.

---

### 2. **IPN (Instant Payment Notification)**
This is THE most important concept for payment systems!

#### The Problem Without IPN
```
Customer pays → Internet dies → Your site never knows payment succeeded → Customer angry!
```

#### The Solution With IPN
```
Customer pays → Pesapal PUSHES notification to YOUR server → You get notified even if customer's internet dies
```

**Real-World Analogy**:
- **Callback URL** = Customer saying "I paid!" (unreliable - they might lie or disconnect)
- **IPN URL** = Bank manager calling YOU directly to confirm payment (reliable!)

#### IPN Types
```python
# GET IPN - Parameters in URL
https://yoursite.com/ipn?OrderTrackingId=ABC123&status=COMPLETED

# POST IPN - Parameters in request body (more secure)
{
    "OrderTrackingId": "ABC123",
    "OrderMerchantReference": "TOUR-12345",
    "OrderNotificationType": "IPNCHANGE"
}
```

**Best Practice**: Always use POST for production (more secure than GET).

---

### 3. **The Three Types of IDs**
Beginners mix these up all the time!

| ID Type | Created By | Purpose | Example |
|---------|-----------|---------|---------|
| **Merchant Reference** | YOUR system | Your internal order ID | `TOUR-20260101-12345` |
| **Order Tracking ID** | Pesapal | Pesapal's tracking number | `b945e4af-80a5-4ec1-8706-e03f8332fb04` |
| **IPN ID** | Pesapal | Links to your IPN URL | `fe078e53-78da-4a83-aa89-e7ded5c456e6` |

**Database Design Tip**:
```sql
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    merchant_reference VARCHAR(50) UNIQUE,  -- YOUR ID
    order_tracking_id VARCHAR(100),         -- PESAPAL ID
    amount DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP
);
```

---

### 4. **Payment Status Flow**
Understanding this prevents 90% of beginner bugs!

```
PENDING → (customer paying) → COMPLETED ✅
                            → FAILED ❌
                            → INVALID ⚠️

COMPLETED → (dispute filed) → REVERSED 🔄
```

**Status Codes**:
- `0` = INVALID (something went wrong)
- `1` = COMPLETED (money received!)
- `2` = FAILED (payment rejected)
- `3` = REVERSED (refund issued)

---

## 🔄 The 5-Step Payment Flow

Every Pesapal integration follows this exact flow:

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: AUTHENTICATE                                           │
│  Get access token (valid 5 minutes)                             │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: REGISTER IPN                                           │
│  Tell Pesapal where to send payment notifications               │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: SUBMIT ORDER                                           │
│  Create payment request, get redirect URL                       │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: CUSTOMER PAYS                                          │
│  Customer redirected to Pesapal, chooses payment method         │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: VERIFY STATUS                                          │
│  IPN triggered → Check status → Update your database            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Hands-On: Building Your First Integration

### Project: Safari Tour Booking System

We'll build a complete payment system step-by-step.

### Phase 1: Environment Setup

```bash
# 1. Create project directory
mkdir pesapal_tutorial
cd pesapal_tutorial

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install requests python-decouple
pip freeze > requirements.txt

# 4. Create .env file
touch .env
```

**Add to `.env`**:
```bash
# Sandbox Credentials (Tanzania Merchant)
PESAPAL_CONSUMER_KEY=ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8
PESAPAL_CONSUMER_SECRET=q27RChYs5UkypdcNYKzuUw460Dg=
PESAPAL_ENVIRONMENT=sandbox

# Your URLs (use ngrok for testing)
SITE_URL=https://your-ngrok-url.ngrok-free.app
IPN_URL=https://your-ngrok-url.ngrok-free.app/ipn
CALLBACK_URL=https://your-ngrok-url.ngrok-free.app/callback
```

---

### Phase 2: Step-by-Step Implementation

#### **Step 1: Authentication** 🔐

Create `pesapal_auth.py`:

```python
"""
Step 1: Authentication
====================
Purpose: Get access token to call Pesapal APIs
Token expires in 5 minutes - must refresh!
"""

import requests
import os
from datetime import datetime, timedelta
from decouple import config

class PesapalAuth:
    """Handles Pesapal authentication"""
    
    def __init__(self):
        self.consumer_key = config('PESAPAL_CONSUMER_KEY')
        self.consumer_secret = config('PESAPAL_CONSUMER_SECRET')
        self.environment = config('PESAPAL_ENVIRONMENT', default='sandbox')
        
        # Choose correct base URL
        if self.environment == 'sandbox':
            self.base_url = "https://cybqa.pesapal.com/pesapalv3"
        else:
            self.base_url = "https://pay.pesapal.com/v3"
        
        # Token storage
        self.token = None
        self.token_expiry = None
    
    def authenticate(self):
        """
        Get access token from Pesapal
        
        Returns:
            str: Access token if successful, None otherwise
        """
        url = f"{self.base_url}/api/Auth/RequestToken"
        
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            print("🔐 Authenticating with Pesapal...")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raises error for 4xx/5xx status codes
            
            data = response.json()
            
            if data.get('status') == '200':
                self.token = data.get('token')
                # Parse expiry date
                expiry_str = data.get('expiryDate')
                self.token_expiry = datetime.fromisoformat(
                    expiry_str.replace('Z', '+00:00')
                )
                
                print(f"✅ Authentication successful!")
                print(f"   Token: {self.token[:20]}...")
                print(f"   Expires: {self.token_expiry}")
                
                return self.token
            else:
                print(f"❌ Authentication failed: {data.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    def get_token(self):
        """
        Get valid token (refreshes if expired)
        
        Returns:
            str: Valid access token
        """
        # Check if token exists and is still valid
        if self.token and self.token_expiry:
            # Add 30 second buffer
            if datetime.now() < (self.token_expiry.replace(tzinfo=None) - timedelta(seconds=30)):
                return self.token
        
        # Token expired or doesn't exist - get new one
        return self.authenticate()
    
    def get_headers(self):
        """
        Get headers with valid bearer token
        
        Returns:
            dict: Headers with authorization
        """
        token = self.get_token()
        
        if not token:
            raise Exception("Failed to get authentication token")
        
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }


# Test the authentication
if __name__ == "__main__":
    print("=" * 60)
    print("PESAPAL AUTHENTICATION TEST")
    print("=" * 60)
    
    auth = PesapalAuth()
    token = auth.authenticate()
    
    if token:
        print("\n✅ Test passed! You can proceed to Step 2.")
    else:
        print("\n❌ Test failed! Check your credentials in .env file")
```

**Run Test**:
```bash
python pesapal_auth.py
```

**Expected Output**:
```
============================================================
PESAPAL AUTHENTICATION TEST
============================================================
🔐 Authenticating with Pesapal...
✅ Authentication successful!
   Token: eyJhbGciOiJIUzI1NiI...
   Expires: 2026-01-01 20:30:45.517770+00:00

✅ Test passed! You can proceed to Step 2.
```

---

#### **Step 2: IPN Registration** 📡

Create `pesapal_ipn.py`:

```python
"""
Step 2: IPN Registration
=======================
Purpose: Register your IPN URL so Pesapal knows where to send notifications
This is done ONCE per URL (store the IPN ID in your database)
"""

import requests
from pesapal_auth import PesapalAuth
from decouple import config


class PesapalIPN:
    """Handles IPN registration and management"""
    
    def __init__(self):
        self.auth = PesapalAuth()
        self.base_url = self.auth.base_url
    
    def register_ipn(self, ipn_url=None, notification_type="POST"):
        """
        Register IPN URL with Pesapal
        
        Args:
            ipn_url (str): Your IPN endpoint URL
            notification_type (str): GET or POST
            
        Returns:
            dict: IPN registration details or None
        """
        # Use environment variable if URL not provided
        if not ipn_url:
            ipn_url = config('IPN_URL')
        
        url = f"{self.base_url}/api/URLSetup/RegisterIPN"
        
        payload = {
            "url": ipn_url,
            "ipn_notification_type": notification_type
        }
        
        try:
            print("📡 Registering IPN URL...")
            print(f"   URL: {ipn_url}")
            print(f"   Type: {notification_type}")
            
            response = requests.post(
                url,
                json=payload,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '200':
                ipn_id = data.get('ipn_id')
                
                print("✅ IPN registered successfully!")
                print(f"   IPN ID: {ipn_id}")
                print(f"\n⚠️  IMPORTANT: Save this IPN ID in your .env file:")
                print(f"   PESAPAL_IPN_ID={ipn_id}")
                
                return data
            else:
                print(f"❌ IPN registration failed: {data.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    def get_ipn_list(self):
        """
        Get all registered IPNs for your merchant account
        
        Returns:
            list: List of registered IPNs
        """
        url = f"{self.base_url}/api/URLSetup/GetIpnList"
        
        try:
            print("📋 Fetching registered IPNs...")
            
            response = requests.get(url, headers=self.auth.get_headers())
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, list):
                print(f"✅ Found {len(data)} registered IPN(s):")
                
                for idx, ipn in enumerate(data, 1):
                    print(f"\n   IPN #{idx}:")
                    print(f"   ID: {ipn.get('ipn_id')}")
                    print(f"   URL: {ipn.get('url')}")
                    print(f"   Type: {ipn.get('ipn_notification_type_description')}")
                    print(f"   Status: {ipn.get('ipn_status_description')}")
                
                return data
            else:
                print("❌ Failed to fetch IPNs")
                return []
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []


# Test IPN registration
if __name__ == "__main__":
    print("=" * 60)
    print("PESAPAL IPN REGISTRATION TEST")
    print("=" * 60)
    
    ipn = PesapalIPN()
    
    # First, list existing IPNs
    print("\n1. Checking existing IPNs...")
    existing_ipns = ipn.get_ipn_list()
    
    # Ask user if they want to register a new one
    if existing_ipns:
        response = input("\n   Do you want to register a new IPN? (y/n): ")
        if response.lower() != 'y':
            print("\n✅ Test complete!")
            exit(0)
    
    # Register new IPN
    print("\n2. Registering new IPN...")
    ipn_url = input("   Enter your IPN URL (or press Enter for .env value): ").strip()
    
    if not ipn_url:
        ipn_url = None  # Will use .env value
    
    result = ipn.register_ipn(ipn_url)
    
    if result:
        print("\n✅ Test passed! You can proceed to Step 3.")
    else:
        print("\n❌ Test failed! Check your IPN URL")
```

**Run Test**:
```bash
python pesapal_ipn.py
```

---

#### **Step 3: Submit Order (Create Payment Request)** 💳

Create `pesapal_payment.py`:

```python
"""
Step 3: Submit Order Request
============================
Purpose: Create a payment request and get redirect URL for customer
"""

import requests
from pesapal_auth import PesapalAuth
from decouple import config


class PesapalPayment:
    """Handles payment order submission"""
    
    def __init__(self):
        self.auth = PesapalAuth()
        self.base_url = self.auth.base_url
    
    def submit_order(self, order_data):
        """
        Submit payment order to Pesapal
        
        Args:
            order_data (dict): Order details
            
        Returns:
            dict: Response with redirect_url or None
        """
        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        
        try:
            print("💳 Submitting order to Pesapal...")
            print(f"   Reference: {order_data.get('id')}")
            print(f"   Amount: {order_data.get('currency')} {order_data.get('amount')}")
            print(f"   Customer: {order_data.get('billing_address', {}).get('email_address')}")
            
            response = requests.post(
                url,
                json=order_data,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '200':
                print("✅ Order submitted successfully!")
                print(f"   Order Tracking ID: {data.get('order_tracking_id')}")
                print(f"   Merchant Reference: {data.get('merchant_reference')}")
                print(f"\n   🔗 Payment URL:")
                print(f"   {data.get('redirect_url')}")
                print(f"\n   👉 Customer should visit this URL to complete payment")
                
                return data
            else:
                print(f"❌ Order submission failed: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def get_transaction_status(self, order_tracking_id):
        """
        Check payment status
        
        Args:
            order_tracking_id (str): Pesapal order tracking ID
            
        Returns:
            dict: Transaction status details
        """
        url = f"{self.base_url}/api/Transactions/GetTransactionStatus"
        
        params = {"orderTrackingId": order_tracking_id}
        
        try:
            print(f"🔍 Checking transaction status...")
            print(f"   Order Tracking ID: {order_tracking_id}")
            
            response = requests.get(
                url,
                params=params,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == '200':
                status = data.get('payment_status_description')
                status_code = data.get('status_code')
                
                # Status code meanings
                status_meanings = {
                    0: "INVALID ⚠️",
                    1: "COMPLETED ✅",
                    2: "FAILED ❌",
                    3: "REVERSED 🔄"
                }
                
                print(f"✅ Status retrieved!")
                print(f"   Status: {status} ({status_meanings.get(status_code, 'UNKNOWN')})")
                print(f"   Amount: {data.get('amount')}")
                print(f"   Payment Method: {data.get('payment_method')}")
                print(f"   Confirmation Code: {data.get('confirmation_code')}")
                print(f"   Description: {data.get('description')}")
                
                return data
            else:
                print(f"❌ Failed to get status: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def create_safari_booking_order(self, 
                                     merchant_reference,
                                     amount,
                                     customer_email,
                                     customer_phone,
                                     customer_name,
                                     tour_description="Kilimanjaro 7-Day Trek"):
        """
        Helper method to create a safari tour booking order
        
        Args:
            merchant_reference (str): Your unique order ID
            amount (float): Tour price
            customer_email (str): Customer email
            customer_phone (str): Customer phone
            customer_name (str): Customer full name
            tour_description (str): Tour package description
            
        Returns:
            dict: Order payload ready for submission
        """
        # Get IPN ID from environment
        ipn_id = config('PESAPAL_IPN_ID', default='')
        callback_url = config('CALLBACK_URL')
        
        # Split customer name
        name_parts = customer_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        order_payload = {
            "id": merchant_reference,
            "currency": "KES",  # Change based on your country
            "amount": float(amount),
            "description": tour_description,
            "callback_url": callback_url,
            "notification_id": ipn_id,
            "billing_address": {
                "email_address": customer_email,
                "phone_number": customer_phone,
                "country_code": "TZ",  # TZ=Tanzania, KE=Kenya, UG=Uganda
                "first_name": first_name,
                "last_name": last_name,
                "line_1": "Safari Booking",
                "city": "Dar es Salaam",
            }
        }
        
        return order_payload


# Test payment submission
if __name__ == "__main__":
    from datetime import datetime
    
    print("=" * 60)
    print("PESAPAL PAYMENT SUBMISSION TEST")
    print("=" * 60)
    
    payment = PesapalPayment()
    
    # Create test order
    merchant_ref = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print("\n📝 Creating test safari booking order...")
    order = payment.create_safari_booking_order(
        merchant_reference=merchant_ref,
        amount=1500.00,
        customer_email="john.doe@example.com",
        customer_phone="+255712345678",
        customer_name="John Doe",
        tour_description="Mount Kilimanjaro 7-Day Machame Route"
    )
    
    # Submit order
    print("\n💳 Submitting order...")
    result = payment.submit_order(order)
    
    if result:
        order_tracking_id = result.get('order_tracking_id')
        redirect_url = result.get('redirect_url')
        
        print(f"\n✅ Test passed!")
        print(f"\n📋 Next steps:")
        print(f"   1. Copy this URL and open in browser:")
        print(f"      {redirect_url}")
        print(f"   2. Complete test payment on Pesapal page")
        print(f"   3. Use this tracking ID to check status:")
        print(f"      {order_tracking_id}")
        
        # Ask if they want to check status now
        input("\n   Press Enter after completing payment to check status...")
        
        print("\n🔍 Checking payment status...")
        status = payment.get_transaction_status(order_tracking_id)
        
    else:
        print("\n❌ Test failed!")
```

**Run Test**:
```bash
python pesapal_payment.py
```

---

### Phase 3: Building the Web Interface (Django)

#### **Step 4: Django Views & URLs**

Create `views.py`:

```python
"""
Django Views for Pesapal Integration
====================================
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime

from .pesapal_payment import PesapalPayment
from .models import Payment


def initiate_payment(request):
    """
    Step 1: Customer initiates payment
    Display booking form
    """
    if request.method == 'POST':
        # Get form data
        tour_name = request.POST.get('tour_name')
        amount = float(request.POST.get('amount'))
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        
        # Create merchant reference
        merchant_ref = f"TOUR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create order
        payment_service = PesapalPayment()
        order = payment_service.create_safari_booking_order(
            merchant_reference=merchant_ref,
            amount=amount,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_name=customer_name,
            tour_description=tour_name
        )
        
        # Submit to Pesapal
        result = payment_service.submit_order(order)
        
        if result:
            # Save to database
            payment = Payment.objects.create(
                merchant_reference=merchant_ref,
                order_tracking_id=result['order_tracking_id'],
                amount=amount,
                currency='KES',
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                description=tour_name,
                status='PENDING'
            )
            
            # Redirect customer to Pesapal
            return redirect(result['redirect_url'])
        else:
            return render(request, 'payment_error.html', {
                'error': 'Failed to initiate payment'
            })
    
    # GET request - show form
    return render(request, 'booking_form.html')


@require_http_methods(["GET"])
def payment_callback(request):
    """
    Step 2: Customer returns from Pesapal
    Handle callback after payment
    """
    # Get parameters from Pesapal callback
    order_tracking_id = request.GET.get('OrderTrackingId')
    merchant_reference = request.GET.get('OrderMerchantReference')
    
    # Verify payment status
    payment_service = PesapalPayment()
    status_data = payment_service.get_transaction_status(order_tracking_id)
    
    if status_data:
        # Update database
        payment = Payment.objects.get(merchant_reference=merchant_reference)
        payment.status = status_data.get('payment_status_description')
        payment.payment_method = status_data.get('payment_method')
        payment.confirmation_code = status_data.get('confirmation_code')
        payment.save()
        
        # Show success/failure page to customer
        return render(request, 'payment_result.html', {
            'payment': payment,
            'status_data': status_data
        })
    else:
        return render(request, 'payment_error.html', {
            'error': 'Could not verify payment status'
        })


@csrf_exempt
@require_http_methods(["POST", "GET"])
def payment_ipn(request):
    """
    Step 3: Pesapal sends IPN notification
    Handle IPN (background notification from Pesapal)
    """
    try:
        # Get parameters (works for both GET and POST)
        if request.method == 'POST':
            data = json.loads(request.body)
            order_tracking_id = data.get('OrderTrackingId')
            merchant_reference = data.get('OrderMerchantReference')
            notification_type = data.get('OrderNotificationType')
        else:  # GET
            order_tracking_id = request.GET.get('OrderTrackingId')
            merchant_reference = request.GET.get('OrderMerchantReference')
            notification_type = request.GET.get('OrderNotificationType')
        
        # Verify payment status with Pesapal
        payment_service = PesapalPayment()
        status_data = payment_service.get_transaction_status(order_tracking_id)
        
        if status_data:
            # Update database
            payment = Payment.objects.get(
                order_tracking_id=order_tracking_id
            )
            
            old_status = payment.status
            new_status = status_data.get('payment_status_description')
            
            payment.status = new_status
            payment.payment_method = status_data.get('payment_method')
            payment.confirmation_code = status_data.get('confirmation_code')
            payment.save()
            
            # Log status change
            print(f"IPN: Payment {merchant_reference} status changed: {old_status} → {new_status}")
            
            # Send email notification if needed
            if new_status == 'Completed':
                # TODO: Send booking confirmation email
                pass
            
            # Respond to Pesapal
            return JsonResponse({
                'orderNotificationType': notification_type,
                'orderTrackingId': order_tracking_id,
                'orderMerchantReference': merchant_reference,
                'status': 200
            })
        else:
            # Failed to verify status
            return JsonResponse({
                'orderNotificationType': notification_type,
                'orderTrackingId': order_tracking_id,
                'orderMerchantReference': merchant_reference,
                'status': 500
            }, status=500)
            
    except Exception as e:
        print(f"IPN Error: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'status': 500
        }, status=500)
```

Create `urls.py`:

```python
"""
URL Configuration for Pesapal Integration
=========================================
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Customer-facing URLs
    path('book/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    
    # Pesapal IPN URL (called by Pesapal servers)
    path('ipn/', views.payment_ipn, name='payment_ipn'),
]
```

Create `models.py`:

```python
"""
Database Models for Payment Tracking
====================================
"""

from django.db import models


class Payment(models.Model):
    """
    Stores payment transaction details
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed'),
        ('INVALID', 'Invalid'),
    ]
    
    # IDs
    merchant_reference = models.CharField(max_length=50, unique=True, db_index=True)
    order_tracking_id = models.CharField(max_length=100, blank=True, db_index=True)
    
    # Amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    
    # Customer details
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Transaction details
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=50, blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['merchant_reference']),
            models.Index(fields=['order_tracking_id']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.merchant_reference} - {self.status}"
    
    @property
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'COMPLETED'
    
    @property
    def can_be_refunded(self):
        """Check if payment can be refunded"""
        return self.status == 'COMPLETED' and self.confirmation_code
```

---

## 🎓 Advanced Topics

### 1. **Handling Token Expiry Gracefully**

```python
from functools import wraps

def require_valid_token(func):
    """
    Decorator to ensure valid token before API calls
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Refresh token if needed
        self.auth.get_token()
        return func(self, *args, **kwargs)
    return wrapper


class PesapalPayment:
    @require_valid_token
    def submit_order(self, order_data):
        # Token is guaranteed to be valid here
        pass
```

### 2. **Idempotency (Preventing Duplicate Payments)**

```python
def initiate_payment(request):
    merchant_ref = f"TOUR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Check if payment already exists
    existing_payment = Payment.objects.filter(
        merchant_reference=merchant_ref
    ).first()
    
    if existing_payment:
        if existing_payment.status == 'PENDING':
            # Reuse existing payment
            return redirect(existing_payment.pesapal_redirect_url)
        elif existing_payment.status == 'COMPLETED':
            # Already paid
            return render(request, 'already_paid.html')
    
    # Create new payment...
```

### 3. **Webhook Security**

```python
import hmac
import hashlib

def verify_pesapal_ipn(request):
    """
    Verify IPN request is genuinely from Pesapal
    """
    # Option 1: IP Whitelist (Pesapal uses pesapal.com domain)
    # Option 2: HMAC signature verification (if Pesapal provides)
    
    # For now, verify by checking with Pesapal API
    order_tracking_id = get_tracking_id_from_request(request)
    status = payment_service.get_transaction_status(order_tracking_id)
    
    return status is not None
```

### 4. **Retry Logic for Failed API Calls**

```python
import time

def retry_api_call(func, max_retries=3, delay=2):
    """
    Retry API call with exponential backoff
    """
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = delay * (2 ** attempt)
            print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s...")
            time.sleep(wait_time)
```

---

## 🎤 Common Interview Questions

### Q1: "Explain the difference between callback URL and IPN URL"

**Answer**:
> "The callback URL is where the customer returns after payment - it's client-side and can fail if the customer's internet drops. The IPN URL is a server-to-server notification from Pesapal directly to our backend - it's reliable even if the customer disconnects. We use the callback for user experience (showing success page) and IPN for critical business logic (updating database, sending confirmations)."

### Q2: "How would you handle a scenario where a customer pays but your server crashes before updating the database?"

**Answer**:
> "This is exactly why Pesapal sends IPN notifications. Even if our server crashes after payment, Pesapal will retry the IPN call. We should:
> 1. Make our IPN endpoint idempotent (safe to call multiple times)
> 2. Use database transactions to ensure atomic updates
> 3. Always verify payment status with Pesapal API before updating
> 4. Log all IPN calls for audit trail"

### Q3: "Why does Pesapal use short-lived tokens (5 minutes)?"

**Answer**:
> "Security! If a token is compromised, the attacker only has 5 minutes to use it. This follows the principle of least privilege - give minimal access for minimal time. In practice, we cache the token and refresh it automatically before expiry."

### Q4: "How would you test the payment integration without spending real money?"

**Answer**:
> "Pesapal provides sandbox credentials that simulate real transactions. We use:
> 1. Sandbox environment (cybqa.pesapal.com)
> 2. Test credentials for each country
> 3. Mock payment methods that auto-complete without real money
> 4. ngrok for local IPN testing
> 5. Unit tests with mocked Pesapal responses"

---

## 🌍 Real-World Scenarios

### Scenario 1: Customer Pays Twice

```python
def handle_duplicate_payment():
    """
    Customer accidentally clicks 'Pay' button twice
    """
    # Solution: Check merchant reference uniqueness
    existing = Payment.objects.filter(
        merchant_reference=merchant_ref,
        status__in=['PENDING', 'COMPLETED']
    ).first()
    
    if existing:
        if existing.status == 'COMPLETED':
            return "Already paid! Here's your confirmation..."
        else:
            return "Payment in progress. Please wait..."
```

### Scenario 2: Refund Request

```python
def process_refund(payment_id):
    """
    Customer requests refund (e.g., tour cancelled)
    """
    payment = Payment.objects.get(id=payment_id)
    
    if not payment.can_be_refunded:
        return "Cannot refund this payment"
    
    # Call Pesapal refund API
    refund_data = {
        "confirmation_code": payment.confirmation_code,
        "amount": payment.amount,
        "username": "admin",
        "remarks": "Tour cancellation - customer request"
    }
    
    result = payment_service.request_refund(refund_data)
    
    if result:
        payment.status = 'REVERSED'
        payment.save()
        # Send refund confirmation email
```

### Scenario 3: Handling Multiple Currencies

```python
COUNTRY_CURRENCY_MAP = {
    'KE': 'KES',  # Kenya - Shilling
    'TZ': 'TZS',  # Tanzania - Shilling
    'UG': 'UGX',  # Uganda - Shilling
    'RW': 'RWF',  # Rwanda - Franc
}

def create_order_with_auto_currency(country_code, amount):
    """
    Automatically select currency based on customer country
    """
    currency = COUNTRY_CURRENCY_MAP.get(country_code, 'USD')
    
    order = {
        "amount": amount,
        "currency": currency,
        "billing_address": {
            "country_code": country_code,
            # ...
        }
    }
    return order
```

---

## 📝 Practice Exercises

### Exercise 1: Basic Integration
**Task**: Build a simple Flask/Django app that:
1. Shows a "Pay $10" button
2. Redirects to Pesapal
3. Shows payment status after payment

### Exercise 2: Webhook Handler
**Task**: Create an IPN endpoint that:
1. Receives POST requests
2. Verifies payment status
3. Updates database
4. Sends email confirmation

### Exercise 3: Admin Dashboard
**Task**: Build an admin panel showing:
1. All payments (with filters)
2. Payment success rate
3. Revenue by payment method
4. Ability to trigger refunds

---

## 🚀 Next Steps

1. **Master the Basics**: Complete all 3 exercises above
2. **Read Pesapal Docs**: https://developer.pesapal.com
3. **Study the Sample Code**: Analyze the scripts you have
4. **Build a Real Project**: Safari booking, online store, etc.
5. **Learn Security**: HTTPS, input validation, SQL injection prevention
6. **Deploy to Production**: Heroku, DigitalOcean, AWS

---

## 📚 Additional Resources

- Pesapal Postman Collection: https://documenter.getpostman.com/view/6715320/UyxepTv1
- Test Credentials: See documentation
- Community Forum: https://developer.pesapal.com/forum
- Django Documentation: https://docs.djangoproject.com
- Requests Library: https://requests.readthedocs.io

---

## 💡 Pro Tips for Talking with Senior Developers

1. **Use Correct Terminology**:
   - ❌ "The payment didn't work"
   - ✅ "The transaction status returned code 2 (FAILED)"

2. **Show You Understand the Flow**:
   - "We authenticate → get token → submit order → handle IPN"

3. **Discuss Edge Cases**:
   - "What if the IPN arrives before the callback?"
   - "How do we handle partial refunds?"

4. **Ask Smart Questions**:
   - ❌ "Why doesn't it work?"
   - ✅ "The IPN isn't being received. Should I check firewall rules or test with ngrok?"

5. **Know Your Metrics**:
   - "Our payment success rate is 94%"
   - "Average transaction processing time is 3.2 seconds"

---

**Good luck with your learning journey! 🎓**

*Remember: Every senior developer was once a beginner. The difference is they asked questions, built projects, and learned from mistakes. You're on the right path!*
