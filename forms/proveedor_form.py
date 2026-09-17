from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    empresa = StringField('Nombre de la empresa', validators=[
        DataRequired(message="El campo es obligatorio."),
        Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
    ], render_kw={"placeholder": "Ej. Cosméticos S.A."})

    contacto = StringField('Contacto / Correo', validators=[
        DataRequired(message="El campo es obligatorio.")
    ], render_kw={"placeholder": "Ej. contacto@empresa.com"})

    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El campo es obligatorio."),
        Length(min=7, max=15, message="El teléfono debe tener entre 7 y 15 dígitos.")
    ], render_kw={"placeholder": "Ej. 0991234567"})

    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="El campo es obligatorio.")
    ], render_kw={"placeholder": "Ej. Guayaquil"})

    submit = SubmitField('Guardar proveedor')