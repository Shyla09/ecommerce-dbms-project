from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from routers.auth import get_current_user

router = APIRouter()

@router.post("/checkout")
def checkout(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    try:
        cart = db.query(models.Cart).filter(models.Cart.u_id == current_user.u_id).first()
        if not cart or not cart.items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        total_amount = 0
        product_items = []
        for item in cart.items:
            # Concurrency Control: Pessimistic Locking via .with_for_update()
            product = db.query(models.Product).filter(models.Product.p_id == item.p_id).with_for_update().first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            if product.p_stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.p_name}")
            total_amount += product.p_price * item.quantity
            product_items.append({"product": product, "item": item})

        new_order = models.Order(u_id=current_user.u_id, order_amount=total_amount)
        db.add(new_order)
        db.flush() # Send inserts to database to generate ID, without ending transaction

        for pi in product_items:
            product = pi["product"]
            item = pi["item"]
            order_item = models.OrderItem(
                order_id=new_order.order_id,
                p_id=item.p_id,
                quantity=item.quantity,
                price_at_purchase=product.p_price
            )
            db.add(order_item)
            # The database trigger "update_stock_after_order" will automatically deduct product stock here
            db.delete(item)  # Clear cart

        # Fake payment
        payment = models.Payment(u_id=current_user.u_id, order_id=new_order.order_id, method="Credit Card", amount=total_amount)
        db.add(payment)

        # Initial tracking
        tracking = models.TrackingDetail(order_id=new_order.order_id, status="Processing")
        db.add(tracking)

        db.commit() # Single transaction commit
        return {"message": "Order placed successfully", "order_id": new_order.order_id, "amount": total_amount}

    except HTTPException as httpe:
        db.rollback()
        raise httpe
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/detailed-history")
def detailed_history(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Using Explicit SQL JOIN to combine multiple tables efficiently
    results = (
        db.query(models.Order, models.OrderItem, models.Product)
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.OrderItem.p_id == models.Product.p_id)
        .filter(models.Order.u_id == current_user.u_id)
        .order_by(models.Order.order_date.desc())
        .all()
    )

    history = []
    for order, order_item, product in results:
        history.append({
            "order_id": order.order_id,
            "order_date": order.order_date,
            "product_name": product.p_name,
            "quantity": order_item.quantity,
            "price_at_purchase": order_item.price_at_purchase
        })

    return {"history": history}
