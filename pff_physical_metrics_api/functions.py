#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 08:34:12 2023

@author: apschram
"""
import requests
import pandas as pd

def get_competitions(url, key):
    ''' 
    Retrieves information of all competitions available for the given API key.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key

    Returns
    ---------
    
    df: a dataframe containing the competition information
    
    '''
    payload = "{\"query\":\"query competitions {\\n    competitions {\\n        id\\n        name\\n        games {\\n            id\\n            season\\n        }\\n    }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['competitions'])
        return df.infer_objects()
    except:
        print(response.text)
        
def get_teams(url, key):
    ''' 
    Retrieves information of all teams available for the given API key.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key

    Returns
    ---------
    
    df: a dataframe containing the team information
    
    '''
    payload = "{\"query\":\"query teams {\\n    teams {\\n        id\\n        name\\n        shortName\\n        country\\n        homeGames {\\n            id\\n        }\\n        awayGames {\\n            id\\n        }\\n        kits {\\n            id\\n            name\\n            primaryColor\\n            secondaryColor\\n            primaryTextColor\\n            secondaryTextColor\\n        }\\n        homeStadium {\\n            id\\n            name\\n            pitches {\\n                id\\n#                grassType\\n                length\\n                width\\n                startDate\\n                endDate\\n            }\\n        }\\n    }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teams'])
        return df.infer_objects()
    except:
        print(response.text)   

def get_games(url, key, competition_id):
    ''' 
    Retrieves information of all games available in a given competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition

    Returns
    ---------
    
    df: a dataframe containing the game information
    
    '''
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        id\\n        name\\n        games {\\n            id\\n            date\\n            season\\n            week\\n            homeTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            awayTeam {\\n                id\\n                name\\n                shortName\\n            }\\n            startPeriod1\\n            endPeriod1\\n            startPeriod2\\n            endPeriod2\\n            period1\\n            period2\\n            halfPeriod\\n            homeTeamStartLeft\\n            homeTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n            awayTeamKit {\\n                name\\n                primaryColor\\n                primaryTextColor\\n                secondaryColor\\n                secondaryTextColor\\n            }\\n            stadium {\\n                id\\n                name\\n                pitches {\\n                    id\\n#                    grassType\\n                    length\\n                    width\\n                    startDate\\n                    endDate\\n                }\\n            }\\n            videos {\\n                id\\n                fps\\n                videoUrl\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
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

def get_visibility(url, key, competition_id, season):
    ''' 
    Retrieves visibility information per team for all games available in a given competition and season.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition
    season: a string to select the season

    Returns
    ---------
    
    df: a dataframe containing the visibility information
    
    '''
    payload = "{\"query\":\"query {\\n  lowTeamVisibility(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", visibilityThreshold: 100) {\\n    gameId\\n    teamId\\n    teamVisibility\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        df = pd.DataFrame.from_dict(response.json()['data']['lowTeamVisibility'])
        return df.infer_objects()
    except:
        print(response.text)

def get_players_competition(url, key, competition_id):
    ''' 
    Retrieves information of all players available in a given competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition

    Returns
    ---------
    
    df: a dataframe containing the player information
    
    '''
    payload = "{\"query\":\"query competition ($id: ID!) {\\n    competition (id: $id) {\\n        games {\\n            season\\n            rosters {\\n                player {\\n                    id\\n                    firstName\\n                    lastName\\n                    nickname\\n                    positionGroupType\\n                    nationality {\\n                        id\\n                        country\\n                    }\\n                    secondNationality {\\n                        id\\n                        country\\n                    }\\n                    weight\\n                    height\\n                    dob\\n                    gender\\n                    countryOfBirth {\\n                        id\\n                        country\\n                    }\\n                    euMember\\n                    transfermarktPlayerId\\n                }\\n            }\\n        }\\n    }\\n}\",\"variables\":{\"id\":" + str(competition_id) + "}}"
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
        for col in [0,'index','rank']:
            try:
                df = df.drop(columns = [col])
            except:
                continue
        df = df.dropna(how = 'all', axis = 0)
        
        df['id'] = df['id'].astype(int)
        
        return df.infer_objects()
    except:
        print(response.text)

def get_player(url, key, player_id):
    ''' 
    Retrieves information of a player for a given player_id.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    player_id: an integer to select the player

    Returns
    ---------
    
    df: a dataframe containing the player information
    
    '''
    payload = "{\"query\":\"query player ($id: ID!) {\\n    player (id: $id) {\\n        id\\n        firstName\\n        lastName\\n        nickname\\n        positionGroupType\\n        nationality {\\n            id\\n            country\\n        }\\n        secondNationality {\\n            id\\n            country\\n        }\\n        weight\\n        height\\n        dob\\n        gender\\n        countryOfBirth {\\n            id\\n            country\\n        }\\n        euMember\\n        rosters {\\n            game {\\n                id\\n            }\\n            started\\n        }\\n        transfermarktPlayerId\\n    }\\n}\",\"variables\":{\"id\":" + str(player_id) + "}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)
    
    try:
        player_data = response.json()['data']['player']
        second_nationality = player_data['secondNationality']['country'] if player_data['secondNationality'] else None
        player_record = {
            'player_id': player_data['id'],
            'first_name': player_data['firstName'],
            'last_name': player_data['lastName'],
            'dob': player_data['dob'],
            'height': player_data['height'],
            'nickname': player_data['nickname'],
            'position_group': player_data['positionGroupType'],
            'nationality': player_data['nationality']['country'],
            'second_nationality': second_nationality,
            'transfermarkt_id': player_data['transfermarktPlayerId'],
            'rosters': player_data['rosters']  # This will remain a nested list of dicts
        }
        
        df = pd.DataFrame([player_record])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsGameReport(url, key, game_id, clock_filter = ""):
    ''' 
    Retrieves physical metrics per player for a given game.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    game_id: an integer to select the game
    clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only    

    Returns
    ---------
    
    df: a dataframe containing the physical metrics
    
    '''
    payload = "{\"query\":\"query {\\n    physicalMetricsGameReport(gameId: " + str(game_id) + ", clock:\\\"" + str(clock_filter) + "\\\") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n    }\\n  }\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsGameReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPlayerReport(url, key, competition_id, season, player_id, clock_filter = "", vis_filter = 10):
    ''' 
    Retrieves physical metrics per game for players in a given season of a competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition
    season: a string to select the season, e.g. "2022" or "2022-2023"
    player_id: an integer to select the player
    clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only
    vis_filter: an integer to filter out games with low visibilty for a team: 0 for all games, 10 to filter out when teams are below 10% visibility

    Returns
    ---------
    
    df: a dataframe containing the physical metrics
    
    '''
    payload = "{\"query\":\"query {\\n    playerPhysicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", playerId: " + str(player_id) + ", clock: \\\"" + str(clock_filter) + "\\\", teamVis: " + str(vis_filter) + ") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['playerPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsTeamReport(url, key, competition_id, season, teams, clock_filter = "", vis_filter = 10):
    ''' 
    Retrieves aggregated physical metrics for teams in a given season of a competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition
    season: a string to select the season, e.g. "2022" or "2022-2023"
    teams: a list identifiers to select the teams, e.g. [67, 78]
    clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only
    vis_filter: an integer to filter out games with low visibilty for a team: 0 for all games, 10 to filter out when teams are below 10% visibility

    Returns
    ---------
    
    df: a dataframe containing the physical metrics
    
    '''
    payload = "{\"query\":\"query {\\n  teamPhysicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", teams: " + str(teams) + ", clock: \\\"" + str(clock_filter) + "\\\", teamVis: " + str(vis_filter) + ") {\\n    teamId\\n    team\\n    visFramePct\\n    gam\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teamPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPositionReport(url, key, competition_id, season, clock_filter = "", vis_filter = 10):
    ''' 
    Retrieves aggregated physical metrics for players in a given season of a competition.
    
    Parameters
    -----------
    
    url: a string that points toward the API, i.e. 'https://faraday.pff.com/api'
    key: a string that serves as the API key
    competition_id: an integer to select the competition
    season: a string to select the season, e.g. "2022" or "2022-2023"
    clock_filter: a string to select periods of games, e.g. "" for whole games, "00:00 - 15:00" for the first 15 minutes of games only
    vis_filter: an integer to filter out games with low visibilty for a team: 0 for all games, 10 to filter out when teams are below 10% visibility

    Returns
    ---------
    
    df: a dataframe containing the physical metrics
    
    '''
    payload = "{\"query\":\"query {\\n  physicalMetricsReport(competitionId: " + str(competition_id) + ", season: \\\"" + str(season) + "\\\", clock: \\\"" + str(clock_filter) + "\\\", teamVis: " + str(vis_filter) + ") {\\n    playerId\\n    player\\n    shirtNumber\\n    pos\\n    age\\n    teamId\\n    team\\n    visFramePct\\n    str\\n    sub\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)