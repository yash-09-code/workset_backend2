# FastAPI + Supabase Business Management API

Generated from the supplied Supabase schema/RLS export.

## Stack
- FastAPI
- Supabase Auth
- Supabase PostgREST (requests use the caller's JWT, so Supabase RLS remains the final authorization layer)
- Pydantic Settings

## Run
1. Copy `.env.example` to `.env`.
2. Set `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
3. Install: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --reload`

Docs:
- `/docs`
- `/redoc`
- `/health`

## Authentication
Use:
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

For protected endpoints send:
`Authorization: Bearer <supabase_access_token>`

## Important RLS design
The API intentionally uses the user's access token when calling Supabase. Do not replace this with the service-role key for normal requests, because the service role bypasses RLS.

The database policies in the supplied export include:
- shop membership checks
- OWNER/ADMIN management for categories, products, suppliers, purchases and expenses
- OWNER-only shop-member management
- OWNER shop updates
- OWNER/ADMIN/EMPLOYEE sale creation
- own-profile access

The API adds friendly 401/403 checks where practical, but database RLS is authoritative.

## Schema covered
`shops`, `shop_members`, `profiles`, `categories`, `suppliers`, `products`, `purchases`, `purchase_items`, `sales`, `sale_items`, `expenses`, `inventory_transactions`, `employee_salaries`, and `shop_dashboard`.

Auth is delegated to Supabase Auth rather than exposing `auth.users`.


## Authentication behavior

Public authentication endpoints do NOT require an Authorization header:

- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`

Protected endpoints require:

`Authorization: Bearer <supabase_access_token>`

Missing/invalid access tokens return `401 Unauthorized` with `WWW-Authenticate: Bearer`.
Valid authentication with an RLS-denied database operation returns `403 Forbidden`.
The API does not use the service-role key for normal user requests, so Supabase RLS remains effective.
