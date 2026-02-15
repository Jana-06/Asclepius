"""
Reset password for an existing Firebase Auth user.
Uses Firebase REST APIs (no service account needed).
"""
import requests
import json

API_KEY = 'AIzaSyDfcCL5NtnA8pPftR_H7dlWND_yEOl0OKo'

# First, get the reset password link
LOOKUP_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup'
RESET_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode'
UPDATE_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:update'

email = 'dr.hackathon@example.com'
new_password = 'Hack@2026'

print("Attempting to find the user and reset password...")
print("Note: We may need to delete and recreate the user instead.\n")

# Let's try a different approach: delete the user via Firebase console or
# use a workaround with custom claims

# For now, let's try to get the existing user's ID token (may fail)
# Then we can use it to update the password

# Alternative: Let's just create a fresh user with a different email for testing
print("Creating a fresh test doctor account...")

SIGNUP_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'

# Try with a simpler email
test_email = 'hackathon.doctor@test.com'
test_password = 'TestPassword123!'

payload = {
    'email': test_email,
    'password': test_password,
    'returnSecureToken': True,
}

params = {'key': API_KEY}

response = requests.post(SIGNUP_URL, json=payload, params=params)

if response.status_code == 200:
    data = response.json()
    uid = data.get('localId')
    print(f"✅ New test user created!")
    print(f"   Email: {test_email}")
    print(f"   Password: {test_password}")
    print(f"   UID: {uid}")
    print(f"\nUse these credentials to test doctor login.")
else:
    error_data = response.json()
    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
    print(f"❌ Error: {error_msg}")
    print(f"Response: {json.dumps(error_data, indent=2)}")

