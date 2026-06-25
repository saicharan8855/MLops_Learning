import requests
import time

def call_with_retry(url, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"Attempt {attempt}: Success!")
                return response
            else:
                print(f"Attempt {attempt}: Got status {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt}: Timed out")
        except requests.exceptions.ConnectionError:
            print(f"Attempt {attempt}: Connection failed")

        wait_time = 2 ** attempt  # exponential backoff: 2, 4, 8 seconds
        print(f"Waiting {wait_time}s before retrying...")
        time.sleep(wait_time)

    print("All retries failed.")
    return None

# this endpoint randomly returns errors ~50% of the time
call_with_retry("https://httpbin.org/status/200,500")
