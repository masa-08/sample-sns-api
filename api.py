#!/user/bin/env python
# -*- coding:utf8 -*-

from flask import Flask, jsonify, request, url_for, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Diary

app = Flask(__name__)
engine = create_engine('sqlite:///sample.db', echo=False)


###################
# APIs about user #
###################

# TODO: exceptの条件を正しくする

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        users = session.query(User).all()
    except User.DoesNotExist:
        abort(404)

    return _make_response([user.serialize for user in users], 200)


@app.route("/api/v1/users/<user_id>", methods=["GET"])
def get_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
    except User.DoesNotExist:
        abort(404)

    return _make_response(user.serialize, 200)

# GET
# * ユーザ名に一致するユーザの情報を取得
#     * http://sample.com/api/v1/users?user_name={ユーザ名}
# PUSH
# * あるユーザの情報を登録
#     * http://sample.com/api/v1/users
# PUT
# * user_idに一致するユーザのパラメータを変更する（ユーザ名、メールアドレス、パスワード、プロフィール画像のパスを変更許可）
#     * http://sample.com/api/v1/users/{user_id}
# DELETE
# * user_idに一致するユーザを削除
#     * http://sample.com/api/v1/users/{user_id}


####################
# APIs about diary #
####################

@app.route("/api/v1/diaries", methods=["GET"])
def get_diaries():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diaries = session.query(Diary).all()
    except Diary.DoesNotExist:
        abort(404)

    return _make_response([diary.serialize for diary in diaries], 200)


@app.route("/api/v1/diaries/<diary_id>", methods=["GET"])
def get_diary(diary_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diary = session.query(Diary).filter(Diary.diary_id == diary_id).one()
    except Diary.DoesNotExist:
        abort(404)

    return _make_response(diary.serialize, 200)


@app.route("/api/v1/users/<user_id>/diaries", methods=["GET"])
def get_tweets_by_user_id(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diaries = session.query(User)\
                         .filter(User.user_id == user_id)\
                         .one()\
                         .diaries
    except User.DoesNotExist:
        abort(404)

    return _make_response([diary.serialize for diary in diaries], 200)

# PUSH
# * あるユーザのツイートを登録
#     * http://sample.com/api/v1/users/{user_id}/tweets
# PUT
# * tweet_idに一致する投稿のパラメータを変更する（本文のみ変更許可？）
#     * http://sample.com/api/v1/tweets/{tweet_id}
# DELETE
# * tweet_idに一致する投稿を削除
#     * http://sample.com/api/v1/tweets/{tweet_id}


##############################
# APIs about friend/follower #
##############################

@app.route("/api/v1/users/<user_id>/friends", methods=["GET"])
def get_friends(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        friends = session.query(User)\
                         .filter(User.user_id == user_id)\
                         .one()\
                         .serialize["friends"]
    except User.DoesNotExist:
        abort(404)

    return _make_response(friends, 200)


@app.route("/api/v1/users/<user_id>/followers", methods=["GET"])
def get_followers(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        followers = session.query(User)\
                           .filter(User.user_id == user_id)\
                           .one()\
                           .serialize["followers"]
    except User.DoesNotExist:
        abort(404)

    return _make_response(followers, 200)


# Used in each api method

def _make_response(data, status_code):
    response = jsonify(data)
    response.status_code = status_code
    return response


if __name__ == "__main__":
    app.run()
