import os
import uuid

from flask_bootstrap import Bootstrap
from flask import (
    Flask, render_template, flash, request,
    redirect, url_for, session
)

from constants import DEFAULT_USERS, UPLOAD_FOLDER
from forms import AddFilesForm, CertificateForm, LoginForm
from services import SignBox
from utils import login_required


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')


@app.route("/url-out", methods=["POST"])
def url_out():
    data = request.data
    filename = f"{app.config['UPLOAD_FOLDER']}/{str(uuid.uuid4())}.txt"
    with open(filename, 'wb') as f:
        f.write(data)
    return "OK"


@app.route("/url-back", methods=["POST"])
def url_back():
    data = request.data
    filename = f"{app.config['UPLOAD_FOLDER']}/{str(uuid.uuid4())}.txt"
    with open(filename, 'wb') as f:
        f.write(data)
    return "OK"


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" in session:
        return redirect(url_for("add_certificate"))

    error = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in DEFAULT_USERS and password == "admin":
            session["username"] = username
            return redirect(url_for("add_certificate"))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template("index.html", form=form, error=error)


@app.route("/add-certificate", methods=["GET", "POST"])
@login_required
def add_certificate():
    if "certificate_id" in session:
        return redirect(url_for("add_files"))

    form = CertificateForm()
    if form.validate_on_submit():
        session["certificate_id"] = form.certificate_id.data
        session["certificate_password"] = form.certificate_password.data
        return redirect(url_for("add_files"))
    return render_template("add-certificate.html", form=form)


@app.route("/add-files", methods=["GET", "POST"])
@login_required
def add_files():
    form = AddFilesForm()
    if form.validate_on_submit():
        upload_data = form.upload_file.data
        pin = form.pin.data

        service = SignBox(
            session["certificate_id"], session["certificate_password"], pin
        )
        response = service.upload_file(upload_data)
        if response.ok:
            job_id = response.text.split("=")[1]
            content_file = service.get_file(job_id)
            filename = f"{app.config['UPLOAD_FOLDER']}/{str(uuid.uuid4())}.pdf"
            with open(filename, 'wb') as fd:
                for chunk in content_file.iter_content(2000):
                    fd.write(chunk)
            flash('La carga de su archivo se realizó con exito!')

    return render_template("add-files.html", form=form)


@app.route("/clean-certificates", methods=["GET"])
@login_required
def clean_certificates():
    session.pop("certificate_id", None)
    session.pop("certificate_password", None)
    return "ok"


@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    session.pop("certificate_id", None)
    session.pop("certificate_password", None)
    return "ok"
