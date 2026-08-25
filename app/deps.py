from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

from .supabase import get_supabase


security = HTTPBearer(auto_error=False)


def bearer_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials.strip()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token is empty",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("TOKEN RECEIVED:", token[:30] + "...")

    return token


def current_supabase(
    token: str = Depends(bearer_token),
) -> Client:
    return get_supabase(token)


def current_user(
    token: str = Depends(bearer_token),
    supabase: Client = Depends(current_supabase),
) -> dict:

    try:
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = response.user

        return {
            "id": str(user.id),
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
        }

    except HTTPException:
        raise

    except Exception as e:
        print("SUPABASE AUTH ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def handle_supabase_error(exc: Exception):
    msg = str(exc)
    low = msg.lower()
    if "permission" in low or "row-level security" in low or "not allowed" in low:
        raise HTTPException(status_code=403, detail="Database policy denied this operation")
    if "duplicate" in low or "unique" in low:
        raise HTTPException(status_code=409, detail="Resource already exists")
    raise HTTPException(status_code=400, detail=msg)
