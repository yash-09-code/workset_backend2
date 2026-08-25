from supabase import create_client, Client
from .config import get_settings


def get_public_supabase() -> Client:
    """Create a client for public Supabase Auth operations."""
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_anon_key)


def get_supabase(access_token: str | None = None) -> Client:
    """Create a client whose PostgREST requests run as the authenticated user."""
    client = get_public_supabase()
    if access_token:
        client.postgrest.auth(access_token)
    return client
