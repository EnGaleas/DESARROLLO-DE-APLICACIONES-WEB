from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FacturacionForm(FlaskForm):
    numero = StringField('Número De Factura', validators=[
        DataRequired(message="El Número De Factura Es Obligatorio.")
    ], render_kw={"placeholder": "Ej. FAC-001"})

    cliente = StringField('Nombre Del Cliente', validators=[
        DataRequired(message="El Nombre Del Cliente Es Obligatorio.")
    ], render_kw={"placeholder": "Ej. María López"})

    fecha = StringField('Fecha (AAAA-MM-DD)', validators=[
        DataRequired(message="La Fecha Es Obligatoria.")
    ], render_kw={"placeholder": "Ej. 2026-09-17"})

    total = FloatField('Total ($)', validators=[
        DataRequired(message="El Total Es Obligatorio."),
        NumberRange(min=0.01, message="El Total Debe Ser Mayor A 0.")
    ], render_kw={"placeholder": "Ej. 25.50"})

    estado = SelectField('Estado De Pago', choices=[
        ('Pagado', 'Pagado'),
        ('Pendiente', 'Pendiente')
    ], validators=[DataRequired(message="Seleccione Un Estado De Pago.")])

    submit = SubmitField('Guardar Factura')