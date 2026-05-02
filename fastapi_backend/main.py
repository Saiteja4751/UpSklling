from fastapi import FastAPI
from pydantic import BaseModel
import pymysql

app = FastAPI()

# DB connection function
def get_connection():
    return pymysql.connect(
        host="localhost",
        # host = "mysql-db",  # ← change this if using Docker
        user="root",
        password="root",  # ← change this!
        database="feedback_db",
        cursorclass=pymysql.cursors.DictCursor
    )

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
