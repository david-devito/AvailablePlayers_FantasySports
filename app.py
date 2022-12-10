import streamlit as st
from pullData import pullDataFromYahoo
from st_aggrid import AgGrid
from getSchedule import getTeamsPlayingOnSelectedDates
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(layout="wide")


@st.cache
def getMostAdded():
    most_added = pullDataFromYahoo()
    return most_added

most_added = getMostAdded()

print(most_added)

st.title("TFB")

teams = set(most_added['Team'].unique())
print(sorted(teams))

#x = st.selectbox("Team", teams)

defaultTeamsList = getTeamsPlayingOnSelectedDates()

curTeam = st.multiselect(
    'Select Teams',
    teams,default=defaultTeamsList)


filteredDF = most_added[most_added['Team'].isin(curTeam)]


gb = GridOptionsBuilder.from_dataframe(filteredDF)


gb.configure_column('Name',pinned=True)
gridOptions = gb.build()

AgGrid(filteredDF, gridOptions=gridOptions, enable_enterprise_modules=True)




