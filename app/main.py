from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers import auth, shops, profile, resources

s=get_settings()
app=FastAPI(title=s.app_name,version="1.0.0",description="Business management API backed by Supabase and protected by Supabase RLS.")
app.add_middleware(CORSMiddleware,allow_origins=s.cors_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.get("/health",tags=["System"])
def health():
    return {"status":"ok","service":s.app_name}

app.include_router(auth.router,prefix=s.api_prefix)
app.include_router(shops.router,prefix=s.api_prefix)
app.include_router(profile.router,prefix=s.api_prefix)
app.include_router(resources.router,prefix=s.api_prefix)
