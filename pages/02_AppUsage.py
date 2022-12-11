import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data


#st.markdown("# Page 2 🎉")
#st.sidebar.markdown("# Page 2 🎉")


@st.cache
def load_data():
    data = pd.read_csv("data/MobileAppData_Updated.csv")
    return data

df=load_data()

# Markdown , '#' indicates markdown, additional ones reduces text size
st.header('Popular App Categories')
st.write(''' 
Social media is unsurprisingly the most used app category. 
You can filter on any specific category to view how they compare against the rest.

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
#race= df['Ethnicity'].unique().tolist()
sel_race = st.sidebar.multiselect("Select one or more User's Race/Ethnicity:", race,default=["White"])

sel_gender = st.sidebar.multiselect("Select User's Gender:", ["Female","Male"],default=["Female","Male"])

appctg=['All']
appctgs=df['AppCategory'].unique().tolist()
appctg.extend(appctgs)
#appctg.append('All')

sel_ctg = st.selectbox("*Choose an App Category", appctg)

colors={'Communication':'#A49592', 'Finance':'#727077', 'Games':'#E99787', 'Lifestyle':'#615049', 
        'Music & Audio':'#537072', 'Productivity':'#8E9B97', 'Social Media':'#07575B', 'Sports':'#6EB5B0', 'Video': '#763626'}
scale = alt.Scale(domain=['Communication', 'Finance', 'Games', 'Lifestyle', 'Music & Audio', 'Productivity', 'Social Media', 'Sports', 'Video'],
                  range=['#A49592', '#727077', '#E99787', '#615049', '#537072', '#8E9B97', '#07575B', '#6EB5B0', '#763626'])

#range=['#BC80BD', '#593704', '#0565A6', '#E31A1C', '#FF7F00', '#6A3D9A', '#5CA2D1', '#FDBF6F', '#229A00'])
# range=['#f4d8af', '#dc7027', '#b6c48e', '#ea8a81', '#301008', '#a96762', '#16123f', '#282828', '#666161'])  
#range=['#e7ba52', '#336666', '#aec7e8', '#1f77b4', '#9467bd', '#2b312e', '#c3544b', '#536b7b', '#8d756b'])                  
#'#8199b8', '#a69998', '#95a36f'
#color = alt.Color('AppCategory:N', scale=scale)
#st.write(colors)
#color='#e7ba52'
#st.write("selected color:" )
#st.write(colors[sel_ctg])

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

time_donut=alt.Chart(time_spent).mark_arc(outerRadius=60,innerRadius=30).encode(
        theta=alt.Theta(field="Avg Time Spent", type="quantitative"),
        color=donutcol,
    )
#text = time_donut.mark_text(radius=120, size=10).encode(text="AppCategory")


# Main App Usage chart  
popular_apps = dataf.groupby(['AppCategory','App Title'])['Panelistid'].nunique().reset_index(name='count')
#st.write(popular_apps)

Apps_Chart = alt.Chart(popular_apps).mark_bar().encode(
        x=alt.X('count', title='Number of Sessions'),
        y=alt.Y('App Title:N', sort='-x'),
        #color=alt.Color('App Title:N', legend=None)
        #color=alt.Color('AppCategory:N', legend=None, scale=scale)
        color=colorscheme
    )

#st.altair_chart(time_donut | Apps_Chart, use_container_width=True)

col1, col2 = st.columns([6,4])
with col2:
    st.altair_chart(time_donut, use_container_width=True)

with col1:
    st.altair_chart(Apps_Chart, use_container_width=True)


if sel_ctg != 'All':
## Dataframe filtered on State
    dataf = dataf.loc[dataf['AppCategory'] == sel_ctg]
    
#st.map(dataf)

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
    #color=alt.Color('App Category:N', scale=alt.Scale(scheme='blueorange'))
    color=colorscheme
).project(
    type='albersUsa'
).properties(
    width=900,
    height=600
)

st.altair_chart(background+points, use_container_width=True)