#######################
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from PIL import Image

#######################
# Page configuration
st.set_page_config(
    page_title="Var?",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded")



#######################
# Ladda in data
gdf = gpd.read_file('Data.gpkg')




#######################
# Sidebar - Hämta input
with st.sidebar:

    st.title('Hur viktiga är dessa frågor för SKBs nya markstrategi?')
    
    Fnärhet = st.slider('Hur stor andel av kommunen ligger inom 1 timme från Stockholm eller Uppsala?', 0, 10, 5)
    FTomträtt = st.slider('Tillämpar kommunen tomträtt?', 0, 10, 5)
    FDirektanvisar = st.slider('Direktanvisar kommunen mark?', 0, 10, 5)
    Fbefolkning = st.slider('Hur är befolkningsutvecklingen i kommunen?', 0, 10, 5)
    Fmarkvärde = st.slider('Vad är snittpriset per kvadratmeter mark?', 0, 10, 5)
    Fgrön = st.slider('Hur stor är krontäckningen i urbana områden i kommunen?', 0, 10, 5)
    Fbestånd = st.slider('Har SKB ett stort bestånd i kommunen?', 0, 10, 5)
    Fmedlemstäthet = st.slider('Hur många SKB-medlemmar bor i kommunen?', 0, 10, 5)
    



########################
# Beräkna poäng baserat på input

gdf['potential']=gdf['närhet']*Fnärhet + gdf['Betyg - Direktanvisningar']*FDirektanvisar + gdf['Betyg - tomträtt']*FTomträtt+gdf['markvärde']*Fmarkvärde + gdf['Befolkingsutveckling - betyg']*Fbefolkning+ gdf['Bestånd']*Fbestånd + gdf['krontäckning']*Fgrön + gdf['antal per invånare']*Fmedlemstäthet#
maxpoäng = 600
gdf = gdf.sort_values(by='potential', ascending=False)

########################
# Definiera funktioner för att skapa grafik

def make_map(gdf):
    color_scale = ["#ffffff", "#004d73"]  # white → blue

    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.__geo_interface__,
        locations=gdf.index,
        color='potential',
        hover_name='Kommun',
        hover_data={},
        color_continuous_scale=color_scale,
        mapbox_style="carto-positron",   # background
        zoom=7,                          # adjust to your region
        center={"lat": 59.457969, "lon": 18.339531},  # roughly center of Sweden 59.457969, 18.339531
        opacity=0.7,
    )

    fig.update_layout(
        height=800,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False
    )

    return fig



#########################
# Plotta in content in Streamlit

col = st.columns((4, 2), gap='medium')

with col[0]:
    st.markdown('# VAR?')
            
    Map = make_map(gdf)
    st.plotly_chart(Map, use_container_width=True)

    
    

with col[1]:
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("")  
    st.markdown('#### Kommuner med högst potential:')



    
    ### Create DF with top kommuner
    df_to_display = gdf[['Kommun', 'potential']]

    
    st.dataframe(
            df_to_display,
            column_order=("Kommun", "potential"),
            hide_index=True,
            # width=None,
            column_config={
                "Kommun": st.column_config.TextColumn(
                    "Kommun",
                ),
                "potential": st.column_config.ProgressColumn(
                    "potential",
                    help=None,
                    min_value=0,
                    max_value=max(gdf.potential),
                    format=" "
                )
            }
        )
    

    

    # Beskrivning
    with st.expander('Beskrivning', expanded=False):
        st.write('''
            Detta verktyg är utvecklat av Urbanworks i syfte att understödja SKBs styrelse till ett evidenbaserat förhållningssätt i framtagandet av en ny markstrategi. Datan som ligger till grund för kartan du ser är hämtad från
                 Traveltime, kommunernas markpolicys, SCB, Svensk Mäklarstatistik, Boverket och SKB. Vi på Urbanworks har utifrån detta dataunderlag poängsatt kommunerna i varje kategori. Verktyget kan användas för att visa hur olika 
                 prioriteringar kan leda till att olika kommuner blir attraktiva för SKB att investera i.''')

    st.write("")  
    st.write("")  


    # Setup logo
    image = Image.open('Urban Works_logga_svart_300 dpi.png')
    st.image(image, width=200)

    image1 = Image.open('SKB - logga.png')
    st.image(image1, width=200)