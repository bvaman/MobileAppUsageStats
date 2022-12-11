import streamlit as st
import pandas as pd

col1,col2 = st.columns(([2,8]))
with col1:
    st.image('images/app1.jpg',use_column_width=True)

st.header("Mobile App Usage Statistics")

#if 'base' not in st.session_state:
#    st.session_state.base = pd.read_csv("data/MobileAppData_Updated.csv")

#st.write(st.session_state.base.count())


    
st.write(
'''
This dataset from the Snowflake Marketplace contains GWS’s proprietary OneMeasure Consumer Panel (OMCP) data about mobile app usage statistics.
They offer continuous monitoring, collection and reporting of mobile consumer behavior for hundreds of thousands of apps. The actively curated opt-in panel is composed of tens of thousands adult mobile users and its composition demographically reflects the US population.


The sample dataset used here contains a week's worth of usage behavior for around 21K users.

* The exploratory data analysis presented in this app aims to 
    * Porfile popular App Categories across various age groups, gender and ethnicities.
    * Explore usage statistics through the week.
    * The availability of geo-spatial attributes also provides the ability to view State/Region specific usage statistics.

' ' 

* Some business needs that could possibly be addressed with a complete dataset - 
    * Audience Segmentation - Profile popular gaming app users by gender, age and income level for better ad targets
    * Foot Traffic Analytics - Foot traffic analysis for any kind of business: Brick and Mortar retailers or restaurants.
    * Risk Analysis - Analyze user behavior to pre-emptively identify potential for usage fade-away and churn for streaming services
    * Quantitative Analysis - Threat posed by the rise of Neo and Challenger banks to traditional Banks
    * Accelerating Advertising Revenue - Analyze the rise and predict future trends of breakout apps in the financial space like Robinhood, Coinbase, Acorns and Stash.

'''
)