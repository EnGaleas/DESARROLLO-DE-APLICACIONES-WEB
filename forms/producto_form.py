from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del producto', validators=[
        DataRequired(message="El campo es obligatorio."),
        Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres.")
    ], render_kw={"placeholder": "Ej. Labial Matte Cream"})

    precio = FloatField('Precio ($)', validators=[
        DataRequired(message="El campo es obligatorio."),
        NumberRange(min=0.01, message="El precio ingresado es incorrecto, debe ser mayor a 0.")
    ], render_kw={"placeholder": "Ej. 6.50"})

    stock = IntegerField('Cantidad en stock', validators=[
        DataRequired(message="El campo es obligatorio."),
        NumberRange(min=0, message="El valor ingresado es incorrecto, no puede ser negativo.")
    ], render_kw={"placeholder": "Ej. 12"})

    categoria = SelectField('Categoría', choices=[
        ('Rostro', 'Rostro'),
        ('Ojos y Cejas', 'Ojos y Cejas'),
        ('Labios', 'Labios'),
        ('Accesorios', 'Accesorios'),
        ('Cuidado Facial', 'Cuidado Facial')
    ], validators=[DataRequired(message="Seleccione una opción válida.")])

    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(message="El campo es obligatorio."),
        Length(min=5, max=200, message="La descripción es incorrecta, debe tener entre 5 y 200 caracteres.")
    ], render_kw={"placeholder": "Ej. Brinda color intenso de larga duración..."})

    submit = SubmitField('Guardar producto')