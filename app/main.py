from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app=FastAPI()



class Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating:Optional[int] =None


try: 
    conn=psycopg2.connect(host='host',database='databse',port='port',user='dummyuser',password='dummypassword',cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("successfully connected")
except Exception as error:
    print("failed to connect")
    time.sleep(45)




my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{
    "title":"title of post 2","content":"content of post 2","id":2
}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i,p in enumerate(my_posts):
         if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message":"Hello World"}


@app.get("/getAllThePosts")
def posts():
    query='''select * from posts'''
    cursor.execute(query)
    print(query)
    return {"successfully recieved all the posts"}


@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""Insert into posts (title,content,published) values (%s,%s,%s) RETURNING*   """,(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    cursor.execute("""select * from posts where id =%s""",(str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return {"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    cursor.execute("""delete from posts where id =%s  RETURNING*  """,(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""update posts set title=%s,content=%s,published=%s where id=%s returning * """,(post.title,post.content,post.published,str(id),))
    updated_post= cursor.fetchone()
    conn.commit()
    if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
   
    return {"data":updated_post}
   
   
