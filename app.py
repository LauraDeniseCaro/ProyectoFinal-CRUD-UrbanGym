import mysql.connector
from mysql.connector import errorcode

#---------------------------------
#SEGUNDA PARTE DSP DE SQL
#---------------------------------
#SE VIENE FLASK
#INSTALAR CON pip install Flask
from flask import Flask, request, jsonify, render_template
from flask import request

#Instalar con pip install flask-cors
#permite la comunicacion entre dos servidores distintos en un el front y en otro el back
from flask_cors import CORS

#despues que desarrollemos los posterior a sql y a flask
#pip install Werkzeug
from werkzeug.utils import secure_filename

#dsp importamos cosas que son de python
import os
import time

#---------------------------------------------------------------
#creamos una instancia de la aplicacion Flask
app = Flask(__name__)
CORS(app)





class Consultas:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS consultas(
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            turno VARCHAR(255) NOT NULL,
            imagen_url VARCHAR(255) NOT NULL,
            asunto VARCHAR(35) NOT NULL,
            mensaje VARCHAR(255) NOT NULL,
            respondida BOOLEAN DEFAULT FALSE)''')
        
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_cliente(self, nombre, email, turno, imagen, asunto, mensaje):
        sql = "INSERT INTO consultas (nombre, email, turno, imagen_url, asunto, mensaje) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, email, turno, imagen, asunto, mensaje)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def consultar_cliente(self, codigo):
        self.cursor.execute(f"SELECT * FROM consultas WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def modificar_cliente(self, codigo, nuevo_nombre, nuevo_email, nuevo_turno, nueva_imagen, nuevo_asunto, nuevo_mensaje):
        sql = "UPDATE consultas SET nombre=%s, email=%s, turno=%s, imagen_url=%s, asunto=%s, mensaje=%s  WHERE codigo = %s"
        valores = (nuevo_nombre, nuevo_email, nuevo_turno, nueva_imagen, nuevo_asunto, nuevo_mensaje, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM consultas")
        clientes = self.cursor.fetchall()
        return clientes

    def eliminar_cliente(self, codigo):
        self.cursor.execute(f"DELETE FROM consultas WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

# Cuerpo del programa principal
# consultas = Consultas(host='localhost', user='root', password='root', database='myapp')

consultas = Consultas(host='lauradenisecar.mysql.pythonanywhere-services.com', user='lauradenisecar', password='caguana2024', database='lauradenisecar$myapp')


# Carpeta para guardar las imagenes.
# RUTA_DESTINO = './static/imagenes/'
RUTA_DESTINO = '/home/lauradenisecar/mysite/static/imagenes'

#LISTAR TODOS LOS CLIENTES
#ahora esto es cuando ya tenemos flask
@app.route("/clientes", methods=["GET"]) #GET metodo para obtener respuestas a nuestras peticiones
def listar_clientes():
    clientes = consultas.listar_clientes()
    return jsonify(clientes)

#MOSTRAR UN SOLO CLIENTE POR EL CODIGO
@app.route("/clientes/<int:codigo>", methods=["GET"])
def mostrar_cliente(codigo):
    cliente = consultas.consultar_cliente(codigo)
    if cliente:
        return jsonify(cliente), 201
    else:
        return "Cliente no encontrado", 404
    

#--------------------------------------------------------------------
# Agregar un  cliente
#--------------------------------------------------------------------
@app.route("/clientes", methods=["POST"])

def agregar_cliente():
    #Recojo los datos del form
    nombre = request.form['nombre']
    email = request.form['email']
    turno = request.form['turno']
    imagen = request.files['imagen']
    asunto = request.form['asunto']  
    mensaje = request.form['mensaje']  
    nombre_imagen=""

    
    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_codigo = consultas.agregar_cliente(nombre, email, turno, nombre_imagen, asunto, mensaje)
    if nuevo_codigo:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si el producto se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Consulta del cliente agregada correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar la consulta del cliente."}), 500
    

#--------------------------------------------------------------------
# Modificar una consulta según su código
#--------------------------------------------------------------------
@app.route("/clientes/<int:codigo>", methods=["PUT"])
def modificar_cliente(codigo):
    #Se recuperan los nuevos datos del formulario
    nuevo_nombre = request.form.get("nombre")
    nuevo_email = request.form.get("email")
    nuevo_turno = request.form.get("turno")
    nuevo_asunto = request.form.get("asunto")
    nuevo_mensaje = request.form.get("mensaje")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el producto guardado
        cliente = consultas.consultar_cliente(codigo)
        if cliente: # Si existe el cliente...
            imagen_vieja = cliente["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del producto
        cliente = consultas.consultar_cliente(codigo)
        if cliente:
            nombre_imagen = cliente["imagen_url"]


    # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos.
    if consultas.modificar_cliente(codigo, nuevo_nombre, nuevo_email, nuevo_turno,nombre_imagen, nuevo_asunto, nuevo_mensaje):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "Consulta modificada"}), 200
    else:
        #Si el producto no se encuentra (por ejemplo, si no hay ningún producto con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Consulta no encontrada"}), 403
    

#--------------------------------------------------------------------
# Eliminar un producto según su código
#--------------------------------------------------------------------
@app.route("/clientes/<int:codigo>", methods=["DELETE"])
def eliminar_cliente(codigo):
    # Busco el producto en la base de datos
    cliente = consultas.consultar_cliente(codigo)
    if cliente: # Si el producto existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = cliente["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el producto del catálogo
        if consultas.eliminar_cliente(codigo):
            #Si el producto se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Consulta eliminada"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el producto no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar la consulta"}), 500
    else:
        #Si el producto no se encuentra (por ejemplo, si no existe un producto con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "Consulta no encontrado"}), 404




#--------------------------Flask--------------------------------
if __name__ == "__main__":
    print("Iniciando la aplicación Flask...")
    app.run(debug=True)
