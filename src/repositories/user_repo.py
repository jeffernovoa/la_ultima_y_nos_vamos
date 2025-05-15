from src.models.user import User

class UserRepository:
    def __init__(self):
        self.usuarios = {}

    def guardar(self, user: User):
        self.usuarios[user.username] = user

    def obtener(self, username):
        return self.usuarios.get(username)

    def existe(self, username):
        return username in self.usuarios