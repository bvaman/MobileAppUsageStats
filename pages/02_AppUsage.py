import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
st.set_page_config(layout="wide")

#st.markdown("# Page 2 🎉")
#st.sidebar.markdown("# Page 2 🎉")


@st.cache
def load_data():
    data = pd.read_csv("data/MobileAppData_Updated.csv")
    data.drop(columns=['StateCd','Dataconntech','Startmarket','Year Month','Daily Session Count','Foregroundduration',
                'Frequency Of Use','Session Duration Minutes'])
    return data

df=load_data()

# Markdown , '#' indicates markdown, additional ones reduces text size
st.header('Popular App Categories')
st.write(''' 
Social media is the most used app category across all age groups and enthnicities.  
\nYou can filter on any specific category to view how they compare against the rest.

You can slice the data further using the sidebar filters. 

''')


st.sidebar.header("Filter the dataset here ")

age = df['AGE'].unique().tolist()
min_age = int(min(age))
max_age = int(max(age))
value = (min_age, 30)

# Double sided Age slider 
Model = st.sidebar.slider('Age Range:',
        min_value=min_age,
        max_value=max_age,
        value=value
        )
selminage, selmaxage = Model

race=['All']
race.extend(df['Ethnicity'].unique().tolist())
sel_race = st.sidebar.multiselect("Select one or more User's Race/Ethnicity:", race,default=["Black or African American"])

sel_gender = st.sidebar.multiselect("Select User's Gender:", ["Female","Male"],default=["Female","Male"])

appctg=['All']
appctgs=df['AppCategory'].unique().tolist()
appctg.extend(appctgs)
#appctg.append('All')

sel_ctg = st.selectbox("*Choose an App Category", appctg)

colors={'Communication':'#006C84', 'Finance':'#66A5AD', 'Games':'#E99787', 'Lifestyle':'#615049', 
        'Music & Audio':'#537072', 'Productivity':'#8E9B97', 'Social Media':'#07575B', 'Sports':'#6EB5B0', 'Video': '#763626'}
scale = alt.Scale(domain=['Communication', 'Finance', 'Games', 'Lifestyle', 'Music & Audio', 'Productivity', 'Social Media', 'Sports', 'Video'],
                  range=['#006C84', '#66A5AD', '#E99787', '#615049', '#537072', '#8E9B97', '#07575B', '#6EB5B0', '#763626'])

if sel_ctg=='All':
    colorscheme=alt.Color('AppCategory:N',legend=None, scale=scale)
    donutcol=alt.Color('AppCategory:N', scale=scale)
else:
    colorscheme=alt.condition(
            alt.datum.AppCategory == sel_ctg,
            alt.value(colors[sel_ctg]),
            alt.value('lightgrey') )     
    donutcol=colorscheme

## Dataframe filtered on Age range 
dfres = df.loc[(df['AGE'] >= selminage) & (df['AGE'] <= selmaxage)]

## Dataframe filtered on Gender
dataf = dfres[dfres['Gender'].str.contains('|'.join(sel_gender)).any(level=0)]

if 'All' not in sel_race:
## Dataframe filtered on Race else existing state retained 
    dataf = dataf[dataf['Ethnicity'].str.contains('|'.join(sel_race)).any(level=0)]

# Avg Time spent on Apps 
time_spent = dataf.groupby(['AppCategory'])['Daily Time Spent Minutes'].mean().reset_index(name='Avg Time Spent')
time_spent['Avg Time Spent'] = round(time_spent['Avg Time Spent'])

time_donut=alt.Chart(time_spent).mark_arc(outerRadius=90,innerRadius=50).encode(
        theta=alt.Theta(field="Avg Time Spent", type="quantitative"),
        color=donutcol,
        tooltip=['Avg Time Spent']        
    ).properties(title='Average Time Spent (Mins)'
    ).configure_title(
        fontSize=15,
        font='Sans serif',
        anchor='middle'
    )

# Main App Usage chart  
popular_apps = dataf.groupby(['AppCategory','App Title'])['Panelistid'].nunique().reset_index(name='count')
#st.write(popular_apps)

Apps_Chart = alt.Chart(popular_apps).mark_bar().encode(
        x=alt.X('count', title='Number of Sessions'),
        y=alt.Y('App Title:N', sort='-x'),
        color=colorscheme
    )

col1, col2 = st.columns([6,4])
with col2:
    st.altair_chart(time_donut, use_container_width=True)

with col1:
    st.altair_chart(Apps_Chart, use_container_width=True)


if sel_ctg != 'All':
## Dataframe filtered on State
    dataf = dataf.loc[dataf['AppCategory'] == sel_ctg]

#Map
# US states background
states = alt.topo_feature(data.us_10m.url, feature='states')
background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=900,
    height=600
).project(type='albersUsa')

points=alt.Chart(dataf).mark_circle(size=8).encode(
    longitude='lon:Q',
    latitude='lat:Q',
    color=colorscheme,
    tooltip=['AppCategory:N','App Title:N']
).project(
    type='albersUsa'
).properties(
    width=900,
    height=600
)

st.altair_chart(background+points, use_container_width=True)