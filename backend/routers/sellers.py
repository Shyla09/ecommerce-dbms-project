from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import schemas, models, database
from routers.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=schemas.SellerOut)
def register_seller(seller: schemas.SellerCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Check if already a seller
    existing = db.query(models.Seller).filter(models.Seller.u_id == current_user.u_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already registered as a seller.")
    
    new_seller = models.Seller(u_id=current_user.u_id, company_name=seller.company_name)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

@router.get("/me", response_model=schemas.SellerOut)
def get_my_seller_profile(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    seller = db.query(models.Seller).filter(models.Seller.u_id == current_user.u_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
    return seller

@router.get("/analytics")
def get_seller_analytics(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    seller = db.query(models.Seller).filter(models.Seller.u_id == current_user.u_id).first()
    if not seller:
        raise HTTPException(status_code=403, detail="You are not a registered seller.")
    
    # Query the native SQL VIEW directly using text()
    query = text("SELECT p_name, total_units_sold, total_revenue FROM SellerSalesSummary WHERE seller_id = :sid")
    results = db.execute(query, {"sid": seller.seller_id}).fetchall()
    
    analytics = []
    for row in results:
        analytics.append({
            "p_name": row[0],
            "total_units_sold": row[1],
            "total_revenue": row[2]
        })
        
    return {"analytics": analytics}
