import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_restful import abort, Api
from data.departaments import Department
from forms.department import AddDepartmentForm
from forms.job import AddJobForm
from forms.login import LoginForm
from forms.user import RegisterForm
from data import db_session, jobs_api, user_api, users_resources, jobs_resources
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
api = Api(app)
db_session.global_init('db/mars_explorer.db')
app.register_blueprint(jobs_api.bp)
app.register_blueprint(user_api.bp)
api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:job_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('journal.html', jobs=jobs, session=session, User=User)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Not allowed'}), 405)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=["GET", "POST"])
@login_required
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_lead.data,
            job=form.title.data,
            work_size=form.size.data,
            collaborators=form.collaborators.data,
            is_finished=form.finished.data
        )
        for i in map(int, job.collaborators.split(', ')):
            user = sess.query(User).filter(User.id == i).first()
            user.jobs.append(job)
        sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form, title='Adding a Job')


@app.route('/<int:id>', methods=["GET", "POST"])
def edit_jobs(id):
    form = AddJobForm()
    sess = db_session.create_session()
    if current_user != sess.query(User).filter(User.id == 1).first():
        job = sess.query(Jobs).filter(Jobs.id == id, (current_user == Jobs.creator)).first()
    else:
        job = sess.query(Jobs).filter(Jobs.id == id).first()
    if request.method == "GET":
        if job:
            form.title.data = job.job
            form.team_lead.data = job.team_leader
            form.size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        if job:
            job.team_leader = form.team_lead.data
            job.job = form.title.data
            job.work_size = form.size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.finished.data
            for i in map(int, job.collaborators.split(', ')):
                user = sess.query(User).filter(User.id == i).first()
                if job not in user.jobs:
                    user.jobs.append(job)
            sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template("add_job.html", title="Editing a job", form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    sess = db_session.create_session()
    if current_user != sess.query(User).filter(User.id == 1).first():
        job = sess.query(Jobs).filter(Jobs.id == id, (current_user == Jobs.creator)).first()
    else:
        job = sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        sess.delete(job)
        for user in sess.query(User).all():
            if job in user.jobs:
                user.jobs.remove(job)
        sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    department = session.query(Department).all()
    return render_template('departments.html', departments=department, session=session, User=User)


@app.route('/adddep', methods=["GET", "POST"])
@login_required
def adddep():
    form = AddDepartmentForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
        )
        for i in map(int, dep.members.split(', ')):
            user = sess.query(User).filter(User.id == i).first()
            user.departments.append(dep)
        sess.commit()
        return redirect('/')
    return render_template('add_department.html', form=form, title='Adding a Department')


@app.route('/departments/<int:id>', methods=["GET", "POST"])
def edit_departments(id):
    form = AddDepartmentForm()
    sess = db_session.create_session()
    if current_user != sess.query(User).filter(User.id == 1).first():
        dep = sess.query(Department).filter(Department.id == id, (current_user == Department.creator)).first()
    else:
        dep = sess.query(Department).filter(Department.id == id).first()
    if request.method == "GET":
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        if dep:
            dep.chief = form.chief.data
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            for i in map(int, dep.members.split(', ')):
                user = sess.query(User).filter(User.id == i).first()
                if dep not in user.departments:
                    user.departments.append(dep)
            sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template("add_department.html", title="Editing a Department", form=form)


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def departments_delete(id):
    sess = db_session.create_session()
    if current_user != sess.query(User).filter(User.id == 1).first():
        dep = sess.query(Department).filter(Department.id == id, (current_user == Department.creator)).first()
    else:
        dep = sess.query(Department).filter(Department.id == id).first()
    if dep:
        sess.delete(dep)
        for user in sess.query(User).all():
            if dep in user.departments:
                user.jobs.remove(dep)
        sess.commit()
    else:
        abort(404)
    return redirect('/departments')


def db_work():
    session = db_session.create_session()
    session.commit()


def main():
    db_work()
    app.run()


if __name__ == '__main__':
    main()
