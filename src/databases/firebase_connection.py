import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_config.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://usuarios-y-credenciales.firebaseio.com/' 
        })