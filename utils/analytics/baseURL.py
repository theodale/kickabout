#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 12:29:20 2021

@author: anirudh
"""
BASE_URL = 'https://fantasy.premierleague.com/api/'


API_ENDPOINTS = {
        'static': "{}bootstrap-static/".format(BASE_URL),
        'fixtures': "{}fixtures/".format(BASE_URL),
        'player_stats':"{}element-summary/".format(BASE_URL),
        'gameweek_stats':'{}event/{}/live/'.format(BASE_URL, '{}'),
        'individual_player': "{}element-summary/{}/".format(BASE_URL, '{}')
        }