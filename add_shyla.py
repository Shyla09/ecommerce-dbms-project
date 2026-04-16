import sys
import os

# Add the backend directory to sys.path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database import SessionLocal
import backend.models as models
from backend.routers.auth import get_password_hash

def add_user():
    db = SessionLocal()
    try:
        email = "shyla@gmail.com"
        password = "rose11"
        
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            print(f"User {email} already exists. Updating password...")
            existing_user.password_hash = get_password_hash(password)
            db.commit()
            return

        print(f"Adding user {email}...")
        hashed_password = get_password_hash(password)
        new_user = models.User(
            first_name="Shyla",
            last_name="User",
            email=email,
            password_hash=hashed_password,
            phone_number="1234567890"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create cart for user
        cart = models.Cart(u_id=new_user.u_id)
        db.add(cart)
        db.commit()

        print(f"Successfully added user {email} with password {password}")

    except Exception as e:
        print(f"Error adding user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_user()
