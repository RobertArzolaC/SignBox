from flask_wtf import FlaskForm
from wtforms import (
    SubmitField, FileField, StringField, PasswordField, BooleanField
)
from flask_wtf.file import (
    DataRequired, FileField, FileRequired, FileAllowed
)


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class CertificateForm(FlaskForm):
    pin = PasswordField(
        'Pin', validators=[DataRequired()]
    )
    certificate_id = StringField(
        'ID Certificado', validators=[DataRequired()]
    )
    certificate_password = PasswordField(
        'Contraseña de Certificado', validators=[DataRequired()]
    )
    submit = SubmitField('Agregar')


class AddFilesForm(FlaskForm):
    use_first_file = BooleanField('Usar primer archivo.')
    use_second_file = BooleanField('Usar segundo archivo.')
    use_third_file = BooleanField('Usar tercer archivo.')
    upload_file = FileField(
        'Ingrese su documento: ', 
        validators=[
            FileRequired(),
            FileAllowed(["pdf"], "Solo se aceptan archivos PDF")
        ]
    )
    pin = PasswordField('PIN: ', validators=[DataRequired()])
    submit = SubmitField('Subir Archivos')
