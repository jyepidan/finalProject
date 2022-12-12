from distutils.command.bdist import show_formats
from json.tool import main
from turtle import color, title, width
from unicodedata import name
import streamlit as st
import pandas as pd
import altair as alt
import numpy as mp
import seaborn as sns
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

df = pd.read_csv(
    '/Users/joasyepidan/Documents/Fall2022/VisualAnalytics-5122/5122_sl/data/police_shooting.csv')
# clean data
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df['age'] = df['age'].astype('int')

st.sidebar.title("OUTLINE")

st.header("US Police Shootings")


def main_page():
    st.subheader("Home page 🎈")
    st.write("US Police Shootings on People from 2015-2022. This dataset was found on kaggle official website  website https://data.charlottenc.gov/datasets/charlotte::officer-traffic-stops/explore")

    tab1, tab2, tab3 = st.tabs(['Description', 'View Dataset', 'Statistics'])
    with tab1:
        st.header("Description")
        text = ''' Although Congress instructed the Attorney General in 1994 to compile and publish annual statistics 
        on police use of excessive force, this was never carried out, and the Federal Bureau of Investigation does not collect these data. 
        The annual average number of justifiable homicides alone was previously estimated to be near 400. 
        Updated estimates from the Bureau of Justice Statistics released in 2015 estimate the number to be around 930 per year, 
        or 1,240 if assuming that non-reporting local agencies kill people at the same rate as reporting agencies.A 2019 study by Esposito, Lee, and Edwards 
        states that police killings are a leading cause of death for men aged 25–29 at 1.8 per 100000, trailing causes such as accidental death (76.6 per 100000), suicide (26.7 per 100000), and other homicides (22.0 per 100000).
        Around 2015–2016, The Guardian newspaper ran its own database, The Counted, which tracked US killings by police and other law enforcement agencies including from gunshots, tasers, car accidents and custody deaths. 
        They counted 1,146 deaths for 2015 and 1,093 deaths for 2016. The database can be viewed by state, gender, race/ethnicity, 
        age, classification (e.g., "gunshot"), and whether the person killed was armed.
        The Washington Post has tracked shootings since 2015, reporting more than 5,000 incidents since their tracking began.The database can also classify people in various categories including race, age, weapon etc. For 2019, it reported a total of 1,004 people shot and killed by police.According to the database, 6,600 have been killed since 2015, including 6,303 men and 294 women. Among those killed, 3,878 were armed with a gun, 1,119 were armed with a knife, 218 were armed with a vehicle, 244 had a toy weapon, and 421 were unarmed.
        A research brief by the Police Integrity Research Group of Bowling Green State University found that between 2005 and 2019, 104 nonfederal law enforcement officers had been arrested for murder or manslaughter for an on-duty shooting. As of 2019, 80 cases cases had concluded, with 35 leading to convictions, though often on lesser charges; 18 were convicted of manslaughter and four were convicted of murder.
        According to an article in The Lancet, between 1980 and 2018, more than 30,000 were killed by the police.The study estimated that 55.5% the deaths were incorrectly classified in the U.S. National Vital Statistics System, which tracks information from death certificates.Death certificates do not require coroners to list whether the police were involved in the death which may contribute to the disparity.
        '''
        st.markdown(
            "On the next tab is the list of people **killed by law enforcement in the United States**, both on duty and off duty.")
        st.markdown(text)
    with tab2:
        st.header("us_police_shooting.csv")
        st.write(df)

    with tab3:
        st.header('Statistics')
        chart1 = df.describe()
        corr = df.corr()
        st.write(chart1)
        heatmap = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='BrBG')
        heatmap.set_title('Correlation Heatmap', fontdict={
                          'fontsize': 12}, pad=12)


def charts():
    st.subheader("CHARTS")
    tab1, tab2, tab3, tab4 = st.tabs(
        ['Death over years', 'Race battle', 'Body Camera effect?', 'MAP'])
    with tab1:
        # line charts of death per year
        st.header("Here you can compare the overall police shootings in US to your favorite State")
        col1, col2 = st.columns(2)
        states = df['state'].unique()
        state = st.selectbox('Select a state for further investigation',states)

        shots_count = df.groupby([pd.Grouper(key='date', freq='Y')])[
            'date'].size().reset_index(name='count')
        line_chart = alt.Chart(shots_count).mark_line(opacity=0.4, color='red').encode(
            x=alt.X('date', title='Year'),
            y='count'
        )
        col1.subheader('Overall Death over years')
        col1.altair_chart(line_chart, use_container_width=True)

        #group by states 

        states = df['state'].unique()
        state_count = df[['date','state','city']] 
        state_count = state_count.groupby([pd.Grouper(key='date', freq='Y'), 'state']).size().reset_index(name='count')

        df_state = state_count[state_count['state'] == state]
        
        line_chart2 = alt.Chart(df_state).mark_line(opacity=0.4, color='yellow').encode(
            x=alt.X('date', title='Year'),
            y='count'
        )
        col2.subheader("Investigate further with your favorite state")
        col2.altair_chart(line_chart2, use_container_width=True)

    with tab2:
        # race death over the years -bar chart
        st.subheader("Race Death Over The Years")
        col1, col2 = st.columns(2)

        race_count = df[['date', 'race']]
        race_count = race_count.groupby(
            [pd.Grouper(key='date', freq='Y'), 'race']).size().reset_index(name='count')
        col1.write(race_count)
        bar_chart = alt.Chart(race_count).mark_bar().encode(
            x=alt.X('date', title='Year'),
            y=alt.Y('count'),
            color=alt.Color('race', legend=alt.Legend(title='Race'))
        ).properties(width=800)
        #view it
        col2.subheader("Suprise?")
        col2.altair_chart(bar_chart, use_container_width=True)
        st.markdown("The purpose of this chart is to show people how bad police shooting is and not only for Black people")


    with tab3:
        # does body camera have an effect on police shooting?
        st.subheader("Does body camera have an effect on police shooting?")
        body_camera = df[['body_camera']]
        body_camera = body_camera.groupby(
            ['body_camera']).size().reset_index(name='count')

        bar_chart_bc = alt.Chart(body_camera).mark_bar().encode(
            y='count:Q',
            x='body_camera:O',
        )
        st.altair_chart(bar_chart_bc, use_container_width=True)
        st.subheader("Body camera DOES MATTER.")
        st.markdown("I remember when body camera was first introduced, many people were skeptical about it on how it could possibly help the police.")
        st.markdown("The answer is obvious. It is not meant to help the police but to also protect us against police officers misusing their authority.")
    with tab4:
        # map us states with most police shootings
        st.subheader("MAP")
        df_map = df[['latitude', 'longitude']]
        st.map(df_map)

        st.subheader("San Francisco dive in")
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=37.76,
                longitude=-122.4,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))


page = st.sidebar.selectbox('',
                            ['Home page', 'Charts'])
if page == 'Home page':
    main_page()
if page == 'Charts':
    charts()
