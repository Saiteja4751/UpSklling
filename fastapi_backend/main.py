from fastapi import FastAPI
from pydantic import BaseModel
import pymysql,time
import os
app = FastAPI()

# DB connection function
# def get_connection():
#     return pymysql.connect(
#         # host="localhost",
#         host = "mysql-db",  # ← change this if using Docker
#         user="root",
#         password="root",  # ← change this!
#         database="feedback_db",
#         cursorclass=pymysql.cursors.DictCursor
#     )

def get_connection():
    for i in range(10):  # retry 10 times
        try:
            conn = pymysql.connect(
                host=os.getenv("DB_HOST", "mysql-db"),
                # host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "root"),
                database=os.getenv("DB_NAME", "feedback_db"),
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✅ Connected to MySQL")
            return conn
        except Exception as e:
            print(f"❌ DB not ready, retrying... {i}")
            time.sleep(3)

    raise Exception("Database connection failed after retries")


@app.on_event("startup")
def startup():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            message TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()



# Pydantic model
class Feedback(BaseModel):
    name: str
    email: str
    message: str

# POST route
@app.post("/feedback/")
def submit_feedback(data: Feedback):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data.name, data.email, data.message))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Feedback submitted successfully!"}

# GET route
@app.get("/feedback/")
def get_feedback():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
