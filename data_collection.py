import requests
import pandas as pd

api_key = "RGAPI-c5e744ba-2a89-424b-a66a-807fea83c360"

grandmaster = 'https://euw1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=' + api_key

data = requests.get(grandmaster)
league_df = pd.DataFrame(data.json())

league_df.reset_index(inplace=True)
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T 
league_df = pd.concat([league_df, league_entries_df], axis=1)
league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df.info()

for i in range(len(league_df)):
    # if (i > 3): 
    #     break
    try:
        request_url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + league_df['summonerId'].iloc[i] + '?api_key=' + api_key 
        print(request_url)
        r = requests.get(request_url)
            
        while r.status_code == 429:
            request_url = 'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + league_df['summonerId'].iloc[i] + '?api_key=' + api_key 
            r = requests.get(request_url)
            
        # account_id = r.json()['summonerId']
        # league_df.iloc[i, -1] = account_id
    except:
        pass


league_df.to_csv('test.csv',index=False)