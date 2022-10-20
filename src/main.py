import io

from flask import (
    Blueprint, render_template, request, abort,
    session, send_file, current_app, Response,
    redirect, url_for
)
from flask_login import login_required, current_user
from src.models import Certificate, Document

from src.services import SignBox


main = Blueprint('main', __name__)
UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']


@main.route('/signed-files')
@login_required
def signed_files():
    certificate = Certificate.query.filter_by(
        user_id=current_user.id, is_active=True
    ).first()
    documents = Document.query.filter_by(
        user_id=current_user.id, is_signed=True
    ).all()

    context = {
        'certificate': certificate,
        'documents': documents
    }

    return render_template('signed-files.html', **context)


@main.route('/signed-file/<int:document_id>')
@login_required
def download_signed_file(document_id):
    document = Document.query.filter_by(
        user_id=current_user.id, id=document_id
    ).first()
    if document is None:
        abort(404)
    return send_file(
        io.BytesIO(document.data_signed),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=document.document_name
    )

@main.route('/restore-files')
@login_required
def restore_files():
    templates = Document.query.filter_by(
        user_id=current_user.id
    ).all()
    for template in templates:
        template.is_signed = False
        template.save()

    return redirect(url_for("auth.index"))


@main.route("/result_<filename>", methods=["POST"])
def url_out(filename):
    data = request.data
    document = Document.query.filter(
        Document.document_name.startswith(filename)
    ).first()

    if document:
        document.data_signed = data
        document.is_signed = True
        document.save()
    
    return "ok"

@main.route("/servicelogs", methods=["POST"])
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
    return redirect(url_for("auth.index"))


@main.route("/add-pin", methods=["POST"])
@login_required
def add_pin():
    data = request.json
    session["pin"] = data["pin"]
    return Response({"message": "Creating Success."}, 201)


@main.route("/add-files", methods=["GET", "POST"])
@login_required
def add_files():
    certificate = Certificate.query.filter_by(
        user_id=current_user.id, is_active=True
    ).first()
    templates = Document.query.filter_by(
        user_id=current_user.id
    ).all()

    if request.method == 'POST':
        data = request.json
        pin = data["pin"]
        document_ids = data["documentIds"]
        templates_to_sign = Document.query.filter(
            Document.id.in_(document_ids)
        ).all()

        if templates_to_sign:
            service = SignBox(
                certificate.certificate_id,
                certificate.certificate_password,
                pin
            )

            for template in templates_to_sign:
                service.upload_file(template.url)

    context = {
        "certificate": certificate,
        "templates": templates,
    }

    return render_template("add-files.html", **context)
