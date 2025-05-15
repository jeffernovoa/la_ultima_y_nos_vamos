from src.models.user import User
import uuid

class UserService:
    def __init__(self, repo):
        self.repo = repo
        self.sesiones = {}

    def register(self, username, password):
        if self.repo.existe(username):
            raise Exception("Usuario ya existe")
        user = User(username, password)
        self.repo.guardar(user)

    def login(self, username, password):
        user = self.repo.obtener(username)
        if user and user.verify_password(password):
            token = str(uuid.uuid4())
            self.sesiones[username] = token
            return token
        raise Exception("Credenciales inválidas")

    def is_logged_in(self, username):
        return username in self.sesiones