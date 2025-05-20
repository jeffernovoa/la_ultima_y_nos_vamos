import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("/Users/jeffer/Documents/GitHub/la_ultima_y_nos_vamos/firebase.json")
firebase_admin.initialize_app(cred)

firebase_db = firestore.client()
