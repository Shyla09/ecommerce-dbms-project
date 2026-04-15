from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    seller = db.query(models.Seller).filter(models.Seller.u_id == current_user.u_id).first()
    if not seller:
        raise HTTPException(status_code=403, detail="You are not a registered seller")
    
    new_product = models.Product(**product.dict(), seller_id=seller.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/{p_id}", response_model=schemas.ProductOut)
def get_product(p_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.p_id == p_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
