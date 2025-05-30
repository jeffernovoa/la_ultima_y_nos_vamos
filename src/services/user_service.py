import uuid
import bcrypt
import firebase_admin
from firebase_admin import credentials, auth, db

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://<TU_PROJECTO>.firebaseio.com/"
    })

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def registrar(self, username, password):
        if self.user_repo.get_by_username(username):
            raise Exception("El usuario ya existe.")
        self.user_repo.create(username, password)
        return "Usuario registrado correctamente."

    def login(self, username, password):
        user_data = self.db_ref.child(username).get()
        if not user_data:
            return False

        if bcrypt.checkpw(password.encode(), user_data["password_hash"].encode()):
            token = str(uuid.uuid4())
            self.sesiones[username] = token
            return True
        return False

    def is_logged_in(self, username):
        return username in self.sesiones
