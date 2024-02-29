from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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

# cursor_factory=RealDictCursor <- this line just includes the column name also
# if not included then it will only return values, so to include column name we use it
# in the following code while loop will keep running until a succesfull connection is not established
# if  connection is not successfull then it sleeps for 2 seconds then executes while loop again
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# @app.post("/posts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"Create": f"title {payload['title']} content {payload['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)
    # %s is written to prevent sql injection
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    # commit is done to save data in db
    conn.commit()
    return {"data":  new_post}


@app.get("/posts/latest")
def get_latest_post():
    post= my_posts[len(my_posts)-1]
    print(post)
    return {"latest_post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s)""", (str(id)) )
    post= cursor.fetchone()
    # post= find_post(int(id))
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")
    return {"post_detail" : post} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ):
    cursor.execute("""DELETE FROM posts WHERE id = (%s)""", (str(id)) )
    deleted_post= cursor.fetchone()
    conn.commit()
    # index= find_post_index(id)
    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, published = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.published, post.content, str(id)))
    updated_post= cursor.fetchone()
    conn.commit()
    # index= find_post_index(id)
    if not updated_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with {id} does not exist ")

    return {"data" : updated_post}
