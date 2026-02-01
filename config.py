from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_CODE = os.getenv("AUTH_CODE")