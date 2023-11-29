from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


class UserModel(SQLModel):
    username: str
    email: EmailStr
    password: str
    name: str


class UserFollowerLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    follower_id: Optional[int] = Field(default=None, foreign_key="followers.id", primary_key=True)

class User(UserModel, table=True):  # Um aus dem Model auch eine Table zu stellen brauchen wir das Attribut table = true
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    posts: list["Post"] = Relationship(back_populates="author")  # Liste an posts von einem User muss über Relationship verknüpft werden. author ist ein VerknüpfungsOject, das muss hier angeben werden
    likes: list["Like"] = Relationship(back_populates="user")
    followers: list["Follower"] = Relationship(back_populates="followed_user", link_model=UserFollowerLink)


class PostModel(SQLModel):
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class Post(PostModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")  # foreignKey muss über diese Schreibweise verknüpft werden. hierzu wird der Tabelennamen aus dem Model genommen mit dem Attribut
    author: Optional[User] = Relationship(back_populates="posts")  # es wird ein Verknüpfungsobject benötigt. Hier muss das Attribut aus dem verknüpften Model angegeben werden. Hier die posts liste
    likes: list["Like"] = Relationship(back_populates="post")


class LikeModel(SQLModel):
    post_id: Optional[int] = Field(default=None, foreign_key="posts.id")


class Like(LikeModel, table=True):
    __tablename__ = "likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    user: Optional[User] = Relationship(back_populates="likes")
    post: Optional[Post] = Relationship(back_populates="likes")

class FollowerModel(SQLModel):
    follower_id: int

class Follower(FollowerModel, table=True):
    __tablename__ = "followers"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int

    followed_user: list[User] = Relationship(back_populates="followers", link_model=UserFollowerLink)


