from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.class_validators import Optional
from random import randrange
import utils


app = FastAPI()


# for prod end RUN IN COMMEND LINE: uvicorn Server:app
# for dev env RUN IN COMMEND LINE: uvicorn Server:app --reload

# some kind of contract with frontEnd, what we expect to get from the post request
class Post(BaseModel):
    title: str
    content: str
    # default value
    published: bool = True
    # optional field
    rating: Optional[int] = None


class User(BaseModel):
    user_name: str
    password: str


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

users = [{"user_name": "user1", "password": "12345"}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# title str, content str

# dont forget - path parameter always comes as string, dont forget to cast it if needed, fastAPI can convert it with
# typing


@app.get("/posts/{id}")
def get_post(id: int):
    # print(type(id))
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    index = my_posts.index(post)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    find = find_post(id)
    if not find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    index = my_posts.index(find)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_dict = user.dict()
    user_dict['id'] = randrange(0, 10000000)
    users.append(user_dict)
    return {"data": user_dict}


@app.get("/users")
def get_posts():
    return {"data": users}
