from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from ..schemas import AuthSignup, AuthLogin, RefreshRequest
from ..deps import current_supabase, current_user, bearer_token
from ..supabase import get_public_supabase

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(body: AuthSignup):
    """Public endpoint: no access token is required to create an account."""
    try:
        db = get_public_supabase()
        result = db.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {"data": {"name": body.name, "phone": body.phone}},
        })
        if not result.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed",
            )
        return {
            "user": {"id": str(result.user.id), "email": result.user.email},
            "session": result.session,
        }
    except HTTPException:
        raise
    except Exception as e:
        msg = str(e).lower()
        if "already registered" in msg or "already exists" in msg:
            raise HTTPException(status_code=409, detail="Email is already registered")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(body: AuthLogin):
    """Public endpoint: exchanges credentials for an access/refresh token pair."""
    try:
        db = get_public_supabase()
        result = db.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })
        if not result.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "expires_in": result.session.expires_in,
            "token_type": "bearer",
            "user": {
                "id": str(result.user.id),
                "email": result.user.email,
            },
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh")
def refresh(body: RefreshRequest):
    """Public endpoint: refresh tokens do not require the old access token."""
    try:
        db = get_public_supabase()
        result = db.auth.refresh_session(body.refresh_token)
        if not result.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "expires_in": result.session.expires_in,
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
def logout(
    db: Client = Depends(current_supabase),
    token: str = Depends(bearer_token),
):
    """Protected endpoint: requires a valid access token."""
    try:
        db.auth.sign_out()
        return {"message": "Logged out"}
    except Exception:
        # A valid token has already been required. Logout is idempotent.
        return {"message": "Logged out"}


@router.get("/me")
def me(user=Depends(current_user)):
    """Protected endpoint: requires a valid access token."""
    return user
