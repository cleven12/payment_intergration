#!/usr/bin/env python3
"""
EXERCISE 2: IPN (Instant Payment Notification) Handler
======================================================

LEARNING OBJECTIVES:
- Understand webhook/callback concepts
- Handle both GET and POST requests
- Parse query parameters and JSON bodies
- Verify payment status
- Update database safely

YOUR TASK:
Build a complete IPN handler that processes payment notifications from Pesapal.

DIFFICULTY: Intermediate ⭐⭐
TIME: 30-40 minutes
"""

import json
from datetime import datetime


class MockRequest:
    """
    Simulates Django/Flask request object for testing
    """
    def __init__(self, method='POST', get_params=None, post_data=None):
        self.method = method
        self.GET = get_params or {}
        self.POST = post_data or {}
        self.body = json.dumps(post_data or {})


class MockDatabase:
    """
    Simulates database for testing
    """
    def __init__(self):
        self.payments = {}
    
    def get_payment(self, order_tracking_id):
        """Get payment by order tracking ID"""
        return self.payments.get(order_tracking_id)
    
    def update_payment(self, order_tracking_id, status, payment_method, confirmation_code):
        """Update payment status"""
        if order_tracking_id in self.payments:
            self.payments[order_tracking_id].update({
                'status': status,
                'payment_method': payment_method,
                'confirmation_code': confirmation_code,
                'updated_at': datetime.now()
            })
            return True
        return False
    
    def create_payment(self, order_tracking_id, merchant_ref, amount):
        """Create new payment record"""
        self.payments[order_tracking_id] = {
            'order_tracking_id': order_tracking_id,
            'merchant_reference': merchant_ref,
            'amount': amount,
            'status': 'PENDING',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }


class MockPesapalAPI:
    """
    Simulates Pesapal API for testing
    """
    def __init__(self):
        self.transactions = {
            'TRACK-001': {
                'status': '200',
                'payment_status_description': 'Completed',
                'payment_method': 'M-Pesa',
                'confirmation_code': 'ABC123XYZ',
                'amount': 1500.00
            },
            'TRACK-002': {
                'status': '200',
                'payment_status_description': 'Failed',
                'payment_method': 'Visa',
                'confirmation_code': '',
                'amount': 2500.00
            }
        }
    
    def get_transaction_status(self, order_tracking_id):
        """Mock getting transaction status"""
        return self.transactions.get(order_tracking_id)


# ============================================
# YOUR CODE STARTS HERE
# ============================================

class IPNHandler:
    """
    Handles IPN notifications from Pesapal
    """
    
    def __init__(self, database, pesapal_api):
        """
        Initialize IPN handler
        
        Args:
            database: Database connection/ORM
            pesapal_api: Pesapal API client
        """
        self.db = database
        self.api = pesapal_api
    
    def extract_ipn_parameters(self, request):
        """
        Extract IPN parameters from request (GET or POST)
        
        Args:
            request: HTTP request object
            
        Returns:
            dict: Dictionary with OrderTrackingId, OrderMerchantReference, OrderNotificationType
        """
        # TODO 1: Handle both GET and POST requests
        # For POST: Parse JSON body
        # For GET: Get query parameters
        
        if request.method == 'POST':
            # TODO: Parse JSON from request.body
            data = ___FILL_THIS___  # Hint: json.loads(request.body)
            
        else:  # GET
            # TODO: Get parameters from request.GET
            data = {
                'OrderTrackingId': request.GET.get('___FILL_THIS___'),  # TODO
                'OrderMerchantReference': request.GET.get('___FILL_THIS___'),  # TODO
                'OrderNotificationType': request.GET.get('___FILL_THIS___')  # TODO
            }
        
        return data
    
    def verify_payment_with_pesapal(self, order_tracking_id):
        """
        Verify payment status with Pesapal API
        (Don't trust IPN parameters - always verify!)
        
        Args:
            order_tracking_id (str): Pesapal order tracking ID
            
        Returns:
            dict: Payment status details or None
        """
        # TODO 2: Call Pesapal API to get transaction status
        # Hint: Use self.api.get_transaction_status()
        
        try:
            status_data = ___FILL_THIS___  # TODO: Call API
            
            if status_data and status_data.get('status') == '200':
                return status_data
            else:
                print(f"❌ Failed to verify payment: {order_tracking_id}")
                return None
                
        except Exception as e:
            print(f"❌ Error verifying payment: {str(e)}")
            return None
    
    def update_payment_status(self, order_tracking_id, payment_data):
        """
        Update payment status in database
        
        Args:
            order_tracking_id (str): Order tracking ID
            payment_data (dict): Payment details from Pesapal
            
        Returns:
            bool: True if update successful
        """
        # TODO 3: Extract payment details
        status = payment_data.get('___FILL_THIS___')  # TODO: Get status description
        payment_method = payment_data.get('___FILL_THIS___')  # TODO: Get payment method
        confirmation_code = payment_data.get('___FILL_THIS___')  # TODO: Get confirmation code
        
        # TODO 4: Update database
        success = self.db.update_payment(
            order_tracking_id,
            status,
            payment_method,
            confirmation_code
        )
        
        if success:
            print(f"✅ Updated payment {order_tracking_id} to {status}")
        else:
            print(f"❌ Failed to update payment {order_tracking_id}")
        
        return success
    
    def send_confirmation_email(self, payment):
        """
        Send email confirmation to customer
        (Simplified for this exercise)
        
        Args:
            payment (dict): Payment details
        """
        # TODO 5: Implement email sending logic
        # For now, just print what would be sent
        
        if payment['status'] == 'Completed':
            print(f"📧 Sending confirmation email for {payment['merchant_reference']}")
            print(f"   Amount: {payment['amount']}")
            print(f"   Status: {payment['status']}")
        elif payment['status'] == 'Failed':
            print(f"📧 Sending failure notification for {payment['merchant_reference']}")
    
    def create_ipn_response(self, order_tracking_id, merchant_ref, notification_type, success):
        """
        Create JSON response to send back to Pesapal
        
        Args:
            order_tracking_id (str): Order tracking ID
            merchant_ref (str): Merchant reference
            notification_type (str): Notification type
            success (bool): Whether processing was successful
            
        Returns:
            dict: JSON response
        """
        # TODO 6: Create response dictionary
        # Status should be 200 if success, 500 if failed
        
        return {
            'orderNotificationType': notification_type,
            'orderTrackingId': order_tracking_id,
            'orderMerchantReference': merchant_ref,
            'status': ___FILL_THIS___  # TODO: 200 if success else 500
        }
    
    def handle_ipn(self, request):
        """
        Main IPN handler - coordinates all steps
        
        Args:
            request: HTTP request object
            
        Returns:
            tuple: (response_dict, http_status_code)
        """
        try:
            # Step 1: Extract parameters
            print("📥 IPN received!")
            ipn_data = self.extract_ipn_parameters(request)
            
            order_tracking_id = ipn_data.get('OrderTrackingId')
            merchant_ref = ipn_data.get('OrderMerchantReference')
            notification_type = ipn_data.get('OrderNotificationType')
            
            print(f"   Tracking ID: {order_tracking_id}")
            print(f"   Merchant Ref: {merchant_ref}")
            print(f"   Type: {notification_type}")
            
            # Step 2: Verify with Pesapal
            print("🔍 Verifying with Pesapal...")
            payment_data = self.verify_payment_with_pesapal(order_tracking_id)
            
            if not payment_data:
                # Verification failed
                response = self.create_ipn_response(
                    order_tracking_id, merchant_ref, notification_type, False
                )
                return response, 500
            
            # Step 3: Update database
            print("💾 Updating database...")
            update_success = self.update_payment_status(order_tracking_id, payment_data)
            
            if not update_success:
                response = self.create_ipn_response(
                    order_tracking_id, merchant_ref, notification_type, False
                )
                return response, 500
            
            # Step 4: Send confirmation
            payment = self.db.get_payment(order_tracking_id)
            self.send_confirmation_email(payment)
            
            # Step 5: Success response
            response = self.create_ipn_response(
                order_tracking_id, merchant_ref, notification_type, True
            )
            
            print("✅ IPN processed successfully!\n")
            return response, 200
            
        except Exception as e:
            print(f"❌ IPN processing error: {str(e)}")
            return {'error': str(e), 'status': 500}, 500


# ============================================
# TEST YOUR CODE
# ============================================

def test_ipn_handler():
    """Test IPN handler with various scenarios"""
    
    print("=" * 60)
    print("TESTING IPN HANDLER")
    print("=" * 60)
    
    # Setup
    db = MockDatabase()
    api = MockPesapalAPI()
    handler = IPNHandler(db, api)
    
    # Create test payment
    db.create_payment('TRACK-001', 'TOUR-12345', 1500.00)
    
    # Test 1: POST IPN for successful payment
    print("\n📝 Test 1: POST IPN - Successful Payment")
    print("-" * 60)
    
    post_request = MockRequest(
        method='POST',
        post_data={
            'OrderTrackingId': 'TRACK-001',
            'OrderMerchantReference': 'TOUR-12345',
            'OrderNotificationType': 'IPNCHANGE'
        }
    )
    
    response, status_code = handler.handle_ipn(post_request)
    
    if status_code == 200 and response['status'] == 200:
        print("✅ Test 1 passed!")
    else:
        print("❌ Test 1 failed!")
        print(f"   Response: {response}")
        print(f"   Status: {status_code}")
    
    # Verify database was updated
    payment = db.get_payment('TRACK-001')
    if payment['status'] == 'Completed':
        print("✅ Database updated correctly!")
    else:
        print(f"❌ Database not updated! Status: {payment['status']}")
    
    # Test 2: GET IPN for failed payment
    print("\n📝 Test 2: GET IPN - Failed Payment")
    print("-" * 60)
    
    db.create_payment('TRACK-002', 'TOUR-67890', 2500.00)
    
    get_request = MockRequest(
        method='GET',
        get_params={
            'OrderTrackingId': 'TRACK-002',
            'OrderMerchantReference': 'TOUR-67890',
            'OrderNotificationType': 'IPNCHANGE'
        }
    )
    
    response, status_code = handler.handle_ipn(get_request)
    
    if status_code == 200:
        print("✅ Test 2 passed!")
    else:
        print("❌ Test 2 failed!")
    
    # Check failed payment status
    payment = db.get_payment('TRACK-002')
    if payment['status'] == 'Failed':
        print("✅ Failed payment status recorded correctly!")
    else:
        print(f"❌ Wrong status! Expected 'Failed', got '{payment['status']}'")
    
    # Test 3: IPN for non-existent payment
    print("\n📝 Test 3: IPN - Non-existent Payment")
    print("-" * 60)
    
    bad_request = MockRequest(
        method='POST',
        post_data={
            'OrderTrackingId': 'TRACK-999',
            'OrderMerchantReference': 'TOUR-99999',
            'OrderNotificationType': 'IPNCHANGE'
        }
    )
    
    response, status_code = handler.handle_ipn(bad_request)
    
    if status_code == 500:
        print("✅ Test 3 passed! Correctly handled non-existent payment")
    else:
        print("❌ Test 3 failed! Should return 500 for non-existent payment")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    test_ipn_handler()


# ============================================
# CHALLENGE QUESTIONS
# ============================================
"""
1. Why do we verify payment status with Pesapal instead of trusting IPN parameters?
   YOUR ANSWER: 
   
2. What's the difference between notification_type "IPNCHANGE" and "CALLBACKURL"?
   YOUR ANSWER: 
   
3. Why should IPN endpoints be idempotent (safe to call multiple times)?
   YOUR ANSWER: 
   
4. How would you prevent duplicate IPN processing?
   YOUR ANSWER: 
   
5. What happens if your IPN endpoint returns 500? Will Pesapal retry?
   YOUR ANSWER: 
"""
