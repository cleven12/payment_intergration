"""
Understanding HTTP Methods
    - GET : Retrive data (like chacking booking status)
    - POST: Send data (like creating a payment)
    - PUT : Update data
    - DELETE : Remove Data
"""

import requests

# Test 1: Simple GET requests
print("===  TEST 1: Basic GET ===")
response = requests.get('https://api.restful-api.dev/objects')
print(f"Status Code: {response.status_code}")
print(f"Response Type : {type(response)}")
print(f"Response Textx: (First 100 Chars): {response.text[:100]}")
