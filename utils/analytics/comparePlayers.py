#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 21:24:40 2021

@author: anirudh
"""
import pandas as pd
from baseURL import API_ENDPOINTS
from utils import *


def PlayerInfo(player_id, element_stats):
    
    info = ['id','web_name', 'now_cost', 'selected_by_percent', 'status', 'total_points']
    stats = [element for element in element_stats if element['id'] == player_id][0]
    
    stats = {key: stats[key] for key in info}
    
    return stats


def PlayerStats(player_id):
   
    player_endpoint = API_ENDPOINTS['individual_player'].format(player_id)
    player_stats = get(player_endpoint)
    
    upcoming_fixtures = player_stats['fixtures']
    fixture_stats = player_stats['history']
    past_seasons = player_stats['history_past']

    points_home = 0
    points_away = 0
    cumulative_points = [0]
    cost = []
    ict = []
    
    for match in fixture_stats:
        
        cumulative_points.append(cumulative_points[-1]+ match['total_points'])
        
        if match['was_home'] == True:
            points_home += match['total_points']
            
            
        if match['was_home'] == False:
            points_away += match['total_points']

        cost.append(match['value'])
        ict.append(match['ict_index'])
        
    
    percent_points_home = round((float(points_home)/float(cumulative_points[-1]))*100,1)
    percent_points_away = round((float(points_away)/float(cumulative_points[-1]))*100,1)
    
    stats = {"percent_points_home":percent_points_home,  
             "percent_points_away": percent_points_away,
             "cumulative_points": cumulative_points[1:], 
             "cost": cost, "ict_index": ict}
    
    return stats


def getPlayerStats(player_id, element_stats):
    
    info = PlayerInfo(player_id, element_stats)
    stats = PlayerStats(player_id)
    
    statistics = info.copy()
    statistics.update(stats)
    
    return json.dumps(statistics)


if __name__ == '__main__':
    
    player_id = 9
    player_endpoint = API_ENDPOINTS['individual_player'].format(player_id)
    
    static_endpoint = API_ENDPOINTS['static']
    element_stats = get(static_endpoint)['elements']
    
    ans = getPlayerStats(player_id, element_stats)
