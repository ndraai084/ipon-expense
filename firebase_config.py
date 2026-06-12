import os
import json
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

if "FIREBASE_CREDENTIALS" in os.environ:
    cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("ipon-firebase.json")

firebase_admin.initialize_app(cred)

db = firestore.client()