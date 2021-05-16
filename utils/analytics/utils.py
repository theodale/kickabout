#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:22:26 2021

@author: anirudh
"""

import requests
import json
from baseURL import *


MIN_GAMEWEEK = 1 
MAX_GAMEWEEK = 38

def get(url):
    response = requests.get(url)
    return json.loads(response.content)



def elementType_to_PlayerPosition(element_type):
    position_dict = {1: "GKP", 
                     2: "DEF", 
                     3: "MID", 
                     4: "FWD"}
    
    return position_dict[element_type]


def playerName_to_id(name=None, player_id=None):
    pass


def last_n_GW(static_endpoint, n):
    
    gameweek_stats = get(static_endpoint)['events']
    
    current_gameweek = int([gw['id'] for gw in gameweek_stats 
                        if gw['is_current'] == True][0])
    
    lastGW = [(gw['id']) for gw in gameweek_stats 
               if gw['id'] in range(current_gameweek-n+1,current_gameweek+1) and gw['id'] >= MIN_GAMEWEEK]
      
    return lastGW



def next_n_GW(static_endpoint, n):
    
    gameweek_stats = get(static_endpoint)['events']
    
    current_gameweek = int([gw['id'] for gw in gameweek_stats 
                        if gw['is_current'] == True][0])
    
    
    nextGW = [(gw['id']) for gw in gameweek_stats 
           if gw['id'] in range(current_gameweek, current_gameweek+n) and gw['id'] <= MIN_GAMEWEEK]
    
    return nextGW



def Players_in_GW(gameweek_endpoint, gameweeks):
    
    PlayersInGW = []
    
    for gameweek in gameweeks:

        url = API_ENDPOINTS['gameweek_stats'].format(gameweek)
        res = get(url)['elements']
        
        players_played = [r['id'] for r in res if r['stats']['minutes'] > 0]
        
        PlayersInGW = [player for player in players_played 
                           if player not in PlayersInGW]
        
    
    return PlayersInGW
        

if __name__ == '__main__':
    
    static_endpoint = API_ENDPOINTS['static']
    fixture_endpoint = API_ENDPOINTS['fixtures']
    gameweek_endpoint = API_ENDPOINTS['gameweek_stats']
    
    cgw = Players_in_GW(gameweek_endpoint, [28,29])