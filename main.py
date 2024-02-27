from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title1", "content": "content1", "id":1},{"title": "title2", "content": "content2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/posts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"Create": f"title {payload['title']} content {payload['content']}"}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data":  post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post= my_posts[len(my_posts)-1]
    print(post)
    return {"latest_post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    post= find_post(int(id))
    print(post)
    return {"post_detail" : post} 
