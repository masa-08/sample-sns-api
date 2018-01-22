#!/user/bin/env python
# -*- coding:utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import User, Diary

Base = declarative_base()
engine = create_engine('sqlite:///sample.db', echo=False)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(user_id="aaa111@", user_name="ユーザ1", name="山田一郎",
             email="aaa111@sample.com", password="aaa111")

user2 = User(user_id="bbb222@", user_name="ユーザ2", name="山田二郎",
             email="bbb222@sample.com", password="bbb222")

user3 = User(user_id="ccc333@", user_name="ユーザ3", name="山田三郎",
             email="ccc333@sample.com", password="ccc333")

diary1 = Diary(diary_id="a1", user_id="aaa111@", body="山田一郎です")
diary2 = Diary(diary_id="b1", user_id="bbb222@", body="山田二郎です")
diary3 = Diary(diary_id="c1", user_id="ccc333@", body="山田三郎です")
diary4 = Diary(diary_id="a2", user_id="aaa111@", body="山田一郎二回目")
diary5 = Diary(diary_id="a3", user_id="aaa111@", body="山田一郎三回目")


def print_all_users(session):
    users = session.query(User).all()

    for user in users:
        print("%d | %s %s %s %s %s %s" % (user.id, user.user_id,
              user.user_name, user.name, user.email, user.password,
              [x.diary_id for x in user.diaries]))


def print_all_diaries(session):
    diaries = session.query(Diary).all()

    for diary in diaries:
        print("%d | %s %s %s" % (diary.id, diary.diary_id, diary.user_id,
              diary.body))


def print_all_friends_followers(session):
    users = session.query(User).all()

    for user in users:
        print("%s | following: %s, followers: %s" % (user.user_name,
              [x.user_name for x in user.friends],
              [x.user_name for x in user.followers]))


if __name__ == "__main__":

    for user in session.query(User):
        session.delete(user)
    session.commit()

    user1.diaries = [diary1, diary4, diary5]
    user2.diaries = [diary2]
    user3.diaries = [diary3]

    user1.followers = [user2, user3]
    user2.followers = [user1]
    user3.followers = [user2]

    session.add_all([user1, user2, user3])
    session.commit()

    print_all_users(session)
    print_all_diaries(session)
    print_all_friends_followers(session)
