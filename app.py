import streamlit as st
from pullData import getPlayerLevelData
from st_aggrid import AgGrid
from getSchedule import getTeamsPlayingOnSelectedDates, getUpcomingMatchups
from st_aggrid.grid_options_builder import GridOptionsBuilder
import datetime

st.set_page_config(layout="wide")

# Scrape Player Info from Yahoo
@st.cache
def getMostAdded():
    playerStatsAndInfo = getPlayerLevelData()
    return playerStatsAndInfo

playerStatsAndInfo = getMostAdded()

# Add a Title
st.title("TFB")

# Get the default list of dates to select from
default_date_list = [str((datetime.datetime.today() + datetime.timedelta(days=x)).date()) for x in range(7)]
# Selection box for dates
selectedDates = st.multiselect(
    'Select Dates',
    default_date_list)

# Get teams that play on selected dates to populate teams list
defaultTeamsList = getTeamsPlayingOnSelectedDates(selectedDates)

# Selection box for teams
teams = set(sorted(playerStatsAndInfo['Team'].unique()))

curTeam = st.multiselect(
    'Select Teams',
    teams,default=defaultTeamsList)



positions = ['C','LW','RW','D']

curPosition = st.multiselect(
    'Select Positions',
    positions,default=positions)


upcomingMatchups = getUpcomingMatchups(curTeam)

st.dataframe(upcomingMatchups)

# Filter player DF based on selections
filteredDF = playerStatsAndInfo[(playerStatsAndInfo['Team'].isin(curTeam)) & (playerStatsAndInfo['Pos'].str.contains('|'.join(curPosition)))]

# Configure and display Dataframe
gb = GridOptionsBuilder.from_dataframe(filteredDF)
# Freeze player name column
gb.configure_column('Name',pinned=True)
gridOptions = gb.build()
AgGrid(filteredDF, gridOptions=gridOptions, enable_enterprise_modules=False)




