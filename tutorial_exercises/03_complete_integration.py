#!/usr/bin/env python3
"""
EXERCISE 3: Complete Payment Flow (Capstone Project)
===================================================

LEARNING OBJECTIVES:
- Integrate all components (auth, IPN, order submission)
- Handle complete payment lifecycle
- Implement error handling and logging
- Build production-ready code

YOUR TASK:
Build a complete tour booking payment system using everything you've learned.

DIFFICULTY: Advanced ⭐⭐⭐
TIME: 60-90 minutes
"""

import requests
import json
import sqlite3
from datetime import datetime
from pathlib import Path


# ============================================
# DATABASE SETUP
# ============================================

class PaymentDatabase:
    """
    Manages payment database operations
    """
    
    def __init__(self, db_path='payments.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # TODO 1: Create payments table
        # Columns needed:
        # - id (INTEGER PRIMARY KEY)
        # - merchant_reference (TEXT UNIQUE)
        # - order_tracking_id (TEXT)
        # - amount (REAL)
        # - currency (TEXT)
        # - customer_name (TEXT)
        # - customer_email (TEXT)
        # - customer_phone (TEXT)
        # - description (TEXT)
        # - status (TEXT DEFAULT 'PENDING')
        # - payment_method (TEXT)
        # - confirmation_code (TEXT)
        # - created_at (TIMESTAMP)
        # - updated_at (TIMESTAMP)
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                -- TODO: Fill in the columns
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_payment(self, **kwargs):
        """
        Create new payment record
        
        Args:
            **kwargs: Payment details
            
        Returns:
            int: Payment ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # TODO 2: Insert payment into database
        cursor.execute('''
            INSERT INTO payments 
            (merchant_reference, order_tracking_id, amount, currency, 
             customer_name, customer_email, customer_phone, description, 
             status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (
            # TODO: Fill in the values from kwargs
        ))
        
        payment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return payment_id
    
    def update_payment(self, order_tracking_id, status, payment_method, confirmation_code):
        """Update payment status"""
        # TODO 3: Implement update logic
        pass
    
    def get_payment_by_tracking_id(self, order_tracking_id):
        """Get payment by order tracking ID"""
        # TODO 4: Implement query
        pass
    
    def get_all_payments(self):
        """Get all payments"""
        # TODO 5: Implement query
        pass


# ============================================
# PESAPAL SERVICE
# ============================================

class PesapalService:
    """
    Complete Pesapal integration service
    """
    
    def __init__(self, consumer_key, consumer_secret, environment='sandbox'):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
        if environment == 'sandbox':
            self.base_url = "https://cybqa.pesapal.com/pesapalv3"
        else:
            self.base_url = "https://pay.pesapal.com/v3"
        
        self.token = None
        self.token_expiry = None
        self.db = PaymentDatabase()
    
    def authenticate(self):
        """Get authentication token"""
        # TODO 6: Implement authentication
        # Hint: Look at Exercise 1
        pass
    
    def get_headers(self):
        """Get headers with valid token"""
        # TODO 7: Check token validity and refresh if needed
        pass
    
    def register_ipn(self, ipn_url, notification_type='POST'):
        """Register IPN URL"""
        # TODO 8: Implement IPN registration
        pass
    
    def create_order(self, 
                     merchant_reference,
                     amount,
                     currency,
                     description,
                     customer_name,
                     customer_email,
                     customer_phone,
                     callback_url,
                     ipn_id):
        """
        Create and submit order to Pesapal
        
        Returns:
            dict: Order details with redirect_url
        """
        # TODO 9: Build order payload
        order_payload = {
            "id": merchant_reference,
            "currency": currency,
            "amount": float(amount),
            "description": description,
            "callback_url": callback_url,
            "notification_id": ipn_id,
            "billing_address": {
                # TODO: Fill in billing address
            }
        }
        
        # TODO 10: Submit to Pesapal
        url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        
        try:
            # Make request
            # Save to database
            # Return result
            pass
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            return None
    
    def get_transaction_status(self, order_tracking_id):
        """Get payment status from Pesapal"""
        # TODO 11: Implement status check
        pass
    
    def handle_ipn(self, ipn_data):
        """
        Handle IPN notification
        
        Args:
            ipn_data (dict): IPN parameters
            
        Returns:
            dict: Response to send back to Pesapal
        """
        # TODO 12: Implement IPN handling
        # Hint: Look at Exercise 2
        pass


# ============================================
# COMMAND LINE INTERFACE
# ============================================

class TourBookingCLI:
    """
    Interactive command-line interface for tour booking
    """
    
    def __init__(self, pesapal_service):
        self.service = pesapal_service
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("SAFARI TOUR BOOKING SYSTEM")
        print("=" * 60)
        print("1. Book New Tour")
        print("2. Check Payment Status")
        print("3. View All Bookings")
        print("4. Register IPN URL")
        print("5. Simulate IPN Call (Testing)")
        print("6. Exit")
        print("=" * 60)
    
    def book_tour(self):
        """Handle new tour booking"""
        print("\n📝 NEW TOUR BOOKING")
        print("-" * 60)
        
        # TODO 13: Collect booking details from user
        # - Tour name
        # - Amount
        # - Customer name
        # - Customer email
        # - Customer phone
        
        # Generate merchant reference
        merchant_ref = f"TOUR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # TODO 14: Call self.service.create_order()
        # Get redirect URL
        # Display payment instructions
        
        pass
    
    def check_status(self):
        """Check payment status"""
        print("\n🔍 CHECK PAYMENT STATUS")
        print("-" * 60)
        
        tracking_id = input("Enter Order Tracking ID: ").strip()
        
        # TODO 15: Call self.service.get_transaction_status()
        # Display status details
        
        pass
    
    def view_bookings(self):
        """Display all bookings"""
        print("\n📋 ALL BOOKINGS")
        print("-" * 60)
        
        # TODO 16: Get all payments from database
        # Display in a nice table format
        
        pass
    
    def register_ipn_url(self):
        """Register IPN URL"""
        print("\n📡 REGISTER IPN URL")
        print("-" * 60)
        
        ipn_url = input("Enter IPN URL: ").strip()
        notification_type = input("Type (GET/POST) [POST]: ").strip().upper()
        
        if not notification_type:
            notification_type = 'POST'
        
        # TODO 17: Call self.service.register_ipn()
        
        pass
    
    def simulate_ipn(self):
        """Simulate IPN call for testing"""
        print("\n🧪 SIMULATE IPN CALL")
        print("-" * 60)
        
        tracking_id = input("Enter Order Tracking ID: ").strip()
        merchant_ref = input("Enter Merchant Reference: ").strip()
        
        ipn_data = {
            'OrderTrackingId': tracking_id,
            'OrderMerchantReference': merchant_ref,
            'OrderNotificationType': 'IPNCHANGE'
        }
        
        # TODO 18: Call self.service.handle_ipn()
        # Display response
        
        pass
    
    def run(self):
        """Main loop"""
        # TODO 19: Authenticate on startup
        print("🔐 Authenticating with Pesapal...")
        # Call authentication
        
        while True:
            self.display_menu()
            choice = input("\nSelect option [1-6]: ").strip()
            
            if choice == '1':
                self.book_tour()
            elif choice == '2':
                self.check_status()
            elif choice == '3':
                self.view_bookings()
            elif choice == '4':
                self.register_ipn_url()
            elif choice == '5':
                self.simulate_ipn()
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid option. Please try again.")


# ============================================
# MAIN PROGRAM
# ============================================

def main():
    """Main entry point"""
    
    print("=" * 60)
    print("PESAPAL TOUR BOOKING SYSTEM")
    print("=" * 60)
    
    # TODO 20: Load credentials
    # Option 1: From environment variables
    # Option 2: From .env file
    # Option 3: From user input
    
    consumer_key = input("\nConsumer Key: ").strip()
    consumer_secret = input("Consumer Secret: ").strip()
    
    if not consumer_key or not consumer_secret:
        print("❌ Credentials required!")
        return
    
    # Initialize service
    service = PesapalService(consumer_key, consumer_secret, environment='sandbox')
    
    # Run CLI
    cli = TourBookingCLI(service)
    cli.run()


if __name__ == "__main__":
    main()


# ============================================
# TESTING CHECKLIST
# ============================================
"""
Test your implementation with these scenarios:

[ ] 1. Authentication
    - Successfully get token
    - Token auto-refreshes when expired
    
[ ] 2. IPN Registration
    - Register new IPN URL
    - View registered IPNs
    
[ ] 3. Order Creation
    - Create order with valid data
    - Get redirect URL
    - Order saved to database
    
[ ] 4. Payment Status
    - Check status of existing order
    - Handle non-existent order
    
[ ] 5. IPN Handling
    - Process successful payment IPN
    - Process failed payment IPN
    - Update database correctly
    - Send appropriate response
    
[ ] 6. Error Handling
    - Invalid credentials
    - Network errors
    - Invalid order tracking ID
    - Database errors
    
[ ] 7. Edge Cases
    - Expired token during request
    - Duplicate merchant reference
    - Missing required fields
    - Invalid email/phone format
"""

# ============================================
# BONUS CHALLENGES
# ============================================
"""
1. Add input validation
   - Validate email format
   - Validate phone format
   - Validate amount (positive number)

2. Add logging
   - Log all API calls
   - Log errors with stack traces
   - Create daily log files

3. Add retry logic
   - Retry failed API calls
   - Use exponential backoff
   - Max 3 retries

4. Add email notifications
   - Send confirmation email on success
   - Send failure notification
   - Use templates

5. Add reporting
   - Generate daily payment report
   - Calculate success rate
   - Show revenue by payment method

6. Add refund functionality
   - Request refund via API
   - Update database
   - Send refund confirmation

7. Deploy to production
   - Use environment variables
   - Set up HTTPS
   - Configure proper error handling
   - Set up monitoring
"""

# ============================================
# SENIOR DEVELOPER QUESTIONS
# ============================================
"""
Be prepared to discuss these with senior developers:

1. Security
   Q: How do you prevent SQL injection?
   Q: How do you secure API credentials?
   Q: Why use HTTPS for IPN URLs?

2. Reliability
   Q: What happens if database is down during IPN?
   Q: How do you handle duplicate IPN calls?
   Q: What's your retry strategy?

3. Performance
   Q: How many requests per second can your system handle?
   Q: How would you cache authentication tokens?
   Q: How would you handle 10,000 concurrent bookings?

4. Monitoring
   Q: How do you track payment success rate?
   Q: What alerts do you set up?
   Q: How do you debug failed payments?

5. Architecture
   Q: Why separate database from API logic?
   Q: How would you scale this system?
   Q: What would you change for production?
"""
