from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None

class UserOut(BaseModel):
    u_id: int
    first_name: str
    last_name: str
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductBase(BaseModel):
    p_name: str
    p_price: float
    p_description: Optional[str] = None
    p_image_url: Optional[str] = None
    p_stock: int
    c_id: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    p_id: int
    seller_id: int
    class Config:
        orm_mode = True

class CartItemCreate(BaseModel):
    p_id: int
    quantity: int

class CartItemOut(BaseModel):
    p_id: int
    quantity: int
    product: ProductOut
    class Config:
        orm_mode = True

class CartOut(BaseModel):
    cart_id: int
    items: List[CartItemOut] = []
    class Config:
        orm_mode = True

class SellerCreate(BaseModel):
    company_name: str

class SellerOut(BaseModel):
    seller_id: int
    u_id: int
    company_name: str
    class Config:
        orm_mode = True
