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


#######################
# Ladda in data
gdf = gpd.read_file('Data.gpkg')




#######################
# Sidebar - Hämta input
with st.sidebar:
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("")
    st.title('Vikta din karta')
    
    Fpolitik = st.selectbox('Politisk riktning', pd.Series(range(11)))
    FTomträtt = st.selectbox('Tomträtt', pd.Series(range(11)))
    FDirektanvisar = st.selectbox('Direktanvisar', pd.Series(range(11)))
    Fbefolkning = st.selectbox('Befolkningsutveckling', pd.Series(range(11)))
    Favstånd = st.selectbox('Avstånd till Stockholm C', pd.Series(range(11)))
    
    
########################
# Beräkna ppoäng baserat på input

gdf['poäng']=gdf['Betyg - Politik']*Fpolitik + gdf['Betyg - Direktanvisningar']*FDirektanvisar + gdf['Betyg - tomträtt']*FTomträtt+gdf['Avstånd till Stockholm C']*Favstånd + gdf['Befolkingsutveckling - betyg']*Fbefolkning
maxpoäng = 500
gdf_sorted = gdf.sort_values(by='poäng', ascending=False)
gdf_sorted['normalized'] = gdf_sorted['poäng'] / maxpoäng
gdf_sorted['poäng'] = (gdf_sorted['normalized'] * 100).round(0)


########################
# Definiera funktioner för att skapa grafik

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
    
    fig.update_layout(height=800)  # <-- Adjust height here

    return fig

def make_scorecard(Fpolitik, FTomträtt, FDirektanvisar, Fbefolkning):
    
    
    Y = [Fpolitik, FTomträtt, FDirektanvisar, Fbefolkning, Favstånd]
    X = ['Politisk riktning', 'Tomträtt', 'Direktanvisar', 'Befolkningsutveckling', 'Avstånd till Stockholm C']

    # Create DataFrame from X and Y
    source = pd.DataFrame({
        'kategori': X,
        'viktning': Y
    })

    # Bar chart
    bar_chart = alt.Chart(source).mark_bar(color='#004D73').encode(
        x=alt.X('viktning:Q', title='Viktning', scale=alt.Scale(domain=[0, 10])),
        y=alt.Y('kategori:O', title='Kategori'),
        tooltip=['kategori:O', 'viktning:Q']
    ).properties(
        width=300,
        height=200
    )
    return bar_chart

#########################
# Plotta in content in Streamlit

col = st.columns((4, 2), gap='medium')

with col[0]:
    st.markdown('# Var ska vi investera?')
            
    Map = make_map(gdf_sorted)
    st.plotly_chart(Map, use_container_width=True)

    st.markdown('#### Min viktning')
    barchart = make_scorecard(Fpolitik, FTomträtt, FDirektanvisar, Fbefolkning)
    st.altair_chart(barchart, use_container_width=True)
    

with col[1]:
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("")  
    st.markdown('#### Kommuner med högst poäng')



    
    ### Create DF with top kommuner
    cols = ['geometry', 'Betyg - Politik', 'Betyg - Direktanvisningar', 'Betyg - tomträtt','normalized']

    df_to_display = gdf_sorted.drop(columns=cols)

    
    st.dataframe(
            df_to_display,
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
                    format=None,
                )
            }
        )
    

    

    # Beskrivning
    with st.expander('Beskrivning', expanded=True):
        st.write('''
            Detta verktyg är utvecklat av Urbanworks i syfte att inspirera SKB till ett evidenbaserat beslutsfattande. Datan är hämtad från ...''')

    st.write("")  
    st.write("")  
    st.write("")  
    st.write("") 
    st.write("") 

    # Setup logo
    image = Image.open('Urban Works_logga_svart_300 dpi.png')
    st.image(image, width=200)

    image1 = Image.open('SKB - logga.png')
    st.image(image1, width=200)



