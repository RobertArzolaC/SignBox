import tempfile

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, flash, request

from services import SignBox
from forms import UploadFileForm


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

@app.route("/url-out", methods=["POST"])
def url_out():
    data = request.data
    with tempfile.TemporaryFile() as fp:
        fp.write(data)
    return "OK"


@app.route("/url-back", methods=["POST"])
def url_back():
    data = request.data
    with tempfile.TemporaryFile() as fp:
        fp.write(data)
    return "OK"


@app.route("/", methods=["GET", "POST"])
def upload_file_form():
    form = UploadFileForm()
    if form.validate_on_submit():
        service = SignBox()
        upload_data = form.upload.data
        response = service.upload_file(upload_data)
        if response.ok:
            job_id = response.text.split("=")[1]
            service.load_job(job_id)
            flash('La carga de su archivo se realizó con exito!')
    return render_template("upload_file.html", form=form)
