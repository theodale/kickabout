#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 15:19:07 2021

@author: anirudh
"""

import numpy as np
import pandas as pd
import json

from baseURL import API_ENDPOINTS
from utils import *


def ppg_vs_cost(element_stats, position=None):
    
    
    df = pd.DataFrame(element_stats)
    df = df[['web_name', 'element_type', 'now_cost', 'points_per_game']]
    
    df['now_cost'] = df['now_cost'].apply(lambda x: float(int(x)/10))
    df['points_per_game'] = df['points_per_game'].apply(lambda x: float(x))
    
    if position != None:
        df = df[df['element_type'] == position]
    
    parse = df.to_json(orient='records')
    
    return parse


def ValueForm_vs_SelectionPercent(element_stats, position=None):
    
    df = pd.DataFrame(element_stats)
    df = df[['web_name', 'element_type', 'now_cost', 'minutes', 'value_form', 'selected_by_percent']]
    
    df['value_form'] = df['value_form'].apply(lambda x: float(x))
    df['selected_by_percent'] = df['selected_by_percent'].apply(lambda x: float(x))
    
    if position !=None:
        df = df[df['element_type'] == position]
    
    parse = df.to_json(orient='records')
    
    return json.dumps(parse)
    
    

def top_selects(element_stats, position=None):
    
    df = pd.DataFrame(element_stats)
    
    df = df[['web_name', 'element_type', 'now_cost', 'selected_by_percent']]
    df['selected_by_percent'] = df['selected_by_percent'].apply(lambda x: float(x))
    df = df.sort_values(by='selected_by_percent', ascending=False)
    
    if position == None:
        df = df.head(10)

    else:
        df = df[df['element_type'] == position]
        df = df.head()

    df['element_type'] = df['element_type'].apply(lambda x : elementType_to_PlayerPosition(x))
    
    parse = df.to_json(orient='records')
    
    return json.dumps(parse)
    


def direct_metrics(element_stats, keyword, position= None):
    """ 
    Parameters
    ----------
    element_stats : TYPE: JSON str
        players_data.
    keyword : TYPE, str
        Enter keyword to get top-ranking players in direct metrics.
        
       Keywords ** total_points: total points acculmulated by player this season.
                ** season_form: total_points/value
                ** current_form: gameweek_points/value
                ** yellow_cards: Yellow Card Accumulated this Season
                ** transfers_in: Most transferred in players
                ** ttransferred_out: Most transferred out players
    Returns
    -------
    json structure
    """

    df = pd.DataFrame(element_stats)
    
    df= df[['web_name', 'element_type', 'now_cost', keyword]].sort_values(
        by= keyword, ascending= False).head(20)
    
    if position != None:
        df = df[df['element_type'] == position]
    
    parse = df.to_json(orient='records')
    
    return json.dumps(parse)


if __name__ == '__main__':
    
    static_endpoint = API_ENDPOINTS['static']
    element_stats = get(static_endpoint)['elements']
    
    print(type(ppg_vs_cost(element_stats, position=4)))
    
    