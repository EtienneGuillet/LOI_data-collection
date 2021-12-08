import re
from riotwatcher import LolWatcher, ApiError
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./league-of-intelligence-firebase-adminsdk-82djt-58c573b384.json")
firebase_admin.initialize_app(cred, {
'databaseURL': 'https://league-of-intelligence.firebaseio.com/'
})

db = firestore.client()
lol_watcher = LolWatcher('RGAPI-0f6d97b7-8df9-44c0-aedd-44243730acde')

def get_puuid(region, player_data):
    try:
        return lol_watcher.summoner.by_id(region, player_data['summonerId'])['puuid']
    except ApiError as err:
        print(f'Cant find puuid from player id: {player_data["summonerId"]}')
        return -1

def get_matches_id(region_match, puuid):
    try:
        return lol_watcher.match.matchlist_by_puuid(region_match, puuid)
    except ApiError as err:
        print(f'Cant find matches id from puuid: {puuid}')
        return -1

def get_match_data(region_match, match_id):
    try:
        return lol_watcher.match.by_id(region_match, match_id)
    except ApiError as err:
        print(f'Cant find match data from match id: {match_id}')
        return -1

def save_match_data(region_db, rank, match_data):
    doc_ref = db.collection(u'matches').document(u'%s' % region_db).collection(rank)
    if (match_data == -1):
        return
    matchId = match_data['metadata']['matchId']
    doc = doc_ref.document(matchId).get()
    if doc.exists:
        print(f'Match data already on database: {matchId}')
    else:
        doc_ref.document(matchId).set(match_data)
        print(f'Added new match data: {matchId}') 

def handle_matches_id(region, rank, matches_id):
    for match_id in matches_id:
        match_data = get_match_data(region[1], match_id)
        save_match_data(region[2], rank, match_data)

def handle_players(region, rank, players):
    for player in players:
        puuid = get_puuid(region[0], player)
        if (puuid == -1):
            continue
        matches_id = get_matches_id(region[1], puuid)
        if (matches_id == -1):
            continue
        handle_matches_id(region, rank, matches_id)

regions = [('NA1', 'AMERICAS', 'NA'), ('KR', 'ASIA', 'KR'), ('EUW1', 'EUROPE', 'EUW')]
ranks = ['challenger', 'grandmaster', 'master', 'diamond', 'platinum', 'gold', 'silver', 'bronze']
queue = "RANKED_SOLO_5x5"

for region in regions:
    for rank in ranks:
        players = []
        if (rank == 'challenger'):
            try:
                players = lol_watcher.league.challenger_by_queue(region[0], queue)['entries']
            except ApiError as err:
                continue
        elif (rank == 'grandmaster'):
            try:
                players = lol_watcher.league.grandmaster_by_queue(region[0], queue)['entries']
            except ApiError as err:
                continue
        elif (rank == 'master'):
            try:
                players = lol_watcher.league.masters_by_queue(region[0], queue)['entries']
            except ApiError as err:
                continue    
        elif (rank == 'diamond'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "DIAMOND", "I"), *lol_watcher.league.entries(region[0], queue, "DIAMOND", "II"), *lol_watcher.league.entries(region[0], queue, "DIAMOND", "III"),  *lol_watcher.league.entries(region[0], queue, "DIAMOND", "IV")]
            except ApiError as err:
                continue
        elif (rank == 'platinum'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "PLATINUM", "I"), *lol_watcher.league.entries(region[0], queue, "PLATINUM", "II"), *lol_watcher.league.entries(region[0], queue, "PLATINUM", "III"), *lol_watcher.league.entries(region[0], queue, "PLATINUM", "IV")]
            except ApiError as err:
                continue
        elif (rank == 'gold'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "GOLD", "I"), *lol_watcher.league.entries(region[0], queue, "GOLD", "II"), *lol_watcher.league.entries(region[0], queue, "GOLD", "III"), *lol_watcher.league.entries(region[0], queue, "GOLD", "IV")]
            except ApiError as err:
                continue
        elif (rank == 'silver'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "SILVER", "I"), *lol_watcher.league.entries(region[0], queue, "SILVER", "II"), *lol_watcher.league.entries(region[0], queue, "SILVER", "III"), *lol_watcher.league.entries(region[0], queue, "SILVER", "IV")]
            except ApiError as err:
                continue
        elif (rank == 'bronze'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "BRONZE", "I"), *lol_watcher.league.entries(region[0], queue, "BRONZE", "II"), *lol_watcher.league.entries(region[0], queue, "BRONZE", "III"), *lol_watcher.league.entries(region[0], queue, "BRONZE", "IV")]    
            except ApiError as err:
                continue
        elif (rank == 'iron'):
            try:
                players = [*lol_watcher.league.entries(region[0], queue, "IRON", "I"), *lol_watcher.league.entries(region[0], queue, "IRON", "II"), *lol_watcher.league.entries(region[0], queue, "IRON", "III"), *lol_watcher.league.entries(region[0], queue, "IRON", "IV")]
            except ApiError as err:
                continue
        handle_players(region, rank, players)