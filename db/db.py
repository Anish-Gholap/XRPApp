import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

class SupabaseSingleton:
    """Singleton class for Supabase client."""
    _instance = None


    @staticmethod
    def get_instance() -> Client:
        if SupabaseSingleton._instance is None:
            SupabaseSingleton._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return SupabaseSingleton._instance

# Create a single instance to be reused
supabase_client = SupabaseSingleton.get_instance()
