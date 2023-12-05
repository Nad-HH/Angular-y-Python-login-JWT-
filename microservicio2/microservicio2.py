from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Reemplaza con tu clave secreta real
jwt = JWTManager(app)


@app.route('/microservicio2', methods=['GET'])
def obtener_datos_del_microservicio2():
    try:
        # Lógica para obtener datos del microservicio 2
        return jsonify(message='Datos del microservicio 2 obtenidos correctamente'), 200
    except Exception as e:
        app.logger.error(f'Error en el microservicio 2: {str(e)}')
        return jsonify(message='Error en el microservicio 2'), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)
