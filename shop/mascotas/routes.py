from flask import redirect, render_template, url_for, flash, request, session, current_app, flash
from .forms import Addmascotas
from .modelos import Sexo_m, Tipo_m, Ubicacion_m, Estado_m, Addmascota
from ..User.model import RegistroU
from shop  import app,db,photos
from flask_login import current_user, login_required
from flask_uploads import UploadSet, IMAGES
from flask import jsonify
from wtforms import SelectField
from .forms import AddModeloForm
from flask import Flask, render_template, request
from keras.models import load_model
from .reconocimiento_util import predict_image
from shop import search,Search
from .modelos import Formulario_r, RegistroReconocimiento
from werkzeug.utils import secure_filename
import secrets
import os

####################### MAIN  #####################
@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/informacion')
def informacion():
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('mascotas/informacion.html',sexom=sexom, tipom=tipom, estadom=estadom,mascotas=mascotas)

#####################################################################################

#####################################################################################

@app.route('/buscar_mascota/<int:mascota_id>')
def buscar_mascota(mascota_id):
    mascota = Addmascota.query.get(mascota_id)
    mascota_nombre = mascota.nombre if mascota else None

    if mascota_nombre:
        # Redirigir a la página de la mascota utilizando el ID
        return redirect(f'/mascota/{mascota_id}')
    else:
        # Enviar una respuesta de error o redirigir a una página de error
        return "Mascota no encontrada"
    

########################################Reconocimiento###########################

@app.route('/reconocimiento', methods=['GET', 'POST'])
@login_required
def reconocimiento():
    mascotas = Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota, (Sexo_m.id == Addmascota.sexo_id)).all()
    tipom = Tipo_m.query.join(Addmascota, (Tipo_m.id == Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota, (Estado_m.id == Addmascota.estado_id)).all()
    
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                raise ValueError('No se seleccionó ninguna imagen.')

            # Obtener la imagen enviada desde el formulario
            image = request.files['image']

            # Cargar el modelo y realizar la predicción de la imagen
            model = load_model("keras_model.h5", compile=False)
            class_names = open("labels.txt", "r").readlines()
            class_name, confidence_score = predict_image(image, model, class_names)

            # Crear un nuevo registro en la tabla RegistroReconocimiento
            mascota_reconocida = Addmascota.query.filter_by(nombre=class_name).first()
            if mascota_reconocida:
                nuevo_registro = RegistroReconocimiento(usuario_id=current_user.id,
                                                        mascota_id=mascota_reconocida.id,
                                                        nombre_usuario=current_user.nombre,
                                                        nombre_mascota=class_name,
                                                        telefono_usuario=current_user.telefono,
                                                        )
                db.session.add(nuevo_registro)
                db.session.commit()

            return render_template('mascotas/reconocimiento.html',
                                class_name=class_name, confidence_score=confidence_score)

        except Exception as e:
            error_message = str(e)
            flash('Error, no se ha seleccionado ninguna imagen', 'danger')
            return render_template('mascotas/reconocimiento.html', error=error_message,
                                class_name=None, confidence_score=None)

    return render_template('mascotas/reconocimiento.html', sexom=sexom, tipom=tipom, estadom=estadom, mascotas=mascotas)



@app.route('/reconocimientoimg', methods=['GET', 'POST'])
@login_required
def reconocimientoimg():
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                raise ValueError('No se seleccionó ninguna imagen.')
        # Obtener la imagen enviada desde el formulario
            image = request.files['image']

        # Cargar el modelo y realizar la predicción de la imagen
            model = load_model("keras_model.h5", compile=False)
            class_names = open("labels.txt", "r").readlines()
            class_name, confidence_score = predict_image(image, model, class_names)
            
            # Obtener el ID de la mascota basado en el nombre resultante de la predicción
            mascota = Addmascota.query.filter_by(nombre=class_name).first()
            mascota_id = mascota.id if mascota else None
            
            # Obtener los detalles del usuario actual
            nombre_mascota = class_name
            nombre_usuario = current_user.nombre
            telefono_usuario = current_user.telefono
            usuario_id= current_user.id
            mascota_id= mascota_id
            
            registro = RegistroReconocimiento( nombre_usuario=nombre_usuario, telefono_usuario=telefono_usuario, nombre_mascota=nombre_mascota, usuario_id= usuario_id,mascota_id=mascota_id)
            db.session.add(registro)
            db.session.commit()
            
            registros = RegistroReconocimiento.query.all()

            
            return render_template('mascotas/reconocimientoimg.html',
            class_name=class_name,confidence_score=confidence_score, nombre_usuario=nombre_usuario, telefono_usuario=telefono_usuario, registros=registros)
            
            
        
        
        except Exception as e:
            error_message = str(e)
            flash(f'Error, no ha seleccionado ninguna imagen', 'danger')
            print(f'Error: {error_message}')  # Imprimir el mensaje de error
            return render_template('mascotas/reconocimientoimg.html', error=error_message,
                                class_name=None, confidence_score=None)
            
        

    return render_template('mascotas/reconocimientoimg.html',sexom=sexom, tipom=tipom, estadom=estadom, mascotas=mascotas)


####################Fin Reconocimiento #########################################
@app.route('/nosotros')
def nosotros():
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('/nosotros.html',sexom=sexom, tipom=tipom, estadom=estadom, mascotas=mascotas)



@app.route('/mascotas/mimascota')
@login_required

def mimascota():
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('mascotas/mimascota.html', title='Mi mascota', mascotas=mascotas, sexom=sexom, tipom=tipom, estadom=estadom)

########################Formulario de regidtro de imágenes para el modelo######################

# UPLOAD_FOLDER = "C:/Users/juana/Desktop/HuellitasFinal/shop/static/images"

# @app.route('/mascotas/addfotos', methods=['GET', 'POST'])
# @login_required
# def addfotos():
#     mascotas = Addmascota.query.filter_by(user_id=current_user.id).all()

#     if request.method == 'POST':
#         mascota_id = request.form.get('mascota')
#         mascota = Addmascota.query.get(mascota_id)

#         if mascota:
#             # Crear una carpeta con el nombre de la mascota
#             folder_path = os.path.join(UPLOAD_FOLDER, mascota.nombre)
#             os.makedirs(folder_path, exist_ok=True)

#             # Guardar las fotos en la carpeta correspondiente
#             image_1 = photos.save(request.files.get('image_1'), folder=folder_path, name="image_1.")
#             image_2 = photos.save(request.files.get('image_2'), folder=folder_path, name="image_2.")
#             image_3 = photos.save(request.files.get('image_3'), folder=folder_path, name="image_3.")
#             image_4 = photos.save(request.files.get('image_4'), folder=folder_path, name="image_4.")
#             image_5 = photos.save(request.files.get('image_5'), folder=folder_path, name="image_5.") 
#             image_6 = photos.save(request.files.get('image_6'), folder=folder_path, name="image_6.")
#             image_7 = photos.save(request.files.get('image_7'), folder=folder_path, name="image_7.")
#             image_8 = photos.save(request.files.get('image_8'), folder=folder_path, name="image_8.")
#             image_9 = photos.save(request.files.get('image_9'), folder=folder_path, name="image_9.")
#             image_10 = photos.save(request.files.get('image_10'), folder=folder_path, name="image_10.")
            
#             formulario = Formulario_r(
#                 nombre=mascota.nombre,
#                 image_1=image_1,
#                 image_2=image_2,
#                 image_3=image_3,
#                 image_4=image_4,
#                 image_5=image_5,
#                 image_6=image_6,
#                 image_7=image_7,
#                 image_8=image_8,
#                 image_9=image_9,
#                 image_10=image_10
#             )

#             db.session.add(formulario)
#             db.session.commit()

#             flash('Las imágenes se han agregado correctamente', 'success')
#             return redirect(url_for('addfotos'))

#     return render_template('/mascotas/addfotos.html', mascotas=mascotas)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = "C:/Users/juana/Desktop/HuellitasFinal/shop/static/images"

@app.route('/mascotas/addfotos', methods=['GET', 'POST'])
@login_required
def addfotos():
    mascotas = Addmascota.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        mascota_id = request.form.get('mascota')
        mascota = Addmascota.query.get(mascota_id)
        
        

        if mascota:
            # Crear una carpeta con el nombre de la mascota
            folder_path = os.path.join(UPLOAD_FOLDER, mascota.nombre)
            os.makedirs(folder_path, exist_ok=True)

            # Guardar las imágenes en la carpeta correspondiente
            images = request.files.getlist('images')
            image_names = []  # Lista para almacenar los nombres de archivo de las imágenes seleccionadas
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(folder_path, filename))
                    image_names.append(filename)

            formulario = Formulario_r(nombre=mascota.nombre)
            formulario.addmascota_id = mascota_id


            db.session.add(formulario)
            db.session.commit()

            flash('Las imágenes se han agregado correctamente', 'success')
            return redirect(url_for('addfotos', mascota_id=mascota_id, image_names=image_names))

    return render_template('/mascotas/addfotos.html', mascotas=mascotas)

#######################Fin formulario Addmodelo ###############################################
@app.route('/result')
def result():
    searchword = request.args.get('q')
    mascotas = Addmascota.query.msearch(searchword, fields=['nombre', 'descripcion'], limit=6)
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    return render_template('mascotas/result.html', mascotas=mascotas,sexom=sexom, tipom=tipom,estadom=estadom)

@app.route('/mascotas/allmascotas')
def allmascotas():
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('mascotas/index.html', mascotas=mascotas, sexom=sexom, tipom=tipom,estadom=estadom)

@app.route('/mascota/<int:id>')
def single_page(id):
    mascota=Addmascota.query.get_or_404(id)
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('mascotas/single_page.html', mascota=mascota, sexom=sexom, tipom=tipom, estadom=estadom)

@app.route('/estado/<int:id>')
def get_estado(id): 
    estado = Addmascota.query.filter_by(estado_id=id)
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    return render_template('mascotas/index.html', estado = estado, estadom=estadom, tipom=tipom,sexom=sexom)

@app.route('/tipo/<int:id>')
def get_tipo(id): 
    tipo = Addmascota.query.filter_by(tipo_id=id)
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    return render_template('mascotas/index.html', tipo = tipo, tipom=tipom, estadom=estadom,sexom=sexom)

@app.route('/sexo/<int:id>')
def get_sexo(id): 
    sexo = Addmascota.query.filter_by(sexo_id=id)
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
    return render_template('mascotas/index.html', sexo = sexo, sexom=sexom, tipom=tipom, estadom=estadom)


################ actualizar##################

@app.route('/actualizarsexo/<int:id>', methods=['GET' , 'POST'])
def actualizarsexo(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes de actualizar','danger')
    actualizarsexo= Sexo_m.query.get_or_404(id)
    sexo=request.form.get('sexo')
    if request.method=="POST":
        actualizarsexo.sexo_m=sexo
        flash(f'El sexo ha sido actualizado', 'success')
        db.session.commit()
        return redirect(url_for('sexos'))
    return render_template('mascotas/actualizarsexo.html', title='Actualizar sexo', actualizarsexo=actualizarsexo)



@app.route('/actualizarubicacion/<int:id>', methods=['GET' , 'POST'])
def actualizarubicacion(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes de actualizar','danger')
    actualizarubicacion= Ubicacion_m.query.get_or_404(id)
    ubicacion=request.form.get('ubicacion')
    if request.method=="POST":
        actualizarubicacion.ubicacion_m=ubicacion
        flash(f'La ubicacion ha sido actualizada', 'success')
        db.session.commit()
        return redirect(url_for('ubicaciones'))
    return render_template('mascotas/actualizarsexo.html', title='Actualizar ubicacion', actualizarubicacion=actualizarubicacion)


@app.route('/actualizartipo/<int:id>', methods=['GET' , 'POST'])
def actualizartipo(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes de actualizar','danger')
    actualizartipo= Tipo_m.query.get_or_404(id)
    tipo=request.form.get('tipo')
    if request.method=="POST":
        actualizartipo.tipo_m=tipo
        flash(f'El tipo ha sido actualizado', 'success')
        db.session.commit()
        return redirect(url_for('tipos'))
    return render_template('mascotas/actualizarsexo.html', title='Actualizar ubicacion', actualizartipo=actualizartipo)


@app.route('/actualizarestado/<int:id>', methods=['GET' , 'POST'])
def actualizarestado(id):
    if 'email' not in session:
        flash(f'Inicie sesion antes de actualizar','danger')
    actualizarestado= Estado_m.query.get_or_404(id)
    estado=request.form.get('estado')
    if request.method=="POST":
        actualizarestado.estado_m=estado
        flash(f'El estado ha sido actualizado', 'success')
        db.session.commit()
        return redirect(url_for('estados'))
    return render_template('mascotas/actualizarsexo.html', title='Actualizar ubicacion', actualizarestado=actualizarestado)




################################ Ingreso ###################################


@app.route('/addsexo' , methods=['GET', 'POST'])
def addsexo():
    if "correo" not in session:
        flash(f'Inicie sesion antes de agregar un sexo','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getsexo=request.form.get('sexo')
        sexo= Sexo_m(sexo_m=getsexo)
        db.session.add(sexo)
        flash(f' El sexo {getsexo} ha sido añadido correctamente','success' )
        db.session.commit()
        return redirect(url_for('addsexo'))
    
    return render_template('mascotas/sexo.html', sexos='sexos')


@app.route('/addtipo' , methods=['GET', 'POST'])
def addtipo():
    if 'correo' not in session:
        flash(f'Inicie sesion antes de agregar un tipo de mascota','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        gettipo=request.form.get('tipo')
        tipo= Tipo_m(tipo_m=gettipo)
        db.session.add(tipo)
        flash(f' El tipo {gettipo} ha sido añadido correctamente','success' )
        db.session.commit()
        return redirect(url_for('addtipo'))
    
    return render_template('mascotas/sexo.html',  tipos='tipos')


@app.route('/addubicacion' , methods=['GET', 'POST'])
def addubicacion():
    if 'correo' not in session:
        flash(f'Inicie sesion antes de agregar una ubicación','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getubicacion=request.form.get('ubicacion')
        ubicacion= Ubicacion_m(ubicacion_m=getubicacion)
        db.session.add(ubicacion)
        flash(f' La ubicacion {getubicacion} ha sido añadido correctamente','success' )
        db.session.commit()
        return redirect(url_for('addubicacion'))
    
    return render_template('mascotas/sexo.html', ubicaciones='ubicaciones')


@app.route('/addestado' , methods=['GET', 'POST'])
def addestado():
    if 'correo' not in session:
        flash(f'Inicie sesion antes de agreagar un estado','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getestado=request.form.get('estado')
        estado= Estado_m(estado_m=getestado)
        db.session.add(estado)
        flash(f' El estado {getestado} ha sido añadido correctamente','success' )
        db.session.commit()
        return redirect(url_for('addestado'))
    
    return render_template('mascotas/sexo.html', estados='estados')

####################################Borrar###########################################

@app.route('/eliminarsexo/<int:id>', methods=['POST'])
def eliminarsexo(id):
    sexo= Sexo_m.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(sexo)
        db.session.commit()
        flash(f'El sexo {sexo.sexo_m} ha sido eliminado correctamente', 'success')
        return redirect(url_for('admin'))
    flash(f'El sexo {sexo.sexo_m} no ha podido ser eliminado correctamente', 'warning')
    return redirect(url_for('admin'))
    

@app.route('/eliminarubicacion/<int:id>', methods=['POST'])
def eliminarubicacion(id):
    ubicacion= Ubicacion_m.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(ubicacion)
        db.session.commit()
        flash(f'La ubicación {ubicacion.ubicacion_m} ha sido eliminado correctamente', 'success')
        return redirect(url_for('admin'))
    flash(f'La ubicación {ubicacion.ubicacion_m} no ha podido ser eliminado correctamente', 'warning')
    return redirect(url_for('admin'))



@app.route('/eliminartipo/<int:id>', methods=['POST'])
def eliminartipo(id):
    tipo= Tipo_m.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(tipo)
        db.session.commit()
        flash(f'El tipo {tipo.tipo_m} ha sido eliminado correctamente', 'success')
        return redirect(url_for('admin'))
    flash(f'El tipo {tipo.tipo_m} no ha podido ser eliminado correctamente', 'warning')
    return redirect(url_for('admin'))




@app.route('/eliminarestado/<int:id>', methods=['POST'])
def eliminarestado(id):
    estado= Estado_m.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(estado)
        db.session.commit()
        flash(f'El estado {estado.estado_m} ha sido eliminado correctamente', 'success')
        return redirect(url_for('admin'))
    flash(f'El estado {estado.estado_m} no ha podido ser eliminado correctamente', 'warning')
    return redirect(url_for('admin'))


#######################Eliminar mascota ADMIN

@app.route('/eliminarmascota/<int:id>' ,methods=['POST'])
def eliminarmascota(id):
    mascota=Addmascota.query.get_or_404(id)
    if request.method=="POST":
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_3))
            except Exception as e:
                print(e)
                
            db.session.delete(mascota) 
            db.session.commit()
            flash(f'La mascota {mascota.nombre} ha sido eliminada', 'success')
            return redirect(url_for('admin'))
    flash(f'Puede eliminar esta mascota')    
    return redirect(url_for('admin'))

#######################Eliminar mascota User###############################

@app.route('/eliminarmascotau/<int:id>' ,methods=['POST'])
def eliminarmascotau(id):
    mascota=Addmascota.query.get_or_404(id)
    if current_user.is_authenticated:
    
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + mascota.image_3))
            except Exception as e:
                print(e)
                
            db.session.delete(mascota) 
            db.session.commit()
            flash(f'La mascota {mascota.nombre} ha sido eliminada', 'success')
    else:
            flash(f'No tienes permisos para eliminar esta mascota', 'error')
    
            # Redirecciona a la página actual
            return redirect(request.referrer)

    # Agrega esta línea como retorno por defecto
    return redirect(request.referrer)
############################## Añadir Mascota #######################################
@app.route('/addmascota', methods=['POST','GET'])
@login_required
def addmascota():
    
    sexos = Sexo_m.query.all()
    tipos = Tipo_m.query.all()
    ubicaciones = Ubicacion_m.query.all()
    estados = Estado_m.query.all()
    form = Addmascotas(request.form)
    if request.method == "POST":
        nombre = form.nombre.data
        edad= form.edad.data
        raza= form.raza.data
        contacto= form.contacto.data
        direccion= form.direccion.data
        descripcion= form.descripcion.data
        fecha= form.fecha.data
        sexo= request.form.get('sexo')
        tipo=request.form.get('tipo')
        ubicacion = request.form.get('ubicacion')
        estado = request.form.get('estado')
        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
        user_id = current_user.id 
        
        addmas= Addmascota(nombre=nombre, edad=edad, raza=raza, contacto=contacto,direccion=direccion,descripcion=descripcion,fecha=fecha,sexo_id=sexo, 
                            tipo_id=tipo, ubicacion_id=ubicacion,estado_id=estado,image_1=image_1, image_2=image_2, image_3=image_3,user_id=user_id)
        db.session.add(addmas)
        
        db.session.commit()
        flash(f'Su mascota {nombre} ha sido agregada correctamente', 'success')
        return redirect(url_for('allmascotas'))
    mascotas= Addmascota.query.all()
    sexom = Sexo_m.query.join(Addmascota,(Sexo_m.id==Addmascota.sexo_id)).all()
    tipom= Tipo_m.query.join(Addmascota,(Tipo_m.id==Addmascota.tipo_id)).all()
    estadom = Estado_m.query.join(Addmascota,(Estado_m.id==Addmascota.estado_id)).all()
        
    return render_template('mascotas/addmascota.html', title="Ingreso de datos de su mascota", 
    form=form, sexos=sexos, tipos=tipos, ubicaciones=ubicaciones, estados=estados, mascotas=mascotas, sexom=sexom, tipom=tipom,estadom=estadom)
    
    
########################## EDITAR MASCOTA ####################
from flask_login import current_user, login_required

@app.route('/editmascota/<int:id>', methods=['GET', 'POST'])
@login_required
def editmascota(id):
    mascota = Addmascota.query.get_or_404(id)
    
    # Verificar si el usuario actual es el dueño de la mascota
    if mascota.user_id != current_user.id:
        flash('No tienes permiso para editar esta mascota.', 'danger')
        return redirect(url_for('allmascotas'))

    sexos = Sexo_m.query.all()
    tipos = Tipo_m.query.all()
    ubicaciones = Ubicacion_m.query.all()
    estados = Estado_m.query.all()

    form = Addmascotas(request.form)

    if request.method == "POST":
        mascota.nombre = form.nombre.data
        mascota.edad = form.edad.data
        mascota.raza = form.raza.data
        mascota.contacto = form.contacto.data
        mascota.direccion = form.direccion.data
        mascota.descripcion = form.descripcion.data
        mascota.sexo_id = request.form.get('sexo')
        mascota.tipo_id = request.form.get('tipo')
        mascota.ubicacion_id = request.form.get('ubicacion')
        mascota.estado_id = request.form.get('estado')

        # Verificar si se ha cargado una nueva imagen y guardarla
        if request.files.get('image_1'):
            mascota.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            mascota.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            mascota.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        flash(f'La mascota {mascota.nombre} ha sido actualizada correctamente', 'success')
        return redirect(url_for('allmascotas'))

    # Preseleccionar los valores actuales en el formulario de edición
    form.nombre.data = mascota.nombre
    form.edad.data = mascota.edad
    form.raza.data = mascota.raza
    form.contacto.data = mascota.contacto
    form.direccion.data = mascota.direccion
    form.descripcion.data = mascota.descripcion

    return render_template('mascotas/editmascota.html', title="Editar Mascota",
    id=mascota.id,form=form, sexos=sexos, tipos=tipos, ubicaciones=ubicaciones,
    estados=estados, mascota=mascota)


