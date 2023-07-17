from flask import redirect, render_template, url_for, flash, request, session, current_app, Flask
from shop  import app,db,photos, bcrypt, search, login_manager
from flask_login import login_required,current_user,logout_user,login_user
from .forms import UserRegisterForm, UserLoginForm
from .model import RegistroU
from flask_wtf import FlaskForm
from flask_mail import Mail,Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from .forms import ResetPasswordForm

import secrets
import os

@app.route('/user/registro', methods=['GET','POST'])
def user_registro():
    form = UserRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        registro = RegistroU(nombre=form.nombre.data, 
        username=form.username.data,
        email=form.email.data,
        telefono=form.telefono.data,
        password=hash_password)
        db.session.add(registro)
        flash(f'Bienvenido {form.nombre.data} Gracias por registrarte', 'success')
        db.session.commit()
        return redirect(url_for('userLogin'))
    return render_template('user/registro.html', form=form)


@app.route('/user/login', methods=['GET','POST'])
def userLogin():
    form= UserLoginForm()
    if form.validate_on_submit():
        user=RegistroU.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f' Inició sesion con éxito', 'success')
            next=request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Correo o contraseña incorrectos', 'danger') 
        return redirect(url_for('userLogin')) 
    return render_template('user/login.html', form=form)

@app.route('/user/logout')
def userLogout():
    logout_user()
    return redirect(url_for('home'))

# ############################Reseteo de contraseña##############################

@app.route('/user/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Obtener el usuario actual
        user = RegistroU.query.filter_by(email=form.email.data).first()

        if user:
            # Generar un hash de la nueva contraseña
            new_password_hash = bcrypt.generate_password_hash(form.new_password.data)

            # Actualizar la contraseña del usuario
            user.password = new_password_hash
            db.session.commit()

            flash('Contraseña restablecida exitosamente', 'success')
            return redirect(url_for('userLogin'))
        else:
            flash('Correo electrónico no válido', 'danger')
    return render_template('user/reset_password.html', form=form)
