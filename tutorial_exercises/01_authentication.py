#!/usr/bin/env python3
"""
EXERCISE 1: Pesapal Authentication
===================================

LEARNING OBJECTIVES:
- Understand how OAuth-like authentication works
- Handle HTTP POST requests
- Parse JSON responses
- Manage token expiry

YOUR TASK:
Complete the missing parts of this authentication class.
Look for TODO comments.

DIFFICULTY: Beginner ⭐
TIME: 15-20 minutes
"""

import requests
import os
from datetime import datetime, timedelta


class PesapalAuth:
    """Handles Pesapal authentication"""
    
    def __init__(self, consumer_key, consumer_secret, environment='sandbox'):
        """
        Initialize authentication handler
        
        Args:
            consumer_key (str): Your Pesapal consumer key
            consumer_secret (str): Your Pesapal consumer secret
            environment (str): 'sandbox' or 'live'
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
        # TODO 1: Set the correct base_url based on environment
        # Sandbox: https://cybqa.pesapal.com/pesapalv3
        # Live: https://pay.pesapal.com/v3
        if environment == 'sandbox':
            self.base_url = "___FILL_THIS___"  # TODO: Fill this
        else:
            self.base_url = "___FILL_THIS___"  # TODO: Fill this
        
        self.token = None
        self.token_expiry = None
    
    def authenticate(self):
        """
        Get access token from Pesapal
        
        Returns:
            str: Access token or None if failed
        """
        # TODO 2: Complete the URL
        url = f"{self.base_url}/api/Auth/RequestToken"
        
        # TODO 3: Create the payload dictionary
        # Hint: It needs consumer_key and consumer_secret
        payload = {
            "consumer_key": "___FILL_THIS___",  # TODO: Fill this
            "consumer_secret": "___FILL_THIS___"  # TODO: Fill this
        }
        
        # TODO 4: Set correct headers
        headers = {
            "Accept": "___FILL_THIS___",  # TODO: What format do we accept?
            "Content-Type": "___FILL_THIS___"  # TODO: What format are we sending?
        }
        
        try:
            # TODO 5: Make a POST request
            # Hint: Use requests.post() with url, json=payload, headers=headers
            response = requests.post(url, json=payload, headers=headers)
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # TODO 6: Extract token from response
            # Hint: Check if status is '200', then get 'token' from data
            if data.get('status') == '200':
                self.token = data.get('___FILL_THIS___')  # TODO: Fill this
                
                # Parse expiry date
                expiry_str = data.get('expiryDate')
                self.token_expiry = datetime.fromisoformat(
                    expiry_str.replace('Z', '+00:00')
                )
                
                print(f"✅ Authentication successful!")
                print(f"   Token: {self.token[:30]}...")
                print(f"   Expires: {self.token_expiry}")
                
                return self.token
            else:
                print(f"❌ Authentication failed: {data.get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {str(e)}")
            return None
    
    def is_token_valid(self):
        """
        Check if current token is still valid
        
        Returns:
            bool: True if valid, False otherwise
        """
        # TODO 7: Implement token validation logic
        # Hint: Check if token exists and hasn't expired
        # Add 30 second buffer to be safe
        
        if self.token is None or self.token_expiry is None:
            return False
        
        now = datetime.now()
        expiry = self.token_expiry.replace(tzinfo=None)
        buffer = timedelta(seconds=30)
        
        # TODO: Return True if token is still valid
        return ___FILL_THIS___  # TODO: Fill this (compare now with expiry - buffer)
    
    def get_token(self):
        """
        Get a valid token (refresh if needed)
        
        Returns:
            str: Valid access token
        """
        # TODO 8: Complete this method
        # If token is valid, return it
        # Otherwise, authenticate and return new token
        
        if self.is_token_valid():
            return self.token
        else:
            return self.authenticate()


# ============================================
# TEST YOUR CODE
# ============================================

def test_authentication():
    """Test authentication with sandbox credentials"""
    
    print("=" * 60)
    print("TESTING AUTHENTICATION")
    print("=" * 60)
    
    # Use Tanzania sandbox credentials
    auth = PesapalAuth(
        consumer_key="ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8",
        consumer_secret="q27RChYs5UkypdcNYKzuUw460Dg=",
        environment='sandbox'
    )
    
    # Test 1: First authentication
    print("\n📝 Test 1: First authentication")
    token1 = auth.authenticate()
    
    if token1:
        print("✅ Test 1 passed!")
    else:
        print("❌ Test 1 failed!")
        return
    
    # Test 2: Token should still be valid
    print("\n📝 Test 2: Check if token is still valid")
    if auth.is_token_valid():
        print("✅ Test 2 passed! Token is valid")
    else:
        print("❌ Test 2 failed! Token should be valid")
    
    # Test 3: Get token (should return cached token)
    print("\n📝 Test 3: Get cached token")
    token2 = auth.get_token()
    
    if token2 == token1:
        print("✅ Test 3 passed! Got cached token")
    else:
        print("❌ Test 3 failed! Should return same token")
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    test_authentication()


# ============================================
# CHALLENGE QUESTIONS (For Discussion)
# ============================================
"""
1. Why does Pesapal use short-lived tokens (5 minutes)?
   YOUR ANSWER: 
   
2. What happens if we don't check token expiry before making API calls?
   YOUR ANSWER: 
   
3. How would you modify this code to store tokens in Redis cache?
   YOUR ANSWER: 
   
4. What's the difference between requests.get() and requests.post()?
   YOUR ANSWER: 
   
5. Why do we use response.raise_for_status()?
   YOUR ANSWER: 
"""
