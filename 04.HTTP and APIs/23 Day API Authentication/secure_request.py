from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get("https://httpbin.org/bearer", headers=headers)
print("Status code:", response.status_code)
print("Body:", response.json())
