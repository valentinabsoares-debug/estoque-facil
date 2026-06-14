import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)
