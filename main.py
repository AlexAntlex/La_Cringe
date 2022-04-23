import datetime
import os
import random

from flask_login import AnonymousUserMixin
from flask import render_template, Flask, request, flash, g, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort
from werkzeug.utils import redirect, secure_filename

from config import Config
from data import db_session
from data.user_posts import PostUser
from data.users import User
from form.login import LoginForm
from form.post import PostForm
from form.register import RegisterForm
from form.delete import DeleteForm
from form.edit import ChangeIngoForm

app = Flask(__name__)
app.config.from_object(Config)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.id = '0'


login_manager = LoginManager()
login_manager.anonymous_user = Anonymous
login_manager.init_app(app)


#  Upload files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def main():
    db_session.global_init("db/users.sqlite")
    app.run()


@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=['GET', 'POST'])
def index():
    session = db_session.create_session()
    my = g.user.id
    posts = session.query(PostUser).filter(PostUser.autor_id != my).order_by(PostUser.id.desc())
    return render_template('start_page.html', posts=posts)
    return render_template('start_page.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            avatar=url_for('static', filename='img/file.png')
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()
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


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('delete.html', title='Deletion',
                                   form=form,
                                   message="Пароли не совпадают")
        else:
            session = db_session.create_session()
            my = g.user.id
            user = session.query(User).filter(User.id == my).first()
            if user.check_password(form.password.data):
                session.delete(user)
                session.commit()
                return redirect('/register')
    return render_template('delete.html', title='Deletion', form=form)


@app.route('/user/<id>', methods=['GET', 'POST'])  # загрузка профиля пользователя
def user_profile(id):
    session = db_session.create_session()
    user = session.query(User).filter_by(id=id).first()
    form = PostForm()
    if user == None:
        flash('User ' + id + ' not found.')
        return render_template('login.html')
    else:
        you = user.name
        my = g.user.id
        info = user.about
        user_id = int(id)
        if my == user_id:
            if form.validate_on_submit():
                file = form.file_url.data
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename) + "/" + user_id
                    way_to_file = os.path.join(app.config['UPLOAD_FOLDER_USER'], filename)
                    file.save(way_to_file)
                    post = PostUser(
                                    date=datetime.datetime.now().strftime("%A %d %b %Y (%H:%M)"),
                                    autor_id=my,
                                    file=way_to_file)
                    session.add(post)
                    session.commit()
                    return redirect(f'{id}')
            posts = session.query(PostUser).filter_by(autor_id=user_id).order_by(PostUser.id.desc())
            return render_template('profile_user.html', title=you, you=you, user_id=user_id, my_id=my, info=info,
                                   form=form, posts=posts, avatar=user.avatar, id=id)
        else:
            posts = session.query(PostUser).filter_by(autor_id=user_id).order_by(PostUser.id.desc())
            return render_template('profile_user.html', title=you, you=you, user_id=user_id, my_id=my, info=info,
                                   form=form, posts=posts, avatar=user.avatar, id=id)


@app.route('/post_delete/<int:id>', methods=['GET', 'POST'])  # удаление поста из бд
@login_required
def post_delete(id):
    session = db_session.create_session()
    posts = session.query(PostUser).filter(PostUser.id == id,
                                           PostUser.autor_id == g.user.id).first()
    if posts:
        session.delete(posts)
        session.commit()
    else:
        abort(404)
    return redirect(f'/user/{g.user.id}')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = ChangeIngoForm()
    user_id = g.user.id
    if request.method == "GET":
        session = db_session.create_session()
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            form.name.data = user.name
            form.info.data = user.about
            form.avatar.data = user.avatar
        else:
            os.abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter_by(id=int(user_id)).first()
        if user:
            way_to_file = user.avatar
            file = form.avatar.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                way_to_file = os.path.join(app.config['UPLOAD_FOLDER_USER'], filename)
                file.save(way_to_file)
            user.name = form.name.data
            user.about = form.info.data
            user.avatar = way_to_file
            session.commit()
            return redirect(f'/user/{user_id}')
        else:
            os.abort(404)
    num = random.randint(1, 35)
    name = "img/edit/edit" + str(num) + ".jpg"
    return render_template('edit.html', info=user.about, name=user.name, form=form, im_user=1, pic=name)


if __name__ == '__main__':
    app.debug = True
    main()
