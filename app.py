import streamlit as st
from pullData import getPlayerLevelData
from st_aggrid import AgGrid
from getSchedule import getTeamsPlayingOnSelectedDates
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(layout="wide")


@st.cache
def getMostAdded():
    playerStatsAndInfo = getPlayerLevelData()
    return playerStatsAndInfo

playerStatsAndInfo = getMostAdded()

st.title("TFB")

teams = set(sorted(playerStatsAndInfo['Team'].unique()))
print(teams)

defaultTeamsList = getTeamsPlayingOnSelectedDates()

curTeam = st.multiselect(
    'Select Teams',
    teams,default=defaultTeamsList)


filteredDF = playerStatsAndInfo[playerStatsAndInfo['Team'].isin(curTeam)]


gb = GridOptionsBuilder.from_dataframe(filteredDF)


gb.configure_column('Name',pinned=True)
gridOptions = gb.build()

AgGrid(filteredDF, gridOptions=gridOptions, enable_enterprise_modules=False)




