from celery import Celery
import time
import mysql.connector
import redis

# Initialize Celery
app = Celery('stock_worker', broker='redis://localhost:6379/0')

# MySQL connection configuration
db_config = {
    'user': 'your_user',
    'password': 'your_password',
    'host': '127.0.0.1',
    'database': 'your_database',
}

# Initialize Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Predefined threshold for low inventory
LOW_INVENTORY_THRESHOLD = 10

@app.task
def check_stock_levels():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Query to get stock levels
        cursor.execute("SELECT product_id, stock_level FROM products")
        products = cursor.fetchall()
        
        for product in products:
            if product['stock_level'] < LOW_INVENTORY_THRESHOLD:
                # Publish low inventory alert to Redis
                r.publish('low_inventory_alerts', f'Product ID {product['product_id']} is low on stock!')
        
    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        if conn:
            cursor.close()
            conn.close()

# Schedule the task to run every 60 seconds
while True:
    check_stock_levels.delay()
    time.sleep(60)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Constants
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI instance
app = FastAPI()

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database simulation
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": pwd_context.hash("testpassword"),
        "disabled": False,
    }
}

fake_stock_db = {
    "part1": 100,
    "part2": 50,
}

# Models
class User(BaseModel):
    username: str
    full_name: str = None
    email: str = None
    disabled: bool = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class StockUpdate(BaseModel):
    part_name: str
    quantity: int

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Invalidate the token (implementation depends on your strategy)
    return {"msg": "Logged out"}

@app.get("/stock", response_model=List[str])
async def get_stock(token: str = Depends(oauth2_scheme)):
    return list(fake_stock_db.items())

@app.put("/stock/update", response_model=dict)
async def update_stock(stock_update: StockUpdate, token: str = Depends(oauth2_scheme)):
    if stock_update.part_name in fake_stock_db:
        fake_stock_db[stock_update.part_name] += stock_update.quantity
        return {"msg": "Stock updated", "new_stock_level": fake_stock_db[stock_update.part_name]}
    else:
        raise HTTPException(status_code=404, detail="Part not found")
