from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class UploadFileForm(FlaskForm):
    upload = FileField(
        'Ingrese su documento: ', 
        validators=[
            FileRequired(),
            FileAllowed(["pdf"], "Solo se aceptan archivos PDF")
        ]
    )
    submit = SubmitField('SUBIR')
