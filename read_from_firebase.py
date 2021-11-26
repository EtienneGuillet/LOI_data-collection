import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("./league-of-intelligence-firebase-adminsdk-82djt-58c573b384.json")
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://league-of-intelligence.firebaseio.com/'
})

db = firestore.client()
doc_ref = doc_ref = db.collection(u'matches').document(u'EUW').collection('matches_data')
docs = doc_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')