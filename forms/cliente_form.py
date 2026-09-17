from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message="El Nombre Es Obligatorio."),
        Length(min=3, max=100, message="El Nombre Debe Tener Entre 3 Y 100 Caracteres.")
    ], render_kw={"placeholder": "Ej. María López"})

    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El Correo Es Obligatorio."),
        Email(message="Ingrese Un Correo Electrónico Válido (Ej. correo@dominio.com).")
    ], render_kw={"placeholder": "Ej. cliente@correo.com"})

    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El Teléfono Es Obligatorio."),
        Length(min=7, max=15, message="Ingrese Un Número De Teléfono Válido.")
    ], render_kw={"placeholder": "Ej. 0991234567"})

    estado = SelectField('Estado', choices=[
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo')
    ], validators=[DataRequired(message="Seleccione Un Estado.")])

    submit = SubmitField('Guardar Cliente')