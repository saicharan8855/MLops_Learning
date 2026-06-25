import requests

print("sending request with a 2 second timeout...")
try:
	response = requests.get("https://httpbin.org/delay/3", timeout = 2)
	print("status code:", response.status_code)
except requests.exceptions.Timeout:
	print("request timed out after 2 seconds - giving up gracefully")

