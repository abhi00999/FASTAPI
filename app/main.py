from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title1", "content": "content1", "id":1},{"title": "title2", "content": "content2", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# the following function will give the index of dictionary with that specific id
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} does not exist "}
    print(post)
    return {"post_detail" : post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ):
    index= find_post_index(id)
    if not index:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index= find_post_index(id)
    if not index:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")
    
    post_dict= post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data" : post_dict}
