from src.models.user import User
from firebase_admin import db
from pymongo import MongoClient

class UserRepository:
    def __init__(self, mongo_uri=None, firebase_root="users"):
        self.firebase_ref = db.reference(firebase_root)
        if mongo_uri:
            self.mongo_client = MongoClient(mongo_uri)
            self.mongo_db = self.mongo_client["voting_app"]
            self.mongo_users = self.mongo_db["users"]
        else:
            self.mongo_client = None

    def save(self, user: User):
        # Firebase
        self.firebase_ref.child(user.user_id).set(user.to_dict())
        # MongoDB
        if self.mongo_client:
            self.mongo_users.update_one(
                {"user_id": user.user_id},
                {"$set": user.to_dict()},
                upsert=True
            )

    def get_by_username(self, username: str) -> User | None:
        # Firebase search
        users = self.firebase_ref.get()
        if users:
            for u in users.values():
                if u["username"] == username:
                    return User.from_dict(u)

        # MongoDB fallback
        if self.mongo_client:
            data = self.mongo_users.find_one({"username": username})
            if data:
                return User.from_dict(data)
        return None
    
    def create(self, username, password):
        # Crea el usuario en la base de datos
        pass  # Implementa la lógica real

    def list_all(self) -> list[User]:
        results = []
        firebase_data = self.firebase_ref.get() or {}
        for user in firebase_data.values():
            results.append(User.from_dict(user))
        return results
