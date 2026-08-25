from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class AuthSignup(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str | None = None
    phone: str | None = None

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int | None = None
    token_type: str = "bearer"
    user: dict[str, Any]

class ProfileUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

class ShopCreate(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None

class ShopUpdate(ShopCreate):
    pass

class MemberCreate(BaseModel):
    user_id: UUID
    role: Literal["OWNER","ADMIN","EMPLOYEE"]
    salary: Decimal | None = None

class MemberUpdate(BaseModel):
    role: Literal["OWNER","ADMIN","EMPLOYEE"] | None = None
    salary: Decimal | None = None

class CategoryCreate(BaseModel):
    shop_id: int
    name: str
    description: str | None = None

class SupplierCreate(BaseModel):
    shop_id: int
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    description: str | None = None

class ProductCreate(BaseModel):
    shop_id: int
    category_id: int | None = None
    supplier_id: int | None = None
    name: str
    selling_price: Decimal = Decimal("0")
    purchase_price: Decimal = Decimal("0")
    stock_quantity: Decimal = Decimal("0")
    low_stock_threshold: Decimal = Decimal("5")
    description: str | None = None

class ProductUpdate(ProductCreate):
    shop_id: int | None = None

class PurchaseCreate(BaseModel):
    shop_id: int
    supplier_id: int | None = None
    recorded_by: UUID | None = None
    purchase_type: str
    reference_number: str | None = None
    total_amount: Decimal = Decimal("0")
    description: str | None = None
    purchase_date: datetime | None = None

class PurchaseItemCreate(BaseModel):
    purchase_id: int
    product_id: int
    quantity: Decimal
    unit_cost: Decimal
    subtotal: Decimal

class SaleCreate(BaseModel):
    shop_id: int
    bill_number: str
    sold_by: UUID | None = None
    subtotal: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    discount: Decimal = Decimal("0")
    total: Decimal = Decimal("0")

class SaleItemCreate(BaseModel):
    sale_id: int
    product_id: int
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal

class ExpenseCreate(BaseModel):
    shop_id: int
    expense_type: str
    amount: Decimal
    description: str | None = None
    expense_date: date | None = None
    purchase_id: int | None = None
    created_by: UUID | None = None

class InventoryTransactionCreate(BaseModel):
    shop_id: int
    product_id: int
    transaction_type: str
    quantity: Decimal
    reference_id: int | None = None
    notes: str | None = None
    created_by: UUID | None = None

class SalaryCreate(BaseModel):
    shop_member_id: int
    amount: Decimal
    salary_month: date
    paid_at: datetime | None = None
    status: Literal["PENDING","PAID"] = "PENDING"

class SalaryUpdate(BaseModel):
    amount: Decimal | None = None
    paid_at: datetime | None = None
    status: Literal["PENDING","PAID"] | None = None
