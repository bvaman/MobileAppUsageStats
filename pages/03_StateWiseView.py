import pandas as pd
import numpy as np
import pydeck as pdk
import streamlit as st
st.set_page_config(layout="wide")

# Markdown , '#' indicates markdown, additional ones reduces text size
st.header('App usage statistics by State' )
st.write(''' 
You can filter on a specific state to view locations where usage was reported.
\nThe interactive map provides a 3D view of the area and hexagon heights indicate locations with higher usage.

*You can slice the data further using the sidebar filters. 

''')


@st.cache
def load_data():
    data = pd.read_csv("data/MobileAppData_Updated.csv")
    data.drop(columns=['StateCd','Dataconntech','Startmarket','Year Month','Daily Session Count','Foregroundduration',
                'Frequency Of Use','Session Duration Minutes'])    
    return data

df=load_data()

st.sidebar.header("App Settings")

age = df['AGE'].unique().tolist()
min_age = int(min(age))
max_age = int(max(age))
value = (min_age, max_age)

# Double sided Age slider 
Model = st.sidebar.slider('Age:',
        min_value=min_age,
        max_value=max_age,
        value=value
        )
selminage, selmaxage = Model

race=['All']
race.extend(df['Ethnicity'].unique().tolist())
sel_race = st.sidebar.multiselect("Select one or more User's Race/Ethnicity:", race,default=["All"])

sel_gender = st.sidebar.multiselect("Select User's Gender:", ["Female","Male"],default=["Female","Male"])


# By State
# StateNm=['All']
# StateNms=df['StateNm'].unique().tolist()
# StateNm.extend(StateNms)

StateNm=df['StateNm'].unique().tolist()
sel_st = st.selectbox("Choose a State for your visualization", StateNm, index=17) # default for NC

## Dataframe filtered on Age range 
df = df.loc[(df['AGE'] >= selminage) & (df['AGE'] <= selmaxage)]

## Dataframe filtered on Gender
df = df[df['Gender'].str.contains('|'.join(sel_gender)).any(level=0)]

if 'All' not in sel_race:
## Dataframe filtered on Race else existing state retained 
    df = df[df['Ethnicity'].str.contains('|'.join(sel_race)).any(level=0)]

if sel_st != 'All':
## Dataframe filtered on State
    df = df.loc[df['StateNm'] == sel_st]

#st.write(df)

# starting point for map 
midpoint = (np.average(df["lat"]), np.average(df["lon"]))

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=5,
        pitch=60,
        bearing=27
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=df,
           get_position='[lon, lat]',
           radius=4500,
           elevation_scale=5,
           elevation_range=[0, 8000],
           #getFillColor=colors,
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            #getFillColor=colors,
            get_radius=4500,
        ),
    ], tooltip={
        'html': '<b>Elevation Value:</b> {colorValue} ',
        'style': {
            'color': 'white'
        }
    }
))

