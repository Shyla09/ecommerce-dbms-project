from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from routers.auth import get_current_user

router = APIRouter()

@router.post("/checkout")
def checkout(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.u_id == current_user.u_id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    for item in cart.items:
        product = db.query(models.Product).filter(models.Product.p_id == item.p_id).first()
        if product.p_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.p_name}")
        total_amount += product.p_price * item.quantity

    new_order = models.Order(u_id=current_user.u_id, order_amount=total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart.items:
        product = db.query(models.Product).filter(models.Product.p_id == item.p_id).first()
        order_item = models.OrderItem(
            order_id=new_order.order_id,
            p_id=item.p_id,
            quantity=item.quantity,
            price_at_purchase=product.p_price
        )
        db.add(order_item)
        product.p_stock -= item.quantity  # Decrease stock
        db.delete(item)  # Clear cart

    # Fake payment
    payment = models.Payment(u_id=current_user.u_id, order_id=new_order.order_id, method="Credit Card", amount=total_amount)
    db.add(payment)

    # Initial tracking
    tracking = models.TrackingDetail(order_id=new_order.order_id, status="Processing")
    db.add(tracking)

    db.commit()
    return {"message": "Order placed successfully", "order_id": new_order.order_id, "amount": total_amount}
