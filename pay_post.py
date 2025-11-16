import requests
import json
from datetime import datetime
headers = {
	'User-Agent' : 'PaymentApp/1.0',
	'Accept' : 'application/json',
	'X-Custom-Header' : 'MyValue'
	}
response = requests.get('https://httpbin.org/headers',headers = headers)
print("Response Sent")
