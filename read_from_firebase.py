import firebase_admin
from firebase_admin import credentials, firestore

def fetch_matches_data(region = "EUW", rank = "challenger"):
    return db.collection(u'matches').document(u'' + region).collection(rank)

regions = ["EUW", "KR", "NA"]
ranks = ["iron", "bronze", "silver", "gold", "platinium", "diamond", "master", "grandmaster", "challenger"]

cred = credentials.Certificate("./league-of-intelligence-firebase-adminsdk-82djt-58c573b384.json")
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://league-of-intelligence.firebaseio.com/'
})
db = firestore.client()

for region in regions:
    for rank in ranks:
        doc_ref = fetch_matches_data(region, rank)
        docs = doc_ref.stream()

        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')



# This script is to print the datas from the different regions colection feel free to modify it as you please