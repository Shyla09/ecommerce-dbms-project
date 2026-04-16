import os
import sys

from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from routers.auth import get_password_hash

def seed_db():
    db = SessionLocal()
    try:
        # Check if users exist to prevent dual seed
        if db.query(models.User).count() > 0:
            print("Database already seeded!")
            return
        
        print("Seeding database...")

        # 1. Create a User (Admin/Seller)
        hashed_password = get_password_hash("admin123")
        admin_user = models.User(
            first_name="Admin",
            last_name="ShopSphere",
            email="admin@shopsphere.com",
            password_hash=hashed_password,
            phone_number="18001234567"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # Ensure Cart exists for user
        admin_cart = models.Cart(u_id=admin_user.u_id)
        db.add(admin_cart)
        db.commit()

        # 2. Register Seller
        seller = models.Seller(
            u_id=admin_user.u_id,
            company_name="ShopSphere Official"
        )
        db.add(seller)
        db.commit()
        db.refresh(seller)

        # 3. Create Categories
        categories = ["Electronics", "Home Decor", "Apparel", "Footwear"]
        cat_map = {}
        for c in categories:
            cat = models.ProductCategory(name=c)
            db.add(cat)
            db.commit()
            db.refresh(cat)
            cat_map[c] = cat.c_id

        # 4. Create Products
        products = [
            {
                "name": "Wireless Noise-Cancelling Headphones", 
                "price": 299.99, 
                "desc": "Experience true silence with these premium over-ear headphones featuring 40 hours of battery life and crystal clear audio.",
                "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=80",
                "cat": "Electronics"
            },
            {
                "name": "Minimalist Smartwatch", 
                "price": 199.50, 
                "desc": "Track your fitness and stay connected with this sleek, water-resistant smartwatch.",
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1000&q=80",
                "cat": "Electronics"
            },
            {
                "name": "Ceramic Artisan Coffee Mug", 
                "price": 24.00, 
                "desc": "Hand-crafted ceramic mug perfect for your morning brew. Microwave and dishwasher safe.",
                "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=1000&q=80",
                "cat": "Home Decor"
            },
            {
                "name": "Classic Denim Jacket", 
                "price": 89.99, 
                "desc": "Timeless vintage wash denim jacket. Perfect for layering in any season.",
                "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=1000&q=80",
                "cat": "Apparel"
            },
            {
                "name": "Running Sneakers 'Aero'", 
                "price": 129.00, 
                "desc": "Lightweight breathable mesh sneakers designed for maximum speed and comfort.",
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1000&q=80",
                "cat": "Footwear"
            },
            {
                "name": "Mechanical Gaming Keyboard", 
                "price": 149.99, 
                "desc": "RGB backlit mechanical keyboard with tactile switches for satisfying typing and gaming.",
                "image": "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=1000&q=80",
                "cat": "Electronics"
            },
            {
                "name": "Ergonomic Office Chair", 
                "price": 249.00, 
                "desc": "High-back ergonomic mesh office chair with adjustable lumbar support.",
                "image": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?auto=format&fit=crop&w=1000&q=80",
                "cat": "Home Decor"
            },
            {
                "name": "Stainless Steel Water Bottle", 
                "price": 35.00, 
                "desc": "Vacuum insulated reusable water bottle keeping drinks cold for 24 hours.",
                "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=1000&q=80",
                "cat": "Home Decor"
            },
            {
                "name": "Leather Messenger Bag", 
                "price": 115.50, 
                "desc": "Genuine leather messenger bag featuring multiple compartments and adjustable strap.",
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=80",
                "cat": "Apparel"
            },
            {
                "name": "Hiking Backpack 40L", 
                "price": 85.00, 
                "desc": "Durable and water-resistant 40L hiking backpack with rain cover.",
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=80",
                "cat": "Apparel"
            }
        ]

        for p in products:
            prod = models.Product(
                seller_id=seller.seller_id,
                c_id=cat_map[p["cat"]],
                p_name=p["name"],
                p_price=p["price"],
                p_description=p["desc"],
                p_image_url=p["image"],
                p_stock=50
            )
            db.add(prod)
        
        db.commit()
        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
