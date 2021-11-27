from riotwatcher import LolWatcher, ApiError
import json

lol_watcher = LolWatcher('RGAPI-0f6d97b7-8df9-44c0-aedd-44243730acde')

# region = 'euw1'
region = 'na1'
# region = 'kr'


# region_match = 'EUROPE'
region_match = 'AMERICAS'
# region_match = 'ASIA'


queue = "RANKED_SOLO_5x5"
json_file = 'matches.json'

challengers = lol_watcher.league.challenger_by_queue(region, queue)
masters = lol_watcher.league.masters_by_queue(region, queue)
grandmasters = lol_watcher.league.grandmaster_by_queue(region, queue)

players = [*challengers['entries'], *grandmasters['entries'], *masters['entries']]

summoners_puuid = []
i= 0

for player in players:
    i += 1
    summoner = lol_watcher.summoner.by_id(region, player['summonerId'])
    summoners_puuid.append(summoner['puuid'])
    if (i == 20):
        break

matches_id = []

for summoner_puuid in summoners_puuid:
    matches_list = lol_watcher.match.matchlist_by_puuid(region_match, summoner_puuid)
    for match_list in matches_list:
        matches_id.append(match_list)

matches_data = []

for match_id in matches_id:
    print(f'Match found - ID: {match_id}')
    match_data = lol_watcher.match.by_id(region_match, match_id)
    matches_data.append(match_data)

fileVariable = open(json_file, 'r+')
fileVariable.truncate(0)
fileVariable.close()
with open(json_file, 'w') as outfile:
    json.dump(matches_data, outfile)