import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np

class PetShopMap:

    def __init__(self):
        self.csv_path = 'data\stores.csv'
        self.df = self.load_data()

    def load_data(self):
        # Lendo os dados do arquivo CSV
        df = pd.read_csv(self.csv_path)
        
        # Dicionário de cores para cada tipo de loja em formato RGBA (0-255)
        color_mapping = {
            'pet_spa': 'rgba(255, 0, 0, 1)',      # red
            'marketplace': 'rgba(0, 0, 255, 1)', # blue
            'pet_shop': 'rgba(0, 255, 0, 1)'     # green
        }

        # Adicionando uma nova coluna 'color' ao DataFrame
        df['color'] = df['tipo'].apply(lambda x: color_mapping.get(x))
        
        return df

    def display_map(self, owner_latitude=None, owner_longitude=None):
        # Filtrando as lojas que estão abertas
        df_aberto = self.df[self.df["aberto"] == True]
        
        # Criando um mapa usando o Plotly.graph_objects
        fig = go.Figure()

        # Adicionando as lojas ao mapa
        fig.add_trace(go.Scattermapbox(
            lat=df_aberto['latitude'],
            lon=df_aberto['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9,
                color=df_aberto['color'],
                opacity=0.6
            ),
            hoverinfo='text',
            hovertext=df_aberto['nome']
        ))

        # Adicionando círculo ao redor da localização do proprietário
        if owner_latitude and owner_longitude:
            circle_lat, circle_lon = self._draw_circle(owner_latitude, owner_longitude, 1)
            fig.add_trace(go.Scattermapbox(
                lat=circle_lat,
                lon=circle_lon,
                mode='lines',
                line=go.scattermapbox.Line(width=2, color='black'),
                fill='toself',
                fillcolor='rgba(0, 0, 0, 0.1)',
                hoverinfo='none'  
            ))
        
            # Atualizando layout do mapa
            fig.update_layout(
                mapbox_style="dark",
                mapbox_center_lat=owner_latitude if owner_latitude else df_aberto['latitude'].mean(),
                mapbox_center_lon=owner_longitude if owner_longitude else df_aberto['longitude'].mean(),
                mapbox_zoom=14,  # Ajustando o zoom
                showlegend=False,
                height=700,
                mapbox_accesstoken='pk.eyJ1Ijoia3ZhbGlpbSIsImEiOiJjbGw0a3pzamIwNm82M3VxampsZ3NicDdqIn0.WEvetdPrWIs1uLTBJqwOLg'# Desativando a legenda
            )
            
            fig.add_trace(go.Scattermapbox(
                lat=df_aberto['latitude'],
                lon=df_aberto['longitude'],
                mode='markers+text',  # Modo de marcadores com texto
                marker=go.scattermapbox.Marker(
                    size=9,
                    color=df_aberto['color'],
                    opacity=0.6
                ),
                text=df_aberto['nome'],  # Texto do nome da loja
                textposition="top right",  # Posição do texto em relação ao marcador
                hoverinfo='none'  
            ))


        # Mostrando o mapa no Streamlit
        st.plotly_chart(fig, use_container_width=True)

    def _draw_circle(self, lat, lon, radius_km):
        # Convertendo latitude e longitude para float
        lat = float(lat)
        lon = float(lon)
        
        lats = []
        lons = []
        
        # Cálculo para ajustar a longitude com base na latitude (para corrigir o efeito oval)
        lon_adj = radius_km / (111.320 * np.cos(np.radians(lat)))

        for i in range(361):  # 360 graus + 1 para fechar o círculo
            angle = 0.0174532925199 * i  # Convertendo graus para radianos
            dx = radius_km * np.cos(angle)
            dy = radius_km * np.sin(angle)

            new_lon = lon + (dx / 111.32)  # Uso do lon_adj aqui
            new_lat = lat + (dy / 110.574)

            lats.append(new_lat)
            lons.append(new_lon)

        return lats, lons