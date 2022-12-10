#import required packages to get data
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd



def pullDataFromYahoo():

    def list_to_name(list):
        """Converts a list to a name."""
        x = ''.join(list)
        return x

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


    #create empty list
    most_added = []
    #relevantTeams = ['NYI','NJ']

    for counti in [0,25,50,75,100,125]:


        url = f'https://hockey.fantasysports.yahoo.com/hockey/37348/players?status=A&pos=P&cut_type=33&stat1=S_S_2022&myteam=0&sort=AR&sdir=1&count={str(counti)}'
        page_content= requests.get(url).text
        soup = BeautifulSoup(''.join(page_content), "lxml")
        
        

        for tables in soup.find_all('tbody'):
        #scrape all rows from the table individually
            for row in tables.find_all('tr'):
            
        #strip the html down to what we need
                detail = (row.get_text(strip=True, separator='|').split('|'))
        
        #clean up noise in the table
                if detail[1] == 'New Player Note' or detail[1] == 'Player Note' or detail[1] == 'No new player Notes' and len(detail) > 3:
        #create a temporary list to append to our empty list
        #the detail comes through in different lengths, so taking items 1,2 #then 4,3,2,1 from the right of each list gives us the data we want #to standardize
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
        #append temp list to our most_added list
                    
                    #if teamName in relevantTeams:
                    
                    most_added.append(temp)
                else:
                    next
        
        
    most_added = pd.DataFrame(most_added)
    most_added.columns = ['Name','Team','Pos','Status','G','A','+/-','PPP','SOG','Hits']


    return most_added


