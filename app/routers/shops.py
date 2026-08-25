from fastapi import APIRouter, Depends
from supabase import Client
from ..deps import current_supabase, current_user
from ..crud import *
from ..schemas import ShopCreate, ShopUpdate, MemberCreate, MemberUpdate

router=APIRouter(tags=["Shops"])

@router.get("/shops")
def list_shops(db:Client=Depends(current_supabase), user=Depends(current_user)):
    # RLS filters to the user's memberships.
    return select_many(db,"shops",limit=500)

@router.post("/shops")
def create_shop(
    body: ShopCreate,
    db: Client = Depends(current_supabase),
    user=Depends(current_user),
):
    result = db.rpc(
        "create_shop",
        {
            "p_name": body.name,
            "p_phone": body.phone,
            "p_email": body.email,
            "p_address": body.address,
        },
    ).execute()

    if not result.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create shop",
        )

    return {
        "id": result.data,
        "message": "Shop created successfully",
        "role": "OWNER",
    }

@router.get("/shops/{shop_id}")
def get_shop(shop_id:int, db:Client=Depends(current_supabase), user=Depends(current_user)):
    return select_one(db,"shops",shop_id)

@router.patch("/shops/{shop_id}")
def update_shop(shop_id:int, body:ShopUpdate, db:Client=Depends(current_supabase), user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER"])
    return update(db,"shops",shop_id,body.model_dump(exclude_none=True))

@router.get("/shops/{shop_id}/members")
def members(shop_id:int, db:Client=Depends(current_supabase), user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"])
    return select_many(db,"shop_members",filters={"shop_id":shop_id},limit=500)

@router.post("/shops/{shop_id}/members")
def add_member(shop_id:int, body:MemberCreate, db:Client=Depends(current_supabase), user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER"])
    return insert(db,"shop_members",{"shop_id":shop_id,**body.model_dump(mode="json")})

@router.patch("/shops/{shop_id}/members/{member_id}")
def update_member(shop_id:int,member_id:int,body:MemberUpdate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER"])
    return update(db,"shop_members",member_id,body.model_dump(exclude_none=True))

@router.delete("/shops/{shop_id}/members/{member_id}")
def delete_member(shop_id:int,member_id:int,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER"])
    return delete(db,"shop_members",member_id)
