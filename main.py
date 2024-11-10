from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange




app=FastAPI()



class Post(BaseModel):
    title:str
    content:str
    published:bool =True
    rating:Optional[int] =None
    

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


@app.get("/")
def posts():
    return {"message":"Hello posts"}


@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    print(my_posts)
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data":my_posts}

@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    post=find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{'message':f"post with id {id} was not found"}
    
    return {"post_detail":post}


@app.delete("/posts/{id}")
def delete_post():
    index=find_index_post(id)
    print(my_posts)
    if index is None:
            return {"message": "Post not found"}, 404 
    my_posts.pop(index)
    return {'message': 'Post was successfully deleted'}



 