from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException 
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from . import models
from .database import engine, SessionLocal 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Configure Postgresql dB connection
while True: 
    
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="R3public1898!", cursor_factory=RealDictCursor)  
        cursor = conn.cursor()
        print("dB connection successful")
        break
    except Exception as error: 
        print("Connecting to dB failed")
        print("Error: ", error)
        time.sleep(2)
    
my_posts = [{"title": "post 1 title", "content": "post 1 content", "id": 1}, {"title": "comfort foods", "content": "southern food", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index 
            
@app.get("/")
def root():
    return {"message": "This is your returned post"}

@app.get()

@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit
    return {"data": new_post}

# retrieve 1 post 
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return{"post_detail": post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
     
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id),)
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Object {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Object {id} not found")
    
  
    return {"data": updated_post}
