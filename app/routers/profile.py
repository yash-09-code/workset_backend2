from fastapi import APIRouter, Depends
from supabase import Client
from ..deps import current_supabase,current_user
from ..crud import select_one,update
from ..schemas import ProfileUpdate
router=APIRouter(prefix="/profile",tags=["Profile"])
@router.get("")
def get_profile(db:Client=Depends(current_supabase),user=Depends(current_user)):
    return select_one(db,"profiles",user["id"])
@router.patch("")
def update_profile(body:ProfileUpdate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    return update(db,"profiles",user["id"],body.model_dump(exclude_none=True))
