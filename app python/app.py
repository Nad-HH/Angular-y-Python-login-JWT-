from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)  # Esto habilita CORS para toda la aplicación

# Resto de tu configuración y rutas
#cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Cambia esto por una clave segura
jwt = JWTManager(app)

#******************prueba de microservicio************************************
# Definir access_token con un valor predeterminado o nulo
access_token = None

url_microservicio2 = "http://localhost:5001/microservicio2"  #  puerto del mciroservicio
if access_token is not None:
    token_jwt = access_token  # Reemplaza con el token JWT real
# Definir token_jwt antes de la prueba del microservicio
token_jwt = None
# Verificar si token_jwt está definida antes de utilizarla
if token_jwt is not None:
    headers = {"Authorization": f"Bearer {token_jwt}"}

    # Realiza una solicitud al segundo microservicio con el token en la cabecera
    response = requests.get(url_microservicio2, headers=headers)

    # Procesa la respuesta según sea necesario
    if response.status_code == 200:
        datos_microservicio2 = response.json()
        print("Datos del segundo microservicio:", datos_microservicio2)
    else:
        print("Error al obtener datos del segundo microservicio. Código de estado:", response.status_code)
else:
    print("token_jwt no está definido. No se realizará la prueba del microservicio.")


# Nueva ruta de prueba para verificar la conexión con el microservicio 2
@app.route('/test-microservicio2', methods=['GET'])
def test_microservicio2():
    try:
        url_microservicio2 = "http://localhost:5001/microservicio2"
        headers = {"Authorization": f"Bearer {token_jwt}"}  # Asegúrate de enviar el token

        response = requests.get(url_microservicio2, headers=headers)

        if response.status_code == 200:
            datos_microservicio2 = response.json()
            return jsonify(message=f'Conexión exitosa con microservicio 2. Datos recibidos: {datos_microservicio2}'), 200
        else:
            app.logger.error(f'Error al conectar con microservicio 2. Código de estado: {response.status_code}. Respuesta: {response.text}')
            return jsonify(message=f'Error al conectar con microservicio 2. Código de estado: {response.status_code}'), 500
    except Exception as e:
        app.logger.error(f'Error interno al procesar la solicitud de prueba: {str(e)}')
        return jsonify(message='Error interno al procesar la solicitud de prueba'), 500
#*****************************************************************************



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
    
