# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 21:03:00 2021

@author: nondarloavedere
"""

from geopy.geocoders import Nominatim
import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import os 

# Directories
data_path = r'Data'

crs = 32632


which_modes = ['Trova casa mia', 'Seleziona comune', 'Seleziona cabina primaria']
which_mode = st.sidebar.selectbox('Seleziona modalità', which_modes, index=0)

if which_mode == 'Trova casa mia':  
    geolocator = Nominatim(user_agent="example app")
    
    sentence = st.sidebar.text_input('Scrivi il tuo indirizzo:', value='B12 Bovisa') 
    try:
        location = geolocator.geocode(sentence)
    
    
        if sentence:
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=25)
            tile = folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Esri Satellite',
                overlay=False,
                control=True
            ).add_to(m)
            
            tile = folium.TileLayer(
                tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}',
                attr='Google',
                name='Google Hybrid',
                overlay=False,
                control=True
            ).add_to(m)
            
            tile = folium.TileLayer(
                tiles='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}',
                attr='Google',
                name='Google Maps',
                overlay=False,
                control=True
            ).add_to(m)
            
            feature_group_3 = folium.FeatureGroup(name=sentence, show=True)
                            
            new_lat = location.latitude
            new_long = location.longitude
            
            # add marker
            tooltip = sentence
            folium.Marker(
                [new_lat, new_long], popup=sentence, tooltip=tooltip
            ).add_to(feature_group_3)
            
            feature_group_3.add_to(m)
            
            folium.plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None,
                                edit_options=None).add_to(m)
            folium.plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen',
                                      force_separate_button=False).add_to(m)
            folium.plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles',
                                          primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
            folium.LayerControl().add_to(m)
            
            # Displaying a map         
            
            folium_static(m)
    except:
            st.write('Non sono riuscito a trovare la tua posizione. Riprova per favore.')
elif which_mode == 'Seleziona comune':  
    admin_gdf = gpd.read_file(os.path.join(data_path, 'Procedure', '3_admin.shp'))
    
    regions = admin_gdf.NAME_1.drop_duplicates().sort_values()
    which_region = st.sidebar.selectbox('Seleziona la regione', regions, index=0)
    
    provinces_gdf = admin_gdf[admin_gdf.NAME_1 == which_region]
    provinces = provinces_gdf.NAME_2.drop_duplicates().sort_values()
    which_province = st.sidebar.selectbox('Seleziona la provincia', provinces, index=0)
        
    comuni_gdf = provinces_gdf[provinces_gdf.NAME_2 == which_province]
    comuni = comuni_gdf.NAME_3.drop_duplicates().sort_values()
    which_comune = st.sidebar.selectbox('Seleziona il comune', comuni, index=0)
         
    area_gdf = comuni_gdf[comuni_gdf.NAME_3 == which_comune]
    
    m = folium.Map(location=[area_gdf.centroid.y, area_gdf.centroid.x], zoom_start=12)
    tile = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    tile = folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid',
        overlay=False,
        control=True
    ).add_to(m)
    
    tile = folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)
    
    feature_group_3 = folium.FeatureGroup(name='Comune selezionato', show=True)
    style4 = {'fillColor': 'red', 'color': 'red'}         
    folium.GeoJson(area_gdf.to_json(), name='Comune selezionato',
                style_function=lambda x: style4).add_to(feature_group_3)
    
    feature_group_3.add_to(m)
    
    folium.plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None,
                        edit_options=None).add_to(m)
    folium.plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen',
                              force_separate_button=False).add_to(m)
    folium.plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles',
                                  primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
    folium.LayerControl().add_to(m)
    
    # Displaying a map         
    
    folium_static(m)

elif which_mode == 'Seleziona cabina primaria':    
    subs_gdf = gpd.read_file(os.path.join(data_path, 'Procedure', '0_cp.shp'))
    
    subs_names = subs_gdf.nome.drop_duplicates().sort_values()
    which_sub = st.sidebar.selectbox('Seleziona la cabina primaria', subs_names, index=0)
    
    sub_gdf = subs_gdf[subs_gdf.nome == which_sub]
    
    m = folium.Map(location=[sub_gdf.unary_union.y, sub_gdf.unary_union.x], zoom_start=12)
    tile = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    tile = folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid',
        overlay=False,
        control=True
    ).add_to(m)
    
    tile = folium.TileLayer(
        tiles='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)
    
    feature_group_3 = folium.FeatureGroup(name=which_sub, show=True)
                    
    new_lat = sub_gdf.unary_union.y
    new_long = sub_gdf.unary_union.x
    
    # add marker
    tooltip = which_sub
    folium.Marker(
        [new_lat, new_long], popup=which_sub, tooltip=tooltip
    ).add_to(feature_group_3)
    
    feature_group_3.add_to(m)
    
    folium.plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None,
                        edit_options=None).add_to(m)
    folium.plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen',
                              force_separate_button=False).add_to(m)
    folium.plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles',
                                  primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
    folium.LayerControl().add_to(m)
    
    # Displaying a map         
    
    folium_static(m)

