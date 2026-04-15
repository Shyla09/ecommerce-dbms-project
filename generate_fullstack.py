import os

def create_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# ---- BACKEND FILES ----

create_file("backend/database.py", """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with actual DB URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/EcommerceDB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

create_file("backend/models.py", """
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Table
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
""")

create_file("backend/schemas.py", """
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
""")

create_file("backend/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, products, cart, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/")
def root():
    return {"message": "Welcome to E-Commerce API"}
""")

create_file("backend/routers/auth.py", """
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from datetime import datetime, timedelta
import schemas, models, database
from passlib.context import CryptContext
from jose import JWTError, jwt

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.u_id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed_password,
        phone_number=user.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Auto-create empty cart
    new_cart = models.Cart(u_id=new_user.u_id)
    db.add(new_cart)
    db.commit()
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.u_id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
""")


create_file("backend/routers/products.py", """
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
""")

create_file("backend/routers/cart.py", """
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
""")

create_file("backend/routers/orders.py", """
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
""")


# ---- FRONTEND FILES ----
create_file("frontend/package.json", """
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "lucide-react": "^0.292.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}
""")

create_file("frontend/vite.config.ts", """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
""")

create_file("frontend/tailwind.config.js", """
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
""")

create_file("frontend/postcss.config.js", """
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")

create_file("frontend/index.html", """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>E-Commerce App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

create_file("frontend/src/index.css", """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}
""")

create_file("frontend/src/main.tsx", """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { AuthProvider } from './context/AuthContext'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>,
)
""")

create_file("frontend/src/api/axios.ts", """
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // FastAPI server
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
""")

create_file("frontend/src/context/AuthContext.tsx", """
import React, { createContext, useState, useEffect } from 'react';
import api from '../api/axios';

export const AuthContext = createContext<{user: any, login: (t: string) => void, logout: () => void}>({
  user: null, login: () => {}, logout: () => {}
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<any>(null);

  const fetchUser = async () => {
    try {
      const res = await api.get('/auth/me');
      setUser(res.data);
    } catch {
      setUser(null);
    }
  };

  useEffect(() => {
    if (localStorage.getItem('token')) {
      fetchUser();
    }
  }, []);

  const login = (token: string) => {
    localStorage.setItem('token', token);
    fetchUser();
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
""")

create_file("frontend/src/App.tsx", """
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Home from './pages/Home';
import Cart from './pages/Cart';
import Auth from './pages/Auth';

function Navbar() {
  const { user, logout } = useContext(AuthContext);
  return (
    <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold text-indigo-600">ShopSphere</Link>
      <div className="flex gap-4">
        <Link to="/cart" className="text-gray-600 hover:text-indigo-600">Cart</Link>
        {user ? (
          <button onClick={logout} className="text-gray-600 hover:text-red-600">Logout</button>
        ) : (
          <Link to="/auth" className="text-gray-600 hover:text-indigo-600">Login/Signup</Link>
        )}
      </div>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="container mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/auth" element={<Auth />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
""")

create_file("frontend/src/pages/Home.tsx", """
import { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Home() {
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    api.get('/products').then(res => setProducts(res.data)).catch(console.error);
  }, []);

  const addToCart = async (p_id: int) => {
    try {
      await api.post('/cart/add', { p_id, quantity: 1 });
      alert('Added to cart!');
    } catch {
      alert('Please login first');
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Our Products</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map(p => (
          <div key={p.p_id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
            <h2 className="text-xl font-semibold mb-2">{p.p_name}</h2>
            <p className="text-gray-600 mb-4">{p.p_description}</p>
            <div className="flex justify-between items-center">
              <span className="text-lg font-bold text-indigo-600">${p.p_price}</span>
              <button 
                onClick={() => addToCart(p.p_id)}
                className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
              >
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
""")

create_file("frontend/src/pages/Auth.tsx", """
import { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({email: '', password: '', first_name: '', last_name: ''});
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', form.email);
        formData.append('password', form.password);
        const res = await api.post('/auth/login', formData);
        login(res.data.access_token);
      } else {
        await api.post('/auth/signup', form);
        alert('Signup successful! Please login.');
        setIsLogin(true);
        return;
      }
      navigate('/');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error occurred');
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-xl shadow-sm mt-10">
      <h2 className="text-2xl font-bold mb-6 text-center">{isLogin ? 'Login' : 'Sign Up'}</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {!isLogin && (
          <>
            <input className="border p-2 rounded" placeholder="First Name" required onChange={e => setForm({...form, first_name: e.target.value})} />
            <input className="border p-2 rounded" placeholder="Last Name" required onChange={e => setForm({...form, last_name: e.target.value})} />
          </>
        )}
        <input className="border p-2 rounded" type="email" placeholder="Email" required onChange={e => setForm({...form, email: e.target.value})} />
        <input className="border p-2 rounded" type="password" placeholder="Password" required onChange={e => setForm({...form, password: e.target.value})} />
        <button className="bg-indigo-600 text-white py-2 rounded font-semibold">{isLogin ? 'Login' : 'Sign Up'}</button>
      </form>
      <p className="mt-4 text-center cursor-pointer text-indigo-600" onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Need an account? Sign up' : 'Have an account? Login'}
      </p>
    </div>
  );
}
""")

create_file("frontend/src/pages/Cart.tsx", """
import { useEffect, useState } from 'react';
import api from '../api/axios';

export default function Cart() {
  const [cart, setCart] = useState<any>(null);

  const fetchCart = () => {
    api.get('/cart').then(res => setCart(res.data)).catch(console.error);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const handleCheckout = async () => {
    try {
      await api.post('/orders/checkout');
      alert('Order Placed Successfully!');
      fetchCart();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Checkout failed');
    }
  };

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded-xl shadow-sm">
      <h2 className="text-2xl font-bold mb-6">Your Cart</h2>
      {!cart || cart.items?.length === 0 ? (
        <p className="text-gray-500">Your cart is empty.</p>
      ) : (
        <div>
          {cart.items.map((item: any) => (
            <div key={item.p_id} className="flex justify-between items-center border-b py-4">
              <div>
                <span className="font-semibold">{item.product.p_name}</span> x {item.quantity}
              </div>
              <span className="text-indigo-600 font-bold">${item.product.p_price * item.quantity}</span>
            </div>
          ))}
          <div className="mt-6 flex justify-end">
            <button onClick={handleCheckout} className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition">
              Checkout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
""")

create_file("README.md", """
# Full-Stack E-Commerce System

This project is a scalable, full-stack e-commerce system using FastAPI (Python Backend), React+Vite+Tailwind (Frontend) and MySQL database.

## System Features
- **User Authentication:** JWT based secure signup/login.
- **Product Listing:** API routing to display registered products.
- **Cart Management:** Endpoints and state mapped logic for active carts.
- **Orders & Tracking:** Cart checkout mechanism handling stock and generating orders + fake payment verification + shipping status mappings.
- **Relational DB:** Complete mapping of Users, Sellers, Products, Orders, Cart, and Payments according to the `schema.sql` guidelines.

---

## 1. Backend Setup (FastAPI)

1. Create a Python Virtual Environment:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Update Datebase Connection:
   In `backend/database.py`, modify `SQLALCHEMY_DATABASE_URL` with your actual MySQL credentials.
   *(Since you have the raw `schema.sql`, you could run `mysql -u root -p EcommerceDB < schema.sql` inside your DB first, or let SQLAlchemy create the schemas automatically on startup via `Base.metadata.create_all(bind=engine)`).*
4. Run the API Server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

---

## 2. Frontend Setup (React setup with Node based tools)

*Note: You need `npm` or `yarn` installed on your machine to start the frontend.*

1. Move to frontend:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```

## 3. Database SQL Files

You can examine the pure relational requirements in the newly created `schema.sql`. The logic conforms strongly to constraints, cascades, and types defined there.
""")
