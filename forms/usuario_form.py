from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistroForm(FlaskForm):
    usuario = StringField('Usuario', validators=[
        DataRequired(message="El nombre de usuario es obligatorio."),
        Length(min=3, max=50, message="El usuario debe tener entre 3 y 50 caracteres.")
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio."),
        Email(message="Ingresa un correo electrónico válido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message="Debes confirmar tu contraseña."),
        EqualTo('password', message="Las contraseñas no coinciden.")
    ])
    submit = SubmitField('Registrarse')