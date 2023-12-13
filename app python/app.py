from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)  # Esto habilita CORS para toda la aplicación

# Resto de tu configuración y rutas
#cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

app.config['JWT_SECRET_KEY'] = 'your_secret_key' 
jwt = JWTManager(app)


# Modelo de Usuario (solo con propósito demostrativo)
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Datos de usuario (solo con propósito demostrativo)
users = [
    User(1, 'admin', '123456'),
]

# Lista de ejemplo de estudiantes (simulación de datos de una base de datos)
lista_de_estudiantes = [
    {"id": 1, "nombre": "Estudiante 1", "edad": 20},
    {"id": 2, "nombre": "Estudiante 2", "edad": 22},
    {"id": 3, "nombre": "Estudiante 3", "edad": 23},
    {"id": 4, "nombre": "Estudiante 3", "edad": 23},
]
# Función de simulación para obtener datos de estudiantes
def obtener_datos_de_estudiantes(current_user):
    # Simplemente devuelve la lista completa de estudiantes
    return lista_de_estudiantes

# Nueva ruta para la raíz
@app.route('/')
def home():
    return jsonify(message='Bienvenido al backend en python!'), 200

# Configuración de Flask-JWT-Extended (autenticación de usuarios) 
@app.route('/login', methods=['POST'])
def login():
    global access_token  # Usar global para acceder a la variable externa
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = next((user for user in users if user.username == username), None)
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
# Ruta protegida con autenticación JWT-Extended
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    
    # Obtén los datos de los estudiantes para el usuario actual (simulación)
    students_data = obtener_datos_de_estudiantes(current_user)

    return jsonify(logged_in_as=current_user, students=students_data), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Elimina las cookies JWT para cerrar la sesión
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

if __name__ == '__main__':
    app.run(debug=True)
    
