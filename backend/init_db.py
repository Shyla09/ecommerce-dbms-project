import pymysql
from database import Base, engine
import models

def init_db():
    try:
        # Connect to MySQL server without specifying a database to create the DB first
        conn = pymysql.connect(host='localhost', user='root', password='alpharose81')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS EcommerceDB;")
        conn.commit()
        cursor.close()
        conn.close()
        print("Database EcommerceDB created or already exists.")
        
        # Now create tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")
    except Exception as e:
        print(f"Error initializing DB: {e}")

if __name__ == "__main__":
    init_db()
