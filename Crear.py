from flask import Flask, request, jsonify
import mysql.connector

crear_codigo_bp = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="siru"
)

@crear_codigo_bp.route('/crear_codigo', methods=['POST'])
def crear_codigo():
    data = request.get_json()

    codigo = data.get('codigo')
    tipo = data.get('tipo')
    estado = data.get('estado', True)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM Usuario WHERE codigo = %s", (codigo,))
    usuario_existente = cursor.fetchone()
    if usuario_existente:
        return jsonify({'success': False, 'message': 'El código ya existe'})

    # Insertar un nuevo registro en la tabla Usuario
    try:
         cursor.execute("INSERT INTO Usuario (codigo, tipo, nombre, contraseña, estado) VALUES (%s, %s, '', '', %s)", 
                   (codigo, tipo, estado))
         db.commit()

         return jsonify({'success': True, 'message': 'Código creado exitosamente'})
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()



if __name__ == '__main__':
    crear_codigo_bp.run(host='0.0.0.0', port=5000)