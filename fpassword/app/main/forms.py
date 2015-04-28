from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, TextAreaField, PasswordField
from wtforms.validators import Required, Length

class RegistroForm(Form):
    usuario = StringField("Usuario", validators=[Length(0, 64)])
    password = PasswordField("Password", validators=[Required(), Length(1, 64)])
    descripcion = TextAreaField("Descripcion")
    submit = SubmitField("Agregar")