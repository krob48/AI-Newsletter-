import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path=".env")

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Add these defaults
DEFAULT_TOPICS = ["ai", "technology"]
MAX_ARTICLES = 5

print("Loaded Guardian key?", bool(GUARDIAN_API_KEY))


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_NAME = os.getenv("FROM_NAME", "AI Newsletter")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
