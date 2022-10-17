from flask import Blueprint, session, redirect, url_for, render_template
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash

from src.forms import LoginForm
from src.models import User


auth = Blueprint('auth', __name__)


@auth.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.add_files"))

    error = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("main.add_files"))
        error = "Usuario o contraseña incorrectos"
    return render_template("index.html", form=form, error=error)


@auth.route("/logout")
@login_required
def logout():
    session.pop("pin", None)
    logout_user()
    return "ok"
