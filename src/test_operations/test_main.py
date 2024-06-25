from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi_users import FastAPIUsers
from pydantic import BaseModel
from sqlalchemy.orm import Session
from test_operations import models
from auth.base_config import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int


class UserBase(BaseModel):
    username: str
    user_mail: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

#   POST   #

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()
    return {"detail": "Post was successfully deleted"}

@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post_update: PostBase, db: db_dependency):
    db_put = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_put is None:
        raise HTTPException(status_code=404, detail='Post was not found')

    for key, value in post_update.dict().items():
        setattr(db_put, key, value)

    db.commit()
    db.refresh(db_put)
    return db_put


#   USER   #

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.delete(db_user)
    db.commit()
    return {"detail": "Users was successfully deleted"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, db: db_dependency):
    db_put_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_put_user is None:
        raise HTTPException(status_code=404, detail='User was not found')

    for key, value in UserBase.dict().items():
        setattr(db_put_user, key, value)

    db.commit()
    db.refresh(db_put_user)
    return db_put_user