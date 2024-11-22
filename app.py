from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
load_dotenv()
app = Flask(__name__)

# Configuración de conexión (usando variables de entorno)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'eduardo')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'e1d2o0p6m')
DB_NAME = os.getenv('DB_NAME', 'refaccionaria')

# Función para manejar la conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para agregar un producto
@app.route('/nuevo', methods=['POST'])
def nuevo_producto():
    data = request.json
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO productos (nombre, numero, cantidad) VALUES (%s, %s, %s)"
            cursor.execute(query, (data['nombre'], data['numero'], data['cantidad']))
            connection.commit()
            return jsonify({'message': 'Producto agregado con éxito'})
        except Error as e:
            print(f"Error al agregar producto: {e}")
            return jsonify({'error': 'No se pudo agregar el producto'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

# Ruta para modificar un producto
@app.route('/modificar', methods=['PUT'])
def modificar_producto():
    data = request.json
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE productos SET nombre = %s, cantidad = %s WHERE id = %s"
            cursor.execute(query, (data['nombre'], data['cantidad'], data['id']))
            connection.commit()
            return jsonify({'message': 'Producto actualizado con éxito'})
        except Error as e:
            print(f"Error al modificar producto: {e}")
            return jsonify({'error': 'No se pudo actualizar el producto'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

# Ruta para eliminar un producto
@app.route('/eliminar', methods=['DELETE'])
def eliminar_producto():
    data = request.json
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM productos WHERE id = %s"
            cursor.execute(query, (data['id'],))
            connection.commit()
            return jsonify({'message': 'Producto eliminado con éxito'})
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            return jsonify({'error': 'No se pudo eliminar el producto'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

# Ruta para obtener los últimos 10 productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id DESC LIMIT 10")
            productos = cursor.fetchall()
            return jsonify(productos)
        except Error as e:
            print(f"Error al obtener productos: {e}")
            return jsonify({'error': 'No se pudieron obtener los productos'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

if __name__ == '__main__':
    app.run(debug=True)