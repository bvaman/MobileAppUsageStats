import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import plotly.express as px
st.set_page_config(layout="wide")

states = alt.topo_feature(data.us_10m.url, feature='states')

# Markdown , '#' indicates markdown, additional ones reduces text size
st.header('Usage stats through the week' )

st.write(''' 
You can view the usage statistics for different App categories through the week.
Press the play button for an animated view or slide to specific day of the week.

*You can slice the data further using the sidebar filters. 

''')


@st.cache
def load_data():
    data = pd.read_csv("data/MobileAppData_Updated.csv")
    return data

df=load_data()

st.sidebar.header("App Settings")

age = df['AGE'].unique().tolist()
min_age = int(min(age))
max_age = int(max(age))
value = (min_age, 30)

# Double sided Age slider 
Model = st.sidebar.slider('Age:',
        min_value=min_age,
        max_value=max_age,
        value=value
        )
selminage, selmaxage = Model

race=['All']
race.extend(df['Ethnicity'].unique().tolist())
sel_race = st.sidebar.multiselect("Select one or more User's Race/Ethnicity:", race,default=["Black or African American"])

sel_gender = st.sidebar.multiselect("Select User's Gender:", ["Female","Male"],default=["Female","Male"])


## Dataframe filtered on Age range 
df = df.loc[(df['AGE'] >= selminage) & (df['AGE'] <= selmaxage)]

## Dataframe filtered on Gender
df = df[df['Gender'].str.contains('|'.join(sel_gender)).any(level=0)]

if 'All' not in sel_race:
## Dataframe filtered on Race else existing state retained 
    df = df[df['Ethnicity'].str.contains('|'.join(sel_race)).any(level=0)]


st.write("")

# Day of week use
dow_time = df.groupby(['DayofWeek','AppCategory','DAY'])['Daily Time Spent Minutes'].mean().reset_index(name='Avg Time Spent')    
dow_time['Avg Time Spent'] = round(dow_time['Avg Time Spent'])
dow_time=dow_time.sort_values('DAY')

fig = px.bar(dow_time,x='AppCategory',y='Avg Time Spent', color='AppCategory',
        color_discrete_sequence=px.colors.sequential.Blugrn_r,
        animation_frame='DayofWeek', animation_group='AppCategory')

#fig.update_yaxes(range=[0, 150])
fig.update_layout(showlegend=False)
fig.update_layout(width=900)

#fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 0.15
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0.025

st.write(fig)
