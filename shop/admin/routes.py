from flask import render_template, session,  request, redirect, url_for, flash
from shop import app, db, bcrypt
from.forms import RegistrationForm,LoginForm
from shop.mascotas.modelos import Addmascota, Sexo_m, Tipo_m, Ubicacion_m, Estado_m
from.modelos import usuario
import os




@app.route('/admin')
def admin():
    if 'correo' not in session:
        flash(f'Inicie sessión primero','danger')
        return redirect(url_for('login'))
    mascotas= Addmascota.query.all()
    return render_template('admin/index.html', title='Pagina del administrador', mascotas=mascotas)

@app.route('/')
def principal():
    return render_template('./index.html', title='Página principal')

@app.route('/sexos')
def sexos():
    if 'correo' not in session:
        flash(f'Inicie sessión primero','danger')
        return redirect(url_for('login'))
    sexos = Sexo_m.query.order_by(Sexo_m.id.desc()).all()
    return render_template('admin/sexo.html', title="Pagina de sexo mascota", sexos=sexos)


@app.route('/tipos')
def tipos():
    if 'correo' not in session:
        flash(f'Inicie sessión primero','danger')
        return redirect(url_for('login'))
    tipos = Tipo_m.query.order_by(Tipo_m.id.desc()).all()
    return render_template('admin/sexo.html', title="Pagina de tipo mascota", tipos=tipos)

@app.route('/ubicaciones')
def ubicaciones():
    if 'correo' not in session:
        flash(f'Inicie sessión primero','danger')
        return redirect(url_for('login'))
    ubicaciones = Ubicacion_m.query.order_by(Ubicacion_m.id.desc()).all()
    return render_template('admin/sexo.html', title="Pagina de ubicación de la mascota", ubicaciones=ubicaciones)


@app.route('/estados')
def estados():
    if 'correo' not in session:
        flash(f'Inicie sessión primero','danger')
        return redirect(url_for('login'))
    estados = Estado_m.query.order_by(Estado_m.id.desc()).all()
    return render_template('admin/sexo.html', title="Pagina de estado de la mascota", estados=estados)




@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = usuario(nombre=form.nombre.data, correo=form.correo.data,
        password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f' Bienvenido {form.nombre.data} Registro realizado con éxito','success')
        return redirect(url_for('login'))
    return render_template('admin/registro.html', form=form, title="Página de registro")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user=usuario.query.filter_by(correo=form.correo.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['correo']=form.correo.data
            flash(f' Bienvenido {form.correo.data} acabas de ingresar con éxito','success')
            return redirect(request.args.get('next')or url_for('admin'))
        else:
            flash('Correo o contraseña incorrectos, por favor ingrese nuevamente','danger')
    return render_template('admin/login.html', form=form, title="Página de login")
    #return render_template('./index.html', form=form, title="Página de login del admin")


################################ LOGOUT ####################################

@app.route('/logout')
def logout():
    session.pop('correo')
    return redirect(url_for('principal'))