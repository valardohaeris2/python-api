from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = [{"title": "post 1 title", "content": "post 1 content", "id": 1}, {"title": "comfort foods", "content": "southern food", "id": 2}]

@app.get("/")
def root():
    return {"message": "Yo man"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# retrieve 1 post 
@app.get("/posts/{id}")
def get_post(id):
    print(id)
    return{"post_detail": f"This is your id {id}"} 
