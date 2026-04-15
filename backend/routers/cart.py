from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, models, database
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=schemas.CartOut)
def get_cart(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.u_id == current_user.u_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@router.post("/add")
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.u_id == current_user.u_id).first()
    
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.cart_id, 
        models.CartItem.p_id == item.p_id
    ).first()
    
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(cart_id=cart.cart_id, p_id=item.p_id, quantity=item.quantity)
        db.add(cart_item)
    
    db.commit()
    return {"message": "Item added to cart"}

@router.delete("/remove/{p_id}")
def remove_from_cart(p_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.u_id == current_user.u_id).first()
    cart_item = db.query(models.CartItem).filter(models.CartItem.cart_id == cart.cart_id, models.CartItem.p_id == p_id).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return {"message": "Item removed from cart"}
    raise HTTPException(status_code=404, detail="Item not found in cart")
