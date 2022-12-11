#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:23:02 2018

@author: daviddevito
"""

import requests
from bs4 import BeautifulSoup
import re
import sys

teamName = ["anaheim-ducks","arizona-coyotes","boston-bruins","buffalo-sabres","calgary-flames","carolina-hurricanes","chicago-blackhawks","colorado-avalanche","columbus-blue-jackets","dallas-stars","detroit-red-wings","edmonton-oilers","florida-panthers","los-angeles-kings","minnesota-wild","montreal-canadiens","nashville-predators","new-jersey-devils","new-york-islanders","new-york-rangers","ottawa-senators","philadelphia-flyers","pittsburgh-penguins","san-jose-sharks","st-louis-blues","tampa-bay-lightning","toronto-maple-leafs","vancouver-canucks","vegas-golden-knights","washington-capitals","winnipeg-jets"]
#teamName = input("Enter the team to run: ")

allDFOData = []
for k in range(0,len(teamName)):
    print(teamName[k])
    
    url = "https://www.dailyfaceoff.com/teams/" + teamName[k] + "/line-combinations/stats/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(r.content,"lxml")
    
    
    name_data = soup.find_all("a", {"class": "player-link"})
    '''
    for i in range(0,30):
    
        name = str(name_data[i].img["alt"])
    
        if i in [0,1,2]: lineVar = 'L1'
        elif i in [3,4,5]: lineVar = 'L2'
        elif i in [6,7,8]: lineVar = 'L3'
        elif i in [9,10,11]: lineVar = 'L4'
        elif i in [12,13]: lineVar = 'D1'
        elif i in [14,15]: lineVar = 'D2'
        elif i in [16,17]: lineVar = 'D3'
        elif i in [18,19,20,21,22]: lineVar = 'PP1'
        elif i in [23,24,25,26,27]: lineVar = 'PP2'
        else: lineVar = ''
        '''
        
        
    playerNames = [str(name_data[x].img["alt"]) for x in range(0,28)]
    lineList = (['L1'] * 3) + (['L2'] * 3) + (['L3'] * 3) + (['L4'] * 3) + (['D1'] * 2) + (['D2'] * 2) + (['D3'] * 2) + (['PP1'] * 5) + (['PP2'] * 5)
    
        
    teamsPlayerInfo = [[i, j] for i, j in zip(playerNames, lineList)]
        
    allDFOData.extend(teamsPlayerInfo)
        
        
        
    #allDFOData.append([name,lineVar])
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    