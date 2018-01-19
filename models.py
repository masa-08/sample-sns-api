#!/user/bin/env python
# -*- coding:utf8 -*-

from sqlalchemy import (create_engine, Column, ForeignKey, Integer, String,
                        DATETIME)
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserFriend(Base):
    __tablename__ = "users_friends"
    user_id = Column("user_id", Integer, ForeignKey("users.id"),
                     primary_key=True)
    friend_id = Column("friend_id", Integer, ForeignKey("users.id"),
                       primary_key=True)

    @property
    def serialize(self):
        return {"user_id": self.user_id,
                "friend_id": self.friend_id}


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, nullable=False,
                autoincrement=True)
    user_id = Column("user_id", String(255), nullable=False, unique=True)
    user_name = Column("user_name", String(255), nullable=False)
    name = Column("name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    password = Column("password", String(255), nullable=False)
    image = Column("image", String(255), default="")
    created = Column("created", DATETIME, default=datetime.now, nullable=False)
    modified = Column("modified", DATETIME, default=datetime.now,
                      nullable=False)

    diaries = relation("Diary", order_by="Diary.id", uselist=True,
                       backref="users", cascade="all, delete, delete-orphan")

    friends = relation("User", secondary="users_friends",
                       primaryjoin=id == UserFriend.user_id,
                       secondaryjoin=id == UserFriend.friend_id,
                       backref="followers")

    @property
    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "user_name": self.user_name,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "image": self.image,
                "diaries": [diary.serialize for diary in self.diaries],
                "friends": self._friends(),
                "followers": self._followers()}

    def _friends(self):
        return [{"id": friend.id,
                 "user_id": friend.user_id,
                 "user_name": friend.user_name,
                 "name": friend.name,
                 "email": friend.email,
                 "password": friend.password,
                 "image": friend.image}
                for friend in self.friends]

    def _followers(self):
        return [{"id": follower.id,
                 "user_id": follower.user_id,
                 "user_name": follower.user_name,
                 "name": follower.name,
                 "email": follower.email,
                 "password": follower.password,
                 "image": follower.image}
                for follower in self.followers]


class Diary(Base):
    __tablename__ = "diaries"

    id = Column("id", Integer, primary_key=True, nullable=False,
                autoincrement=True)
    diary_id = Column("diary_id", String(255), nullable=False, unique=True)
    user_id = Column("user_id", String(255), ForeignKey("users.user_id"))
    body = Column("body", String(255), nullable=False)
    created = Column("created", DATETIME, default=datetime.now, nullable=False)
    modified = Column("modified", DATETIME, default=datetime.now,
                      nullable=False)

    @property
    def serialize(self):
        return {"id": self.id,
                "diary_id": self.diary_id,
                "user_id": self.user_id,
                "body": self.body}


if __name__ == "__main__":
    engine = create_engine('sqlite:///sample.db', echo=True)
    Base.metadata.create_all(engine)
