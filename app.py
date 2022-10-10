import os
import uuid

from flask_bootstrap import Bootstrap
from flask import (
    Flask, render_template, flash, request, abort,
    redirect, url_for, session, send_from_directory,
    send_file
)

from constants import DEFAULT_USERS, UPLOAD_FOLDER
from forms import AddFilesForm, CertificateForm, LoginForm
from services import SignBox
from utils import login_required


app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')


@app.route('/signed-files', defaults={'req_path': ''})
@app.route('/signed-files/<path:req_path>')
@login_required
def dir_listing(req_path):
    abs_path = os.path.join(app.config['UPLOAD_FOLDER'], req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = os.listdir(abs_path)
    return render_template('signed-files.html', files=files)


@app.route("/url-out", methods=["POST"])
def url_out():
    data = request.data
    filename = f"{app.config['UPLOAD_FOLDER']}/{str(uuid.uuid4())}.pdf"

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with open(filename, 'wb') as f:
        f.write(data)

    return "OK"


@app.route("/url-back", methods=["POST"])
def url_back():
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
        service.upload_file(upload_data)
        flash('La carga de su archivo se realizó con exito!.  ')

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
