#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 08:34:12 2023

@author: apschram
"""
import requests
import pandas as pd

def physicalMetricsGameReport(url, key, game):
    payload = "{\"query\":\"query {\\n    physicalMetricsGameReport(gameId: " + str(game) + ", clock:\\\"\\\") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n    }\\n  }\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsGameReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPlayerReport(url, key, competition, season, player):
    payload = "{\"query\":\"query {\\n    playerPhysicalMetricsReport(competitionId: " + str(competition) + ", season: \\\"" + str(season) + "\\\", playerId: " + str(player) + ") {\\n      playerId\\n      player\\n      shirtNumber\\n      pos\\n      age\\n      teamId\\n      team\\n      gameDate\\n      gam\\n      visFramePct\\n      str\\n      sub\\n      min\\n      tot\\n      spr\\n      hsr\\n      lsr\\n      jog\\n      walk\\n      sprPct\\n      hsrPct\\n      sprt\\n      hsrt\\n      lsrt\\n      jogt\\n      walkt\\n      accel\\n      decel\\n      sprc\\n      hsrc\\n      maxspeed\\n      avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['playerPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsTeamReport(url, key, competition, season, teams):
    payload = "{\"query\":\"query {\\n  teamPhysicalMetricsReport(competitionId: " + str(competition) + ", season: \\\"" + str(season) + "\\\", teams: " + str(teams) + ") {\\n    teamId\\n    team\\n    visFramePct\\n    gam\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['teamPhysicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)

def physicalMetricsPositionReport(url, key, competition, season):
    payload = "{\"query\":\"query {\\n  physicalMetricsReport(competitionId: " + str(competition) + ", season: \\\"" + str(season) + "\\\") {\\n    playerId\\n    player\\n    shirtNumber\\n    pos\\n    age\\n    teamId\\n    team\\n    visFramePct\\n    str\\n    sub\\n    min\\n    tot\\n    spr\\n    hsr\\n    lsr\\n    jog\\n    walk\\n    sprPct\\n    hsrPct\\n    sprt\\n    hsrt\\n    lsrt\\n    jogt\\n    walkt\\n    accel\\n    decel\\n    sprc\\n    hsrc\\n    maxspeed\\n    avgspeed\\n  }\\n}\",\"variables\":{}}"
    response = requests.request("POST", url, headers = {'x-api-key': key, 'Content-Type': 'application/json'}, data = payload)

    try:
        df = pd.DataFrame.from_dict(response.json()['data']['physicalMetricsReport'])
        return df.infer_objects()
    except:
        print(response.text)