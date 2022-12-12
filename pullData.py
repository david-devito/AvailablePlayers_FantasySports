#import required packages to get data
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getPlayerLevelData():
    
    # Making name data readable
    def list_to_name(list):
        """Converts a list to a name."""
        x = ''.join(list)
        return x
    
    # Making name data readable
    def remove_non_ascii(text):
        """Removes non-ascii text and returns english vowel or blank in their place."""
        temp = []
        for i in text:
            if ord(i) < 128:
                temp.append(i)
            elif ord(i) in [232,233,234,235]:
                temp.append('e')
            elif ord(i) in [224,225,226,227,228,229]:
                temp.append('a')
            elif ord(i) in [236,237,238,239]:
                temp.append('i')
            elif ord(i) in [242,243,244,245,246]:
                temp.append('o')
            elif ord(i) == 241:
                temp.append('n')
            else:
                temp.append(' ')
        return temp
    
    
    
    # Pull Season-Level Data
    def getFullSeasonData():
    
        fullSeason = []
    
        for counti in [0,25,50,75,100,125]:
    
    
            url = f'https://hockey.fantasysports.yahoo.com/hockey/37348/players?status=A&pos=P&cut_type=33&stat1=S_S_2022&myteam=0&sort=AR&sdir=1&count={str(counti)}'
            page_content= requests.get(url).text
            soup = BeautifulSoup(''.join(page_content), "lxml")
            
            
    
            for tables in soup.find_all('tbody'):
    
                for row in tables.find_all('tr'):
                    detail = (row.get_text(strip=True, separator='|').split('|'))
    
                    if detail[1] == 'New Player Note' or detail[1] == 'Player Note' or detail[1] == 'No new player Notes' and len(detail) > 3:
                        playerName = detail[2]
                        teamName = detail[3].split(' - ')[0]
                        playerpos = detail[3].split(' - ')[1]
                        
                        if 'FA' in detail:
                            faOrWaivers = 'FA'
                        else:
                            faOrWaivers = 'W'
                        
                        
                        goals = detail[-6]
                        assists = detail[-5]
                        plusminus = detail[-4]
                        ppp = detail[-3]
                        sog = detail[-2]
                        hits = detail[-1]
                        
                        temp = [list_to_name(remove_non_ascii(playerName)),teamName,playerpos,faOrWaivers,goals,assists,plusminus,ppp,sog,hits]
                        
                        fullSeason.append(temp)
                    else:
                        next
            
            
        fullSeason = pd.DataFrame(fullSeason)
        fullSeason.columns = ['Name','Team','Pos','Status','G','A','+/-','PPP','SOG','Hits']
    
    
        return fullSeason
    
    fullSeason = getFullSeasonData()
    
    
    # Pull Last-14 Data and Last-7 Data
    def getLast14Data():
    
        last14 = []
        
        for counti in [0,25,50,75,100,125]:
            
            url = f'https://hockey.fantasysports.yahoo.com/hockey/37348/players?status=A&pos=P&cut_type=33&stat1=K_K&myteam=0&sort=AR_L14&sdir=1&count={str(counti)}'
            page_content= requests.get(url).text
            soup = BeautifulSoup(''.join(page_content), "lxml")
            
            
        
            for tables in soup.find_all('tbody'):
        
                for row in tables.find_all('tr'):
                    detail = (row.get_text(strip=True, separator='|').split('|'))
        
                    if detail[1] == 'New Player Note' or detail[1] == 'Player Note' or detail[1] == 'No new player Notes' and len(detail) > 3:
                        playerName = detail[2]
                        
                        last14rank = detail[-2]
                        last7rank = detail[-1]
                        
                        temp = [list_to_name(remove_non_ascii(playerName)),last7rank,last14rank]
                        
                        last14.append(temp)
                    else:
                        next
            
            
        last14 = pd.DataFrame(last14)
        last14.columns = ['Name','Last7','Last14']
        
        return last14
        
    last14 = getLast14Data()
        
    fullStatsDF = pd.merge(fullSeason,last14,on='Name',how='left')
    
    
    # Pull Transaction Data
    def getTransactionData():
    
        adds = []
        
        for counti in [0,25,50,75,100,125]:
            
            url = f'https://hockey.fantasysports.yahoo.com/hockey/37348/players?status=A&pos=P&cut_type=33&stat1=R_R&myteam=0&sort=BI_A&sdir=1&count={str(counti)}'
            page_content= requests.get(url).text
            soup = BeautifulSoup(''.join(page_content), "lxml")
            
            
        
            for tables in soup.find_all('tbody'):
        
                for row in tables.find_all('tr'):
                    detail = (row.get_text(strip=True, separator='|').split('|'))
        
                    if detail[1] == 'New Player Note' or detail[1] == 'Player Note' or detail[1] == 'No new player Notes' and len(detail) > 3:
                        playerName = detail[2]
                        
                        recentadds = detail[-6]
                        
                        temp = [list_to_name(remove_non_ascii(playerName)),recentadds]
                        
                        adds.append(temp)
                    else:
                        next
            
            
        adds = pd.DataFrame(adds)
        adds.columns = ['Name','Adds']
        
        return adds
        
    adds = getTransactionData()
        
    fullStatsDF = pd.merge(fullStatsDF,adds,on='Name',how='left')
    
    
    
    fullStatsDF = fullStatsDF[['Name','Team','Pos','Status','Adds','Last7','Last14','G','A','+/-','PPP','SOG','Hits']]
    
    fullStatsDF = fullStatsDF.sort_values(by='Last14', ascending=True)

    return fullStatsDF











