from dotenv import load_dotenv
import os

load_dotenv()


DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")