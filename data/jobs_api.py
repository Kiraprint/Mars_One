# В пост запросе id не обрабатывается и так, у него есть автоинкремент


import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs
from .users import User

bp = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@bp.route('/api/jobs')
def get_jobs():
    sess = db_session.create_session()
    jobs = sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators')) for item in jobs]
        }
    )


@bp.route('/api/jobs/<int:job_id>')
def get_job(job_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators'))
        }
    )


@bp.route('/api/jobs', methods=['POST'])
def add_job():
    req = request.json
    if not req:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req for key in ['job', 'team_leader', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    sess = db_session.create_session()
    job = Jobs(
        job=req['job'],
        team_leader=req['team_leader'],
        collaborators=req['collaborators'],
        work_size=req['work_size']
    )
    for i in map(int, req['collaborators'].split(', ')):
        user = sess.query(User).filter(User.id == i).first()
        user.jobs.append(job)
    sess.add(job)
    sess.commit()
    return jsonify({'success': 'OK'})


@bp.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    sess.delete(job)
    sess.commit()
    return jsonify({'success': 'OK'})


@bp.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    req = request.json
    if not req:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req for key in ['job', 'team_leader', 'work_size', 'collaborators']):
        return jsonify({'error': 'Bad request'})
    job.job = req['job']
    job.team_leader = req['team_leader']
    job.work_size = req['work_size']
    job.collaborators = req['collaborators']
    for i in map(int, job.collaborators.split(', ')):
        user = sess.query(User).filter(User.id == i).first()
        if job not in user.jobs:
            user.jobs.append(job)
    sess.commit()
    return jsonify({'success': 'OK'})
