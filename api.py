#!/user/bin/env python
# -*- coding:utf8 -*-

from flask import Flask, jsonify, request, abort, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Diary

app = Flask(__name__)
engine = create_engine('sqlite:///sample.db', echo=False)


###################
# APIs about user #
###################

# TODO: exceptの条件を正しくする

@app.route("/api/v1/users/list", methods=["GET"])
def get_users():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        users = session.query(User).all()
    except User.DoesNotExist:
        abort(404)

    return make_response(jsonify([user.serialize for user in users]))


@app.route("/api/v1/users/<user_id>", methods=["GET"])
def get_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
    except User.DoesNotExist:
        abort(404)

    return make_response(jsonify(user.serialize))


@app.route("/api/v1/users", methods=["GET"])
def get_user_by_user_name():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user_name = request.args.get("user_name")
        user = session.query(User).filter(User.user_name == user_name).one()
    except User.DoesNotExist:
        abort(404)

    return make_response(jsonify(user.serialize))


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    Session = sessionmaker(bind=engine)
    session = Session()

    json = request.json
    user = User(user_id=json["user_id"], user_name=json["user_name"],
                name=json["name"], email=json["email"],
                password=json["password"])

    try:
        session.add(user)
        session.commit()
    except User.DoesNotExist:
        abort(400)

    return make_response("", 201)


@app.route("/api/v1/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    json = request.json

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
        user.user_name = json["user_name"]
        user.name = json["name"]
        user.email = json["email"]
        user.password = json["password"]
        user.image = json["image"]

        session.commit()
    except User.DoesNotExist:
        abort(400)

    return make_response("", 204)


@app.route("/api/v1/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).one()

        session.delete(user)
        session.commit()
    except User.DoesNotExist:
        abort(400)

    return make_response("", 204)


####################
# APIs about diary #
####################

@app.route("/api/v1/diaries/list", methods=["GET"])
def get_diaries():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diaries = session.query(Diary).all()
    except Diary.DoesNotExist:
        abort(404)

    return make_response(jsonify([diary.serialize for diary in diaries]))


@app.route("/api/v1/diaries/<diary_id>", methods=["GET"])
def get_diary(diary_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diary = session.query(Diary).filter(Diary.diary_id == diary_id).one()
    except Diary.DoesNotExist:
        abort(404)

    return make_response(jsonify(diary.serialize))


@app.route("/api/v1/users/<user_id>/diaries/list", methods=["GET"])
def get_diaries_by_user_id(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diaries = session.query(User)\
                         .filter(User.user_id == user_id)\
                         .one()\
                         .diaries
    except User.DoesNotExist:
        abort(404)

    return make_response(jsonify([diary.serialize for diary in diaries]))


@app.route("/api/v1/diaries", methods=["POST"])
def create_diary():
    Session = sessionmaker(bind=engine)
    session = Session()

    json = request.json
    diary = Diary(diary_id=json["diary_id"], user_id=json["user_id"],
                  body=json["body"])
    try:
        session.add(diary)
        session.commit()
    except User.DoesNotExist:
        abort(400)

    return make_response("", 201)


@app.route("/api/v1/diaries/<diary_id>", methods=["PUT"])
def update_diary(diary_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    json = request.json

    try:
        diary = session.query(Diary).filter(Diary.diary_id == diary_id).one()
        diary.body = json["body"]

        session.commit()
    except User.DoesNotExist:
        abort(400)

    return make_response("", 204)


@app.route("/api/v1/diaries/<diary_id>", methods=["DELETE"])
def delete_diary(diary_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        diary = session.query(Diary).filter(Diary.diary_id == diary_id).one()

        session.delete(diary)
        session.commit()
    except Diary.DoesNotExist:
        abort(400)

    return make_response("", 204)


##############################
# APIs about friend/follower #
##############################

@app.route("/api/v1/users/<user_id>/friends/list", methods=["GET"])
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

    return make_response(jsonify(friends))


@app.route("/api/v1/users/<user_id>/friends", methods=["POST"])
def add_friend(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    friend_id = request.json["friend_id"]

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
        friend = session.query(User).filter(User.user_id == friend_id).one()

        if(friend.user_id not in [f.user_id for f in user.friends]):
            user.friends.append(friend)
            session.commit()
    except User.DoesNotExist:
        abort(404)

    return make_response("", 201)


@app.route("/api/v1/users/<user_id>/friends/<friend_id>", methods=["DELETE"])
def delete_friend(user_id, friend_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
        friend = session.query(User).filter(User.user_id == friend_id).one()

        if(friend.user_id in [f.user_id for f in user.friends]):
            user.friends.remove(friend)
            session.commit()
    except User.DoesNotExist:
        abort(404)

    return make_response("", 201)


@app.route("/api/v1/users/<user_id>/followers/list", methods=["GET"])
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

    return make_response(jsonify(followers))


@app.route("/api/v1/users/<user_id>/followers", methods=["POST"])
def add_follower(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    follower_id = request.json["follower_id"]

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
        follower = session.query(User)\
                          .filter(User.user_id == follower_id)\
                          .one()

        if(follower.user_id not in [f.user_id for f in user.followers]):
            user.followers.append(follower)
            session.commit()
    except User.DoesNotExist:
        abort(404)

    return make_response("", 201)


@app.route("/api/v1/users/<user_id>/followers/<follower_id>",
           methods=["DELETE"])
def delete_follower(user_id, follower_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).one()
        follower = session.query(User)\
                          .filter(User.user_id == follower_id)\
                          .one()

        if(follower.user_id in [f.user_id for f in user.followers]):
            user.followers.remove(follower)
            session.commit()
    except User.DoesNotExist:
        abort(404)

    return make_response("", 201)


if __name__ == "__main__":
    app.run()
