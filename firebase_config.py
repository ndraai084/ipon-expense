import os
import json
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

firebase_json = os.environ["FIREBASE_CREDENTIALS"]

cred_dict = json.loads(firebase_json)

cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()