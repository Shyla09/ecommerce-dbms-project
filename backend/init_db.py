import os
import pymysql
from database import Base, engine
import models
from dotenv import load_dotenv

load_dotenv()

def init_db():
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "root")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "EcommerceDB")

    try:
        # Connect to MySQL server without specifying a database to create the DB first
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database {db_name} created or already exists.")
        
        # Now create tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")
    except Exception as e:
        print(f"Error initializing DB: {e}")

if __name__ == "__main__":
    init_db()
