from fastapi import HTTPException
from supabase import Client
from .deps import handle_supabase_error

def select_many(db: Client, table: str, *, filters: dict | None = None, order: str | None = None, limit: int = 100, offset: int = 0):
    try:
        q = db.table(table).select("*")
        for k, v in (filters or {}).items():
            if v is not None:
                q = q.eq(k, v)
        if order:
            q = q.order(order, desc=True)
        q = q.range(offset, offset + limit - 1)
        return q.execute().data
    except Exception as e:
        handle_supabase_error(e)

def select_one(db: Client, table: str, item_id: int | str):
    try:
        result = db.table(table).select("*").eq("id", item_id).single().execute()
        return result.data
    except Exception as e:
        if "0 rows" in str(e).lower() or "no rows" in str(e).lower():
            raise HTTPException(404, "Resource not found")
        handle_supabase_error(e)

def insert(db: Client, table: str, payload: dict):
    try:
        return db.table(table).insert(payload).execute().data
    except Exception as e:
        handle_supabase_error(e)

def update(db: Client, table: str, item_id: int | str, payload: dict):
    payload = {k: v for k, v in payload.items() if v is not None}
    try:
        return db.table(table).update(payload).eq("id", item_id).execute().data
    except Exception as e:
        handle_supabase_error(e)

def delete(db: Client, table: str, item_id: int | str):
    try:
        return db.table(table).delete().eq("id", item_id).execute().data
    except Exception as e:
        handle_supabase_error(e)

def require_role(db: Client, user_id: str, shop_id: int, allowed: list[str]):
    try:
        rows = db.table("shop_members").select("role").eq("shop_id", shop_id).eq("user_id", user_id).limit(1).execute().data
        if not rows or rows[0]["role"] not in allowed:
            raise HTTPException(403, f"Requires one of: {', '.join(allowed)}")
        return rows[0]["role"]
    except HTTPException:
        raise
    except Exception as e:
        handle_supabase_error(e)
