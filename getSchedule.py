import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta





def getTeamsPlayingOnSelectedDates():
    
    teamAbbrevDict = {'Anaheim Ducks':'ANA',
     'Arizona Coyotes':'ARI',
     'Boston Bruins':'BOS',
     'Buffalo Sabres':'BUF',
     'Calgary Flames':'CGY',
     'Carolina Hurricanes':'CAR',
     'Chicago Blackhawks':'CHI',
     'Colorado Avalanche':'COL',
     'Columbus Blue Jackets':'CBJ',
     'Dallas Stars':'DAL',
     'Detroit Red Wings':'DET',
     'Edmonton Oilers':'EDM',
     'Florida Panthers':'FLA',
     'Los Angeles Kings':'LA',
     'Minnesota Wild':'MIN',
     'Montreal Canadiens':'MTL',
     'Nashville Predators':'NSH',
     'New Jersey Devils':'NJ',
     'New York Islanders':'NYI',
     'New York Rangers':'NYR',
     'Ottawa Senators':'OTT',
     'Philadelphia Flyers':'PHI',
     'Pittsburgh Penguins':'PIT',
     'San Jose Sharks':'SEA',
     'Seattle Kraken':'SJ',
     'St. Louis Blues':'STL',
     'Tampa Bay Lightning':'TB',
     'Toronto Maple Leafs':'TOR',
     'Vancouver Canucks':'VAN',
     'Vegas Golden Knights':'VGK',
     'Washington Capitals':'WPG',
     'Winnipeg Jets':'WSH'}
    
    

    schedDF = pd.read_csv('2022_2023_NHL_Schedule.csv', header=None)
    schedDF.columns = ['Date','Time','Away','Home']
    schedDF['Home'].unique()
    
    curDate = str(dt.datetime.now().date())
    
    
    curDF = schedDF[schedDF['Date'].isin([curDate,str(pd.to_datetime(curDate).date()+timedelta(1))])]
    
    curDatesTeamList = list(curDF['Away']) + list(curDF['Home'])
    
    import collections
    playOnSelectedDates = [item for item, count in collections.Counter(curDatesTeamList).items() if count > 1]
    
    playOnSelectedDates = [teamAbbrevDict[x] for x in playOnSelectedDates]
    return playOnSelectedDates



