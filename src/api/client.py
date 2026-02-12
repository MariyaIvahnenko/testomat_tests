import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv

load_dotenv()


class TestomatClient:
    def __init__(self):
        self.base_url = os.getenv('BASE_APP_URL')
        self.email = None
        self.password = None
        self.jwt_token = None
        self._authenticated = False

    def login(self) -> bool:
        if not self.email or not self.password:
            print("Error: Email and password must be set before login")
            return False

        login_url = f"{self.base_url}/api/login"

        try:
            payload = {
                "email": self.email,
                "password": self.password
            }

            response = requests.post(login_url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.jwt_token = data.get("jwt")

            if not self.jwt_token:
                print("Error: No JWT token received in response")
                return False

            self._authenticated = True
            return True

        except requests.exceptions.Timeout:
            print("Error: Authentication request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error: Authentication failed - {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Status: {e.response.status_code}")
                print(f"Response: {e.response.text[:200]}")
            return False

    def get_headers(self) -> Dict[str, str]:
        if not self.jwt_token or not self._authenticated:
            if not self.login():
                raise Exception("Not authenticated and login failed")

        return {
            "Authorization": self.jwt_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_projects(self) -> Dict[str, Any]:
        projects_url = f"{self.base_url}/api/projects"

        try:
            headers = self.get_headers()
            response = requests.get(projects_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise Exception("Get projects request timed out")
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to get projects: {e}"
            if hasattr(e, 'response') and e.response:
                error_msg += f"\nStatus: {e.response.status_code}"
            raise Exception(error_msg)

    def clear_authentication(self):
        self.jwt_token = None
        self._authenticated = False

    def is_authenticated(self) -> bool:
        return self._authenticated and self.jwt_token is not None
