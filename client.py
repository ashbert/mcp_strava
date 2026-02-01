# client.py
import json
import os
import requests
from datetime import datetime, timezone
from config import CLIENT_ID, CLIENT_SECRET

TOKEN_FILE = "token.json"

class StravaClient:
    def __init__(self):
        self.token_data = self._load_token()
        self.access_token = self.token_data.get("access_token")
        self.refresh_token = self.token_data.get("refresh_token")
        self.expires_at = self.token_data.get("expires_at")

    def _load_token(self):
        if not os.path.exists(TOKEN_FILE):
            raise FileNotFoundError("token.json not found")
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)

    def _save_token(self, new_data):
        with open(TOKEN_FILE, "w") as f:
            json.dump(new_data, f, indent=2)
        self.token_data = new_data
        self.access_token = new_data["access_token"]
        self.refresh_token = new_data["refresh_token"]
        self.expires_at = new_data["expires_at"]

    def _is_expired(self):
        now = datetime.now(timezone.utc).timestamp()
        return now >= self.expires_at

    def refresh_if_needed(self):
        if not self._is_expired():
            return

        print("Refreshing access token...")
        response = requests.post("https://www.strava.com/oauth/token", data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        })

        if response.status_code == 200:
            self._save_token(response.json())
            print("Token refreshed.")
        else:
            raise RuntimeError(f"Failed to refresh token: {response.text}")

    @property
    def headers(self):
        self.refresh_if_needed()
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_activities(self, per_page=20, page=1, after=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "per_page": per_page,
            "page": page
        }

        if after:
            params["after"] = after

        url = "https://www.strava.com/api/v3/athlete/activities"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch activities: {response.status_code} {response.text}")

        return response.json()
