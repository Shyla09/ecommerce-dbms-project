from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Table, CheckConstraint, DDL, event
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "User"
    u_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String(20))

    addresses = relationship("Address", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")

class Address(Base):
    __tablename__ = "Address"
    address_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("User.u_id", ondelete="CASCADE"), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)

    user = relationship("User", back_populates="addresses")

class Seller(Base):
    __tablename__ = "Seller"
    seller_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("User.u_id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String(150), nullable=False)

    products = relationship("Product", back_populates="seller")

class ProductCategory(Base):
    __tablename__ = "Product_Category"
    c_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "Product"
    __table_args__ = (
        CheckConstraint('p_stock >= 0', name='check_p_stock_positive'),
        CheckConstraint('p_price >= 0', name='check_p_price_positive'),
    )

    p_id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("Seller.seller_id", ondelete="CASCADE"), nullable=False)
    c_id = Column(Integer, ForeignKey("Product_Category.c_id", ondelete="SET NULL"))
    p_name = Column(String(200), nullable=False)
    p_price = Column(Float, nullable=False)
    p_description = Column(Text)
    p_image_url = Column(String(500))
    p_stock = Column(Integer, default=0, nullable=False)

    seller = relationship("Seller", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")

class Cart(Base):
    __tablename__ = "Cart"
    cart_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("User.u_id", ondelete="CASCADE"), unique=True, nullable=False)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "Cart_Items"
    cart_id = Column(Integer, ForeignKey("Cart.cart_id", ondelete="CASCADE"), primary_key=True)
    p_id = Column(Integer, ForeignKey("Product.p_id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "Order"
    __table_args__ = (
        CheckConstraint('order_amount >= 0', name='check_order_amount_positive'),
    )

    order_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("User.u_id", ondelete="CASCADE"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    order_amount = Column(Float, nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    tracking = relationship("TrackingDetail", back_populates="order")

class OrderItem(Base):
    __tablename__ = "Order_Items"
    order_id = Column(Integer, ForeignKey("Order.order_id", ondelete="CASCADE"), primary_key=True)
    p_id = Column(Integer, ForeignKey("Product.p_id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Payment(Base):
    __tablename__ = "Payment"
    payment_id = Column(Integer, primary_key=True, index=True)
    u_id = Column(Integer, ForeignKey("User.u_id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("Order.order_id", ondelete="CASCADE"), nullable=False)
    method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)

class TrackingDetail(Base):
    __tablename__ = "Tracking_Detail"
    t_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.order_id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="tracking")

# --- Triggers ---
trigger_ddl = DDL("""
CREATE TRIGGER update_stock_after_order
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    UPDATE Product
    SET p_stock = p_stock - NEW.quantity
    WHERE p_id = NEW.p_id;
END;
""")

event.listen(
    OrderItem.__table__,
    'after_create',
    trigger_ddl
)

