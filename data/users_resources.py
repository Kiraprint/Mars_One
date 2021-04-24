from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.users import User


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        users = sess.query(User).all()
        return jsonify({'users': [user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')
        ) for user in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        sess = db_session.create_session()
        users = sess.query(User).get(user_id)
        return jsonify({'user': users.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')
        )})

    def put(self, user_id):
        args = parser.parse_args()
        abort_if_users_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.city_from = args['city_from']
        sess.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('city_from', required=True)