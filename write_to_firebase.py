import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("./league-of-intelligence-firebase-adminsdk-82djt-58c573b384.json")
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://league-of-intelligence.firebaseio.com/'
})

db = firestore.client()
doc_ref = db.collection(u'matches').document(u'EUW').collection('matches_data')

with open("matches.json", "r") as f:
	file_contents = json.load(f)
for match_data in file_contents:
	doc_ref.document().set(match_data)