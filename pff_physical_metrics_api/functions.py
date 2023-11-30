#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 08:34:12 2023

@author: apschram
"""
import requests
import pandas as pd

def get_competitions(url, key):
    payload = "{\"query\":\"query competitions {\\n    competitions {\\n        id\\n        name\\n        games {\\n            id\\n            season\\n        }\\n    }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['competitions'])
        return df.infer_objects()
    except:
        print(response.text)
        
def get_teams(url, key):
    payload = "{\"query\":\"query teams {\\n    teams {\\n        id\\n        name\\n        shortName\\n        country\\n        homeGames {\\n            id\\n        }\\n        awayGames {\\n            id\\n        }\\n    }\\n}\",\"variables\":{}}"    
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teams'])
        return df.infer_objects()
    except:
        print(response.text)   

def get_games(url, key, competition_id):
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        id\\n        name\\n        games {\\n            id\\n            date\\n            season\\n            week\\n            homeTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            awayTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            startPeriod1\\n            endPeriod1\\n            startPeriod2\\n            endPeriod2\\n            period1\\n            period2\\n            halfPeriod\\n            homeTeamStartLeft\\n            homeTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n            awayTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['competition']['games'])
        
        competition = pd.DataFrame(index = df.index)
        competition.loc[:,'id'] = response.json()['data']['competition']['id']
        competition.loc[:,'name'] = response.json()['data']['competition']['name']
        competition['competition'] = competition[['id','name']].to_dict(orient = 'records')
        
        df = df.merge(competition[['competition']], how = 'left', left_index = True, right_index = True)
        df = df.reindex(sorted(df.columns), axis = 1).infer_objects()
        return df.infer_objects()
    except:
        print(response.text)

def get_players_competition(url, key, competition_id):
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        games {\\n            rosters {\\n                player {\\n                    id\\n                    firstName\\n                    lastName\\n                    nickname\\n                    positionGroupType\\n                    nationality {\\n                        id\\n                        country\\n                    }\\n                    secondNationality {\\n                        id\\n                        country\\n                    }\\n                    weight\\n                    height\\n                    dob\\n                    gender\\n                    countryOfBirth {\\n                        id\\n                        country\\n                    }\\n                    euMember\\n                }\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame(response.json()['data']['competition']['games'])
        df = df['rosters'].apply(pd.Series)
        df = df.dropna(how = 'all', axis = 0)
        
        oneCol = []
        colLength = len(list(df.columns))
        for k in range(colLength):
            oneCol.append(df[k])
        
        df = pd.concat(oneCol, ignore_index = True)
        df = df.apply(pd.Series)['player'].apply(pd.Series)
        
        df = df.reset_index(drop = False)
        df['rank'] = df.groupby('id')['index'].rank('dense', ascending = False)
        df = df[df['rank'] == 1]
        # df = df.drop_duplicates()
        df = df.drop(columns = [0,'index','rank'])
        df = df.dropna(how = 'all', axis = 0)
        
        df['id'] = df['id'].astype(int)
        
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsGameReport(url, key, game_id):
    payload = "{\"query\":\"query {\\n    physicalMetricsGameReport(gameId: " + str(game_id) + ", clock:\\\"\\\") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n    }\\n  }\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsGameReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPlayerReport(url, key, competition_id, season, player_id):
    payload = "{\"query\":\"query {\\n    playerPhysicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", playerId: " + str(player_id) + ") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['playerPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsTeamReport(url, key, competition_id, season, teams):
    payload = "{\"query\":\"query {\\n  teamPhysicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", teams: " + str(teams) + ") {\\n    teamId\\n    team\\n    visFramePct\\n    gam\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teamPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPositionReport(url, key, competition_id, season):
    payload = "{\"query\":\"query {\\n  physicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\") {\\n    playerId\\n    player\\n    shirtNumber\\n    pos\\n    age\\n    teamId\\n    team\\n    visFramePct\\n    str\\n    sub\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)