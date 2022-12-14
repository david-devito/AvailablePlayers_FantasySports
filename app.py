import streamlit as st
from pullData import getPlayerLevelData, getPlayerLevelData_IM
from st_aggrid import AgGrid
from getSchedule import getTeamsPlayingOnSelectedDates, getUpcomingMatchups
from st_aggrid.grid_options_builder import GridOptionsBuilder
import datetime

st.set_page_config(layout="wide")

# Scrape Player Info from Yahoo Fantasy League
@st.cache
def getPlayerData(getCurDateForCache):
    playerStatsAndInfo = getPlayerLevelData()
    return playerStatsAndInfo

getCurDateForCache = [datetime.datetime.now().date(),datetime.datetime.now().hour]
playerStatsAndInfo = getPlayerData(getCurDateForCache)

# Add a Title
st.title("TFB")

# Set the default list of dates to select from
default_date_list = [str((datetime.datetime.today() + datetime.timedelta(days=x)).date()) for x in range(7)]
# Selection box for dates
selectedDates = st.multiselect(
    'Select Dates',
    default_date_list)

# Get teams that play on selected dates to populate teams default teams list
defaultTeamsList = getTeamsPlayingOnSelectedDates(selectedDates)

# Selection box for teams
teams = set(sorted(playerStatsAndInfo['Team'].unique()))

curTeam = st.multiselect(
    'Select Teams',
    teams,default=defaultTeamsList)


# Selection box for positions
positions = ['C','LW','RW','D']

curPosition = st.multiselect(
    'Select Positions',
    positions,default=positions)

# Get upcoming matchups for selected teams
try:
    upcomingMatchups = getUpcomingMatchups(curTeam)
    st.dataframe(upcomingMatchups)
except:
    st.title("No Dates and/or Teams Selected")

# Filter player DF based on selections
filteredDF = playerStatsAndInfo[(playerStatsAndInfo['Team'].isin(curTeam)) & (playerStatsAndInfo['Pos'].str.contains('|'.join(curPosition)))]

# Configure Dataframe
gb = GridOptionsBuilder.from_dataframe(filteredDF)
# Freeze player name column
gb.configure_column('Name',pinned=True)
gridOptions = gb.build()
# Sort dataframe by selected column
filteredDF = filteredDF.sort_values(by='Last14', ascending=True)
# Display Dataframe
AgGrid(filteredDF, gridOptions=gridOptions, enable_enterprise_modules=False)




