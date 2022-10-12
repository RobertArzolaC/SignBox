import os
import uuid

from flask import (
    Blueprint, render_template, flash, request, abort,
    redirect, url_for, session, send_file, current_app
)
from flask_login import login_required, current_user

from src.forms import AddFilesForm, CertificateForm
from src.services import SignBox


main = Blueprint('main', __name__)
UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']


@main.route('/signed-files', defaults={'req_path': ''})
@main.route('/signed-files/<path:req_path>')
@login_required
def dir_listing(req_path):
    abs_path = os.path.join(UPLOAD_FOLDER, req_path)

    if not os.path.exists(abs_path):
        return abort(404)

    if os.path.isfile(abs_path):
        return send_file(abs_path)

    files = os.listdir(abs_path)
    return render_template('signed-files.html', files=files)


@main.route("/url-out", methods=["POST"])
def url_out():
    data = request.data
    filename = f"{UPLOAD_FOLDER}/{str(uuid.uuid4())}.pdf"

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with open(filename, 'wb') as f:
        f.write(data)

    return "OK"


@main.route("/url-back", methods=["POST"])
def url_back():
    return "OK"


@main.route("/add-certificate", methods=["GET", "POST"])
@login_required
def add_certificate():
    if "certificate_id" in session:
        return redirect(url_for("main.add_files"))

    form = CertificateForm()
    if form.validate_on_submit():
        session["certificate_id"] = form.certificate_id.data
        session["certificate_password"] = form.certificate_password.data
        return redirect(url_for("main.add_files"))

    return render_template("add-certificate.html", form=form, current_user=current_user)


@main.route("/add-files", methods=["GET", "POST"])
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
