import flask
from flask import jsonify, request
from . import db_session
from .users import User

bp = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@bp.route('/api/users')
def get_users():
    sess = db_session.create_session()
    users = sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from')) for item in
                 users]
        }
    )


@bp.route('/api/users/<int:user_id>')
def get_user(user_id):
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from'))
        }
    )


@bp.route('/api/users', methods=['POST'])
def add_user():
    req = request.json
    if not req:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    sess = db_session.create_session()
    user = User(
        surname=req['surname'],
        name=req['name'],
        age=req['age'],
        position=req['position'],
        speciality=req['speciality'],
        address=req['address'],
        email=req['email'],
        city_from=req['city from']
    )
    sess.add(user)
    sess.commit()
    return jsonify({'success': 'OK'})


@bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    sess.delete(user)
    sess.commit()
    return jsonify({'success': 'OK'})


@bp.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    req = request.json
    if not req:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'city_from']):
        return jsonify({'error': 'Bad request'})
    user.surname = req['surname']
    user.name = req['name']
    user.age = req['age']
    user.position = req['position']
    user.speciality = req['speciality']
    user.address = req['address']
    user.email = req['email']
    user.city_from = req['city_from']
    sess.commit()
    return jsonify({'success': 'OK'})
