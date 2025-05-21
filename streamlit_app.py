#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd

#######################
# Page configuration
st.set_page_config(
    page_title="Var ska vi investera?",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("default")


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
    st.write('''
        - **Politisk riktning**: 10 = vänster, 0 = höger
        - **Tomträtt**: 10 = ja, 00 = nej
        - **Direktanvisar**: 10 = ja, 0 = nej
    ''')
    
Fpolitik = 7
FTomträtt = 3
FDirektanvisar = 5

gdf['poäng']=gdf['Betyg - Politik']*Fpolitik + gdf['Betyg - Direktanvisningar']*FDirektanvisar + gdf['Betyg - tomträtt']*FTomträtt
gdf_sorted = gdf.sort_values(by='poäng', ascending=False)
#gdf_sorted['normalized'] = gdf_sorted['total'] / gdf_sorted['total'].max()
#gdf_sorted['poäng'] = (gdf_sorted['normalized'] * 100).round(1)

print(gdf_sorted)


"""
#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap
"""
print('check 0')
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
        zoom=8, 
        center={"lat": 59.33, "lon": 18.07}
    )
    return fig

FIG = make_map(gdf_sorted)
FIG.show()

#######################
# Dashboard Main Panel
col = st.columns((4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Var ska vi investera?')
    
    Map = make_map(gdf)
    st.plotly_chart(Map, use_container_width=True)
    
    """
    heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
    """



with col[1]:
    st.markdown('#### Min bästa kommun')

st.dataframe(gdf.drop(columns='geometry'))

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
                    "Betyg": st.column_config.ProgressColumn(
                        "poäng",
                        min_value=0,
                        max_value=max(gdf.poäng),
                     )}
                 )
    
with st.expander('Beskrivning', expanded=True):
        st.write('''
            Detta verktyg är utvecklat av Urbanworks i syfte att inspirera SKB till ett evidenbaserat beslutsfattande. Datan är hämtad från ...''')