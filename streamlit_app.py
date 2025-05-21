#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd
from PIL import Image

#######################
# Page configuration
st.set_page_config(
    page_title="Var ska vi investera?",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("default")


# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #ffffff;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)



#######################
# Load data
gdf = gpd.read_file('250521_prepared-data.gpkg')




#######################
# Sidebar
with st.sidebar:
    st.title('Vikta din karta')
    
    Fpolitik = st.selectbox('Politisk riktning', pd.Series(range(11)))
    FTomträtt = st.selectbox('Tomträtt', pd.Series(range(11)))
    FDirektanvisar = st.selectbox('Direktanvisar', pd.Series(range(11)))
    

gdf['poäng']=gdf['Betyg - Politik']*Fpolitik + gdf['Betyg - Direktanvisningar']*FDirektanvisar + gdf['Betyg - tomträtt']*FTomträtt
gdf['poäng'] = gdf['poäng']/gdf['poäng'].max()
gdf_sorted = gdf.sort_values(by='poäng', ascending=False)
#gdf_sorted['normalized'] = gdf_sorted['total'] / gdf_sorted['total'].max()
#gdf_sorted['poäng'] = (gdf_sorted['normalized'] * 100).round(1)




#######################
# Plots

# Heatmap
#def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
#    heatmap = alt.Chart(input_df).mark_rect().encode(
#            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
#            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
#            color=alt.Color(f'max({input_color}):Q',
#                             legend=None,
#                             scale=alt.Scale(scheme=input_color_theme)),
#            stroke=alt.value('black'),
#            strokeWidth=alt.value(0.25),
#        ).properties(width=900
#        ).configure_axis(
#        labelFontSize=12,
#        titleFontSize=12
#        ) 
    # height=300
#    return heatmap


def make_map(gdf):
    color_scale = [
        (0, "rgba(255, 255, 255, 0.8)"),   
        (1, "rgba(0, 77, 115, 0.8)")     
    ]

    fig = px.choropleth_map(
        gdf,
        geojson=gdf.__geo_interface__,
        locations=gdf.index,
        color='poäng',
        hover_name='Kommun',
        color_continuous_scale=color_scale, 
        map_style="light",
        zoom=7, 
        center={"lat": 59.33, "lon": 18.07}
    )
    return fig

col = st.columns((2, 2), gap='medium')

with col[0]:
    st.markdown('#### Var ska vi investera?')
    
    Map = make_map(gdf)
    st.plotly_chart(Map, use_container_width=True)
    




with col[1]:
    st.markdown('#### Kommuner med högst poäng')



    cols = ['geometry', 'Betyg - Politik', 'Betyg - Direktanvisningar', 'Betyg - tomträtt',
        'Styre-2014', 'Styre-2018', 'Styre-2022', 'färgkod', 'kom_name', 'Direktanvisar',
        'Tomträtt_y', '2023', '2024', 'Befolkningsutveckling']

    st.dataframe(gdf_sorted.drop(columns=cols),
                 column_order=("Kommun", "poäng"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Kommun": st.column_config.TextColumn(
                        "Kommun",
                    ),
                    "poäng": st.column_config.ProgressColumn(
                        "poäng",
                        min_value=0,
                        max_value=max(gdf.poäng),
                        color="#gray"
                     )}
                 )
    
with st.expander('Beskrivning', expanded=True):
        st.write('''
            Detta verktyg är utvecklat av Urbanworks i syfte att inspirera SKB till ett evidenbaserat beslutsfattande. Datan är hämtad från ...''')
        
# Setup logo
image = Image.open('Urban Works_logga_vit.png')
st.image(image, width=200)