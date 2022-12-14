import os
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import shutil
from conf.forms import *
from conf.definitions import *
from conf.database import User
from conf.mail import *

#region Config
app = Flask(__name__)
app.config['SECRET_KEY'] = get_key('data/app.key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///data/database/database.db"
app.config['UPLOAD_FOLDER'] = "data/temp"
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LeV5AAjAAAAACODekyZL6OdKTPa7ggejdMny-tR"
app.config['RECAPTCHA_PRIVATE_KEY'] = get_key('data/recaptcha.key')
# https://www.google.com/recaptcha/about/
# https://myaccount.google.com/u/2/apppasswords

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#endregion

#region Pages
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/articles/")
def articles():
    article_list = []
    with open(r'data/database/articles.db', 'r') as f:
        for line in f:
            x = line[:-1]
            article_list.append(x)

    return render_template("articles.html", list=article_list)

@app.route("/<title>/")
def read_article(title):
    list = []
    file = open(f'data/articles/{title}.txt', 'r')
    count = 0
    header = ""

    for line in file:
        count += 1
        list.append(line.strip())

    return render_template("read_article.html", title=title, list=list, header=header)

@app.route("/blog/")
def blog():
    #return render_template("blog.html")
    return render_template("comingsoon.html")

@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    user_email = current_user.email
    email_list = []
    form = AccountForm()
    is_signed_up = True

    with open(r'data/database/newsletter.db', 'r') as f:
        for line in f:
            x = line[:-1]
            email_list.append(x)

    if user_email in email_list:
        is_signed_up = True
    else:
        is_signed_up = False

    if form.validate_on_submit():
        newsletter(form, current_user, is_signed_up)
        if is_signed_up == True:
            return render_template("account.html", form=form, name=current_user.username, email=current_user.email, is_signed_up=False)
        elif is_signed_up == False:
            return render_template("account.html", form=form, name=current_user.username, email=current_user.email, is_signed_up=True)
        
    return render_template("account.html", form=form, name=current_user.username, email=current_user.email, is_signed_up=is_signed_up)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('account'))

        return render_template("login.html", form=form, wrong_login=True)

    return render_template("login.html", form=form, wrong_login=False)

@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        log(f"a new user \"{form.username.data}\" has signed up")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/admin/")
@login_required
def admin():
    id = current_user.username
    f = open("data/database/admin.db")
    list = f.read()

    if id in list:
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/upload/", methods=['GET', 'POST'])
@login_required
def admin_upload():
    id = current_user.username
    f = open("data/database/admin.db")
    list = f.read()

    if id in list:
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(path)
            pdf2article(path, form.title.data)
            shutil.copyfile(path, f"data/articles/pdf/{form.title.data}.pdf")
            log(f"a new article \"{form.title.data}\" has been uploaded")

        return render_template("admin_upload.html", form=form)
    else:
        return redirect(url_for("home"))

@app.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                log(f"the user \"{current_user.username}\" has deleted their account")
                db.session.query(User).filter(User.id == current_user.id).delete()
                db.session.commit()
                return redirect(url_for('login'))

        return render_template("delete.html", form=form)

    return render_template("delete.html", form=form)

#endregion

#region Actions
@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("account"))

@app.route("/admin/clearuploads/")
@login_required
def clear_upload():
    id = current_user.username
    f = open("data/database/admin.db")
    list = f.read()

    if id in list:
        clear_folder("data/uploaded_files")
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("home"))

#endregion

if __name__ == "__main__":
    app.run(debug = True)