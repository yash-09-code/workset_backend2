from fastapi import APIRouter, Depends
from supabase import Client
from ..deps import current_supabase,current_user
from ..crud import *
from ..schemas import *

router=APIRouter(tags=["Business"])

def make_list(db, table, shop_id, limit, offset):
    return select_many(db,table,filters={"shop_id":shop_id},order="created_at",limit=limit,offset=offset)

@router.get("/shops/{shop_id}/categories")
def categories(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"categories",shop_id,limit,offset)
@router.post("/shops/{shop_id}/categories")
def category_create(shop_id:int,body:CategoryCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"]); return insert(db,"categories",body.model_dump())

@router.get("/shops/{shop_id}/suppliers")
def suppliers(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"suppliers",shop_id,limit,offset)
@router.post("/shops/{shop_id}/suppliers")
def supplier_create(shop_id:int,body:SupplierCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"]); return insert(db,"suppliers",body.model_dump(exclude_none=True))

@router.get("/shops/{shop_id}/products")
def products(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"products",shop_id,limit,offset)
@router.post("/shops/{shop_id}/products")
def product_create(shop_id:int,body:ProductCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"]); return insert(db,"products",body.model_dump(exclude_none=True))
@router.patch("/products/{product_id}")
def product_update(product_id:int,body:ProductUpdate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    if body.shop_id is not None: require_role(db,user["id"],body.shop_id,["OWNER","ADMIN"])
    row=select_one(db,"products",product_id); require_role(db,user["id"],row["shop_id"],["OWNER","ADMIN"])
    return update(db,"products",product_id,body.model_dump(exclude_none=True,exclude={"shop_id"}))

@router.get("/shops/{shop_id}/purchases")
def purchases(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"purchases",shop_id,limit,offset)
@router.post("/shops/{shop_id}/purchases")
def purchase_create(shop_id:int,body:PurchaseCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"]); return insert(db,"purchases",body.model_dump(exclude_none=True))

@router.post("/purchases/{purchase_id}/items")
def purchase_item_create(purchase_id:int,body:PurchaseItemCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    p=select_one(db,"purchases",purchase_id); require_role(db,user["id"],p["shop_id"],["OWNER","ADMIN"])
    return insert(db,"purchase_items",{**body.model_dump(),"purchase_id":purchase_id})

@router.get("/shops/{shop_id}/sales")
def sales(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"sales",shop_id,limit,offset)
@router.post("/shops/{shop_id}/sales")
def sale_create(shop_id:int,body:SaleCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return insert(db,"sales",body.model_dump(exclude_none=True))

@router.post("/sales/{sale_id}/items")
def sale_item_create(sale_id:int,body:SaleItemCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    s=select_one(db,"sales",sale_id); require_role(db,user["id"],s["shop_id"],["OWNER","ADMIN","EMPLOYEE"])
    return insert(db,"sale_items",{**body.model_dump(),"sale_id":sale_id})

@router.get("/shops/{shop_id}/expenses")
def expenses(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"expenses",shop_id,limit,offset)
@router.post("/shops/{shop_id}/expenses")
def expense_create(shop_id:int,body:ExpenseCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"]); return insert(db,"expenses",body.model_dump(exclude_none=True))

@router.get("/shops/{shop_id}/inventory")
def inventory(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return make_list(db,"inventory_transactions",shop_id,limit,offset)
@router.post("/shops/{shop_id}/inventory")
def inventory_create(shop_id:int,body:InventoryTransactionCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"]); return insert(db,"inventory_transactions",body.model_dump(exclude_none=True))

@router.get("/shops/{shop_id}/salaries")
def salaries(shop_id:int,limit:int=100,offset:int=0,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"])
    rows=db.table("shop_members").select("id").eq("shop_id",shop_id).execute().data
    ids=[x["id"] for x in rows]
    if not ids:return []
    return db.table("employee_salaries").select("*").in_("shop_member_id",ids).range(offset,offset+limit-1).execute().data

@router.post("/shops/{shop_id}/salaries")
def salary_create(shop_id:int,body:SalaryCreate,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN"])
    return insert(db,"employee_salaries",body.model_dump(exclude_none=True))

@router.get("/shops/{shop_id}/dashboard")
def dashboard(shop_id:int,db:Client=Depends(current_supabase),user=Depends(current_user)):
    require_role(db,user["id"],shop_id,["OWNER","ADMIN","EMPLOYEE"])
    try:
        return db.table("shop_dashboard").select("*").eq("shop_id",shop_id).single().execute().data
    except Exception as e:
        handle_supabase_error(e)
