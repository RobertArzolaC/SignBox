import os
import uuid

from flask import (
    Blueprint, render_template, flash, request, abort,
    session, send_file, current_app, Response
)
from flask_login import login_required, current_user
from src.models import Certificate

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


@main.route("/add-certificate", methods=["POST"])
@login_required
def add_certificate():
    data = request.json
    certificate = Certificate(
        user_id=current_user.id,
        certificate_id=data["certificateId"],
        certificate_password=data["certificatePassword"],
    )
    certificate.save()
    return Response({"message": "Creating Success."}, 201)


@main.route("/delete-certificate", methods=["GET"])
@login_required
def delete_certificate():
    certificate = Certificate.query.filter_by(
        user_id=current_user.id, is_active=True,
    ).first()
    certificate.is_active = False
    certificate.save()
    return Response({"message": "Deleting Success."}, 200)


@main.route("/add-pin", methods=["POST"])
@login_required
def add_pin():
    data = request.json
    session["pin"] = data["pin"]
    return Response({"message": "Creating Success."}, 201)


@main.route("/add-files", methods=["GET", "POST"])
@login_required
def add_files():
    if request.method == 'POST':
        templates = []
        data = request.json
        use_first_template = data.get("useFirstTemplate", None)
        use_second_template = data.get("useSecondTemplate", None)

        if use_first_template:
            templates.append(os.getenv("FIRST_TEMPLATE"))

        if use_second_template:
            templates.append(os.getenv("SECOND_TEMPLATE"))

        if templates:
            certificate = Certificate.query.filter_by(
                user_id=current_user.id, is_active=True,
            ).first()
            service = SignBox(
                certificate.certificate_id,
                certificate.certificate_password,
                session["pin"]
            )
            for template in templates:
                service.upload_file(template)

    certificate = Certificate.query.filter_by(
        user_id=current_user.id, is_active=True
    ).first()

    return render_template("add-files.html", certificate=certificate)
