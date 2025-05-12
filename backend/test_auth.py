import httpx

BASE_URL = "http://127.0.0.1:8000/api/auth"

test_user = {
    "email": "testuser@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
}

with httpx.Client(follow_redirects=True) as client:
    # 1. Register
    print("Registering user...")
    r = client.post(f"{BASE_URL}/register", json=test_user)
    print("Register:", r.status_code, r.json())

    # 2. Login
    print("\nLogging in...")
    login_data = {"email": test_user["email"], "password": test_user["password"]}
    r = client.post(f"{BASE_URL}/login", json=login_data)
    print("Login:", r.status_code, r.json())
    # Save session cookie
    session_cookie = r.cookies.get("session_token")
    print("Session cookie:", session_cookie)

    # 3. Get current user info
    print("\nGetting current user info...")
    cookies = {"session_token": session_cookie}
    r = client.get(f"{BASE_URL}/me", cookies=cookies)
    print("Me:", r.status_code, r.json())

    # 4. Logout
    print("\nLogging out...")
    r = client.post(f"{BASE_URL}/logout", cookies=cookies)
    print("Logout:", r.status_code, r.json()) 