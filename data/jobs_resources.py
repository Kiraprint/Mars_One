from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs
from data.users import User


def abort_if_jobs_not_found(job_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(job_id)
    if not news:
        abort(404, message=f"Job {job_id} not found")


class JobsListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        jobs = sess.query(Jobs).all()
        return jsonify({'jobs': [job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators')
        ) for job in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            collaborators=args['collaborators'],
            work_size=args['work_size']
        )
        for i in map(int, job.collaborators.split(', ')):
            user = session.query(User).filter(User.id == i).first()
            if job not in user.jobs:
                user.jobs.append(job)
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_jobs_not_found(job_id)
        sess = db_session.create_session()
        jobs = sess.query(Jobs).get(job_id)
        return jsonify({'job': jobs.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators')
        )})

    def put(self, job_id):
        args = parser.parse_args()
        abort_if_jobs_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(job_id)
        job.job = args['job']
        job.team_leader = args['team_leader']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        for i in map(int, job.collaborators.split(', ')):
            user = sess.query(User).filter(User.id == i).first()
            if job not in user.jobs:
                user.jobs.append(job)
        sess.commit()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        abort_if_jobs_not_found(job_id)
        session = db_session.create_session()
        news = session.query(Jobs).get(job_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
