#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Apr  7 18:30:54 2021

@author: anirudh
"""

import numpy as np
import pandas as pd
import json

from baseURL import API_ENDPOINTS
from utils import get


def get_teams(team_id= None, teamDict=None):
    
    if teamDict == None:
        static_endpoint = API_ENDPOINTS['static']
        teams = get(static_endpoint)['teams']
        
        dictTeam = {team['id']: team['name'] for team in teams} 
    
    if team_id == None :
        return dictTeam
    
    else: 
        return dictTeam[team_id]


def fixture_difficulty(team_id, fixtures):
    
    # fixture_endpoint = API_ENDPOINTS['fixtures']
    # fixtures = get(fixture_endpoint)
    
    fixtures = [fixture for fixture in fixtures 
                if (fixture['finished']==False and (fixture['team_h']==team_id or fixture['team_a']==team_id))]
    
    fixture_difficulty_list = []
    opposition = []
    event = []
    
    if len(fixtures) > 5:
        fixtures = fixtures[:5]
    
    for fixture in fixtures:
        if fixture['team_h']==team_id:
            fixture_difficulty_list.append(fixture['team_h_difficulty'])
            opposition.append(fixture['team_a'])
            event.append(fixture['event'])

           
        elif fixture['team_a']==team_id:
            fixture_difficulty_list.append(fixture['team_a_difficulty'])
            opposition.append(fixture['team_h'])
            event.append(fixture['event'])

    
    meanFDR = np.mean(fixture_difficulty_list)
    
    FDTable = {"team_id": team_id, "opposition": opposition, 
               "difficulty":fixture_difficulty_list}

    return json.dumps(FDTable)


def total_points_accumulated(team_id, element_stats):
    
    # static_endpoint = API_ENDPOINTS['static']
    # element_stats = get(static_endpoint)['elements']
    
    team_points = [float(element['total_points']) for element in element_stats 
                     if element['team'] == team_id]
    

    total_points = np.sum(team_points)
    
    return json.dumps({"team_id":team_id, "points":total_points})



def top_picks(team_id, element_stats):
    
    # static_endpoint = API_ENDPOINTS['static']
    # element_stats = get(static_endpoint)['elements']
    
    players_picked = [element for element in element_stats 
                     if element['team'] == team_id]
    
    player_df = pd.DataFrame(players_picked)
    player_df = player_df[['id', 'web_name', 'selected_by_percent']]
    
    player_df = player_df.sort_values('selected_by_percent', ascending=False).head().to_json(orient='records')
    parsed = json.loads(player_df)
    
    return json.dumps(parsed)
    

def performance_HomeAway(team_id, fixtures):
    
    fixtures_finished = [fixture for fixture in fixtures if fixture['finished']==True]
    
    fixtures_home = [fixture for fixture in fixtures_finished if fixture['team_h']==team_id]
    
    fixtures_away = [fixture for fixture in fixtures_finished if fixture['team_a']==team_id]
    
    
    n_fixtures_home = len(fixtures_home)
    n_fixtures_away = len(fixtures_away)
    
    home_wins = 0
    away_wins = 0
    
    for fixture in fixtures_finished:
        if (fixture['team_h'] == team_id and 
            (fixture['team_h_score'] > fixture['team_a_score'])) :
            home_wins = home_wins + 1
        
        if(fixture['team_a'] == team_id and 
            (fixture['team_h_score'] < fixture['team_a_score'])):
            away_wins = away_wins + 1
        

    performance = {'team_id': str(team_id), 
                   "fixtures_home":str(n_fixtures_home), "fixtures_away":str(n_fixtures_away), 
                   "home_wins": str(home_wins), "away_wins": str(away_wins)}
    
    return json.dumps(performance)


if __name__ == '__main__':
    
    static_endpoint = API_ENDPOINTS['static']
    fixture_endpoint = API_ENDPOINTS['fixtures']
    
    fixtures = get(fixture_endpoint)
    element_stats = get(static_endpoint)['elements']
    
    teamsDict = get_teams()

    
    HomeAway=[]
    FDR=[]
    TotalPoints = []
    TopPicks = []
    for team_id in teamsDict.keys():
        
        HomeAway.append(performance_HomeAway(team_id, fixtures))
        TotalPoints.append(total_points_accumulated(team_id, element_stats))
        TopPicks.append(top_picks(team_id, element_stats))
        FDR.append(fixture_difficulty(team_id, fixtures))
    
    TeamStats = json.dumps({"Strength": HomeAway, 
                            "Points": TotalPoints,
                            "TopSelection": TopPicks,
                            "FixtureDifficulty": FDR}, indent=4)
    
        
    
