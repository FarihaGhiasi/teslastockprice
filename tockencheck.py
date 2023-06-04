import os

api_key = os.environ.get("API_KEY")
if api_key:
    print("API_KEY is set:", api_key)
else:
    print("API_KEY is not set")
