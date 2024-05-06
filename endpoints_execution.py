import requests
import time
import json

# Load user data
with open("./jsons/test_user.json") as test_user_file:
    test_user_data = json.load(test_user_file)

# Set the base URL
url = "http://localhost:8000"

# Register user
user_registration = requests.post(f"{url}/register", json=test_user_data)
time.sleep(0.5)  # Wait for half a second to ensure the registration completes

# Get the token
token_response = requests.post(
    f"{url}/token", 
    data={"username": "test", "password": "test", "grant_type": "password"}, 
    headers={"content-type": "application/x-www-form-urlencoded"}
)
token_json = token_response.json()
token = token_json["access_token"]  # Extract the access token

# Use the token in subsequent requests
headers = {"Authorization": f"Bearer {token}"}
profile_response = requests.get(f"{url}/profile", headers=headers)
delete_user_response = requests.delete(f"{url}/profile/delete_user", json={"username": "test"}, headers=headers)

# Print responses for debugging
print("Registration Response:", user_registration.status_code)
print("Token Response:", token_response.status_code)
print("Token:", token)
print("Profile Response:", profile_response.status_code)
print("Delete User Response:", delete_user_response.status_code)

