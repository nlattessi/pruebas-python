from flask import render_template, flash, redirect, url_for
from . import main
from .forms import RegistroForm
from .. import db
from ..models import Registro

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/agregar', methods=['GET', 'POST'])
def agregar():
    form = RegistroForm()
    if form.validate_on_submit():
        registro = Registro(usuario=form.usuario.data, password=form.password.data, descripcion=form.descripcion.data)
        db.session.add(registro)
        flash("Se agrego un nuevo registro a la base.")
        return redirect(url_for('main.index'))
    return render_template('agregar.html', form=form)

