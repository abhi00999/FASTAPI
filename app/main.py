from random import randrange
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

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

# what we've basically done here is, I have basically said as we, you know, when we get a path, 
# when we get a HTTP request, you know, before we had all of our path operations in here, instead, 
# what's going to happen is, you know, we go down the list like we normally do. 
# And so as we go down our list, this is our first app object that we kind of reference. 
# And in here, it just says, I want you to include everything, I want you to include our post dot router. 
# And so the request will then go into here. And it's going to take a look at all of these routes. 
# And it's going to see if it's a match. And if it finds a match, it's going to respond like it normally does.
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



