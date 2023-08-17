from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import csv
import random
from PIL import Image
from modules.login.login import (
    load_config, save_config, login_widget, authenticate_users, 
    password_reset, register_new_user, forgot_password, 
    forgot_username, update_user_details, get_email_from_username
    )

from modules.db.db import (
    load_users_data, save_users_data
    )
from yaml.loader import SafeLoader
import streamlit.components.v1 as components
import yaml
from modules.login.hasher import Hasher
from modules.login.authenticate import Authenticate
from modules.map.map import PetShopMap
from modules.map.cepabertoapi import CepAbertoAPI

from modules.recommendations.recommendation_based_on_purchase import RecommendationBasedOnPurchase
from modules.recommendations.recommendation_by_species import RecommendationBySpecies
from modules.recommendations.general_recommendations import GeneralRecommendations
from modules.recommendations.recommendation_for_user import RecommendationForUser

user_rec = RecommendationForUser()
species_rec = RecommendationBySpecies()
general_rec = GeneralRecommendations()


st.set_page_config(layout="wide")

def register_user_info():
    # Carregue os dados existentes
    users_data = load_users_data()
    
    # Atualize com os novos dados
    users_data[owner_email] = {
        'owner_data': st.session_state.owner_data,
        'pet_data': st.session_state.pet_data
    }
    
    # Salve os dados atualizados de volta no arquivo
    save_users_data(users_data)


def main_app():
    path_especie_raca = r'data\especie_raca.csv'
    path_styles = r'style\style.css'
    

    # Apply custom CSS styles to the header and other elements
    st.markdown(f'<link href="{path_styles}" rel="stylesheet">', unsafe_allow_html=True)

    # Display the styled header
    st.markdown('<p class="title">MERCADO PET</p>', unsafe_allow_html=True)
    st.markdown('<style>' + open(path_styles).read() + '</style>', unsafe_allow_html=True)
    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=['Home', 'Area do Dono', 'Busca', 'Recomendações', 'Login/Logout'],
            iconName=['house', 'info', 'search', 'recommendations', 'logout'],
            default_choice=0
            )

    if tabs == 'Home':
        col1, col2, col3 = st.columns([1,12,1])
        with col2:
            img_logo = Image.open(r'images\logo.png')
            st.image(img_logo, width=500)

            st.write('**Bem-vindo à Mercado Pet**, seu centro on-line abrangente para todas as necessidades do seu animal de estimação! Sabemos o quanto o seu amigo peludo significa para você e, por isso, estamos comprometidos em fornecer tudo que eles necessitam para uma vida saudável e feliz. Desde alimentos de alta qualidade e guloseimas saborosas até brinquedos atraentes, acessórios chiques e medicamentos confiáveis, a Mercado Pet oferece a variedade mais ampla de produtos de qualidade para cães, gatos, pássaros, peixes e outros animais de estimação. Aqui, a vida do seu pet é a nossa prioridade!')
            st.write('Nossa plataforma amigável e fácil de usar torna suas compras de produtos para animais de estimação mais confortáveis do que nunca. Navegue, escolha e receba seus produtos favoritos com alguns cliques, no conforto de sua casa. Além disso, nosso **sistema de recomendação refinado** permite que você descubra novos produtos que seu pet vai amar. Ele aprende a partir de suas compras anteriores e sugere itens que atendem às necessidades específicas e preferências do seu pet. Nunca foi tão fácil mimar seus amigos de quatro patas!')
            st.write('Queremos que você faça parte da nossa família Mercado Pet. A nossa missão é transformar a vida dos pets através da entrega de produtos e serviços com qualidade excepcional, e nos esforçamos para que você e seu pet se sintam amados e valorizados. Se você está procurando o melhor para o seu amigo de estimação, não procure mais. Junte-se a nós na Mercado Pet e transforme a vida do seu amiguinho hoje!')
        
    elif tabs == 'Area do Dono':
        df = pd.read_csv(path_especie_raca)

        # Se o usuário estiver autenticado, carregue seus dados
        owner_default_data = {}
        pet_default_data = {}
        if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
            users_data = load_users_data()
            st.session_state.user_email = get_email_from_username(st.session_state.username)
            user_data = users_data.get(st.session_state.user_email, {})
            owner_default_data = user_data.get('owner_data', {})
            pet_default_data = user_data.get('pet_data', {})

            # Dados do Dono
            with st.form(key='owner_form'):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.header("Dados do Dono")
                    owner_name = st.text_input(label='Nome do Dono', value=owner_default_data.get('Nome do Dono', ''))
                    owner_phone = st.text_input(label='Telefone', value=owner_default_data.get('Telefone', ''))
                    owner_address = st.text_input(label='Endereco', value=owner_default_data.get('Endereco', ''))
                with col2:
                    st.markdown('<div style="height:70px;"></div>', unsafe_allow_html=True)
                    owner_city = st.text_input(label='Cidade', value=owner_default_data.get('Cidade', ''))
                    owner_state = st.text_input(label='Estado', value=owner_default_data.get('Estado', ''))
                    owner_zip = st.text_input(label='CEP', value=owner_default_data.get('CEP', ''))
                    
                    if submit_owner := st.form_submit_button(label='Salvar Dados do Dono'):
                        st.session_state.owner_data = {
                            'Nome do Dono': owner_name,
                            'Email': st.session_state.user_email,
                            'Telefone': owner_phone,
                            'Endereco': owner_address,
                            'Cidade': owner_city,
                            'Estado': owner_state,
                            'CEP': owner_zip,
                        }
                        st.write("Dados do Dono salvos!")
                        
                        users_data = load_users_data()
                        if st.session_state.user_email not in users_data:
                            users_data[st.session_state.user_email] = {}
                        users_data[st.session_state.user_email]['owner_data'] = st.session_state.owner_data
                        
                        # Salve os dados atualizados de volta no arquivo
                        save_users_data(users_data)
                        
            # Dados do Pet
            species = df['Especie'].unique().tolist()
            breeds = df['Raca'].unique().tolist()
            with st.form(key='pet_form'):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.header("Dados do Pet")
                    pet_name = st.text_input(label='Nome do Pet', value=pet_default_data.get('Nome do Pet', ''))
                    
                    pet_species_index = species.index(pet_default_data.get('Especie', 'Selecione a especie')) if pet_default_data.get('Especie') in species else 0
                    pet_species = st.selectbox(label='Especie', options=['Selecione a especie'] + species, index=1 + species.index(pet_default_data.get('Especie', 'Selecione a especie')))
                    
                    pet_breed_index = breeds.index(pet_default_data.get('Raca', 'Selecione a raca')) if pet_default_data.get('Raca') in breeds else 0
                    pet_breed = st.selectbox(label='Raca', options=['Selecione a raca'] + breeds, index=1 + breeds.index(pet_default_data.get('Raca', 'Selecione a raca')))
                    
                    gender_options = ['Selecione o sexo', 'Femea', 'Macho']
                    pet_gender_index = gender_options.index(pet_default_data.get('Sexo', 'Selecione o sexo')) if pet_default_data.get('Sexo') in gender_options else 0
                    pet_gender = st.selectbox(label='Sexo', options=gender_options, index=pet_gender_index)
                    
                    pet_dob = st.date_input(label='Data de Nascimento do Pet', value=pet_default_data.get('Data de Nascimento do Pet', datetime.date.today()))
                    
                    

                    # Foto do Pet
                    with col2:
                        st.markdown('<div style="height:70px;"></div>', unsafe_allow_html=True)
                        if pet_default_data.get('Nome do Pet', '') == 'Batatinha':
                            img_batatinha = Image.open(r'images\batatinha.jpg')
                            st.image(img_batatinha, use_column_width=True)
                            
                        if pet_default_data.get('Nome do Pet', '') == 'Bernardinho':
                            img_batatinha = Image.open(r'images\bernardo.jpg')
                            st.image(img_batatinha, use_column_width=True)
                        
                        if submit_pet := st.form_submit_button(label='Salvar Dados do Pet'):
                            st.session_state.pet_data = {
                                'Nome do Pet': pet_name,
                                'Especie': pet_species,
                                'Raca': pet_breed,
                                'Sexo': pet_gender,
                                'Data de Nascimento do Pet': pet_dob,
                            }
                            st.write("Dados do Pet salvos!")
                            
                            users_data = load_users_data()
                            if st.session_state.user_email not in users_data:
                                users_data[st.session_state.user_email] = {}
                            users_data[st.session_state.user_email]['pet_data'] = st.session_state.pet_data
                            
                            # Salve os dados atualizados de volta no arquivo
                            save_users_data(users_data)
        else:
            st.warning('Login Não Identificado')


    elif tabs == 'Busca':
        if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
            st.text_input(label='Pesquisa')
            if "owner_data" in st.session_state:
                st.title(f"Mapa das lojas Pet pela sua área, {st.session_state.owner_data.get('Nome do Dono', '')}")
            
                # Criando uma instância da classe
                map_instance = PetShopMap()
                
                cep_api = CepAbertoAPI()
                cep = st.session_state.owner_data.get('CEP', '')
                latitude, longitude = cep_api.get_lat_lon_from_cep(cep)

                # Exibindo o mapa com a localização do proprietário
                map_instance.display_map(latitude, longitude)
        else:
            st.warning('Login Não Identificado')


    # Função para exibir um produto em uma box
    def exibir_produto(produto):
        col1, col2, col3 = st.columns(3)  # Dividir o espaço em três colunas
        
        with col1:
            st.subheader(produto['Nome'])  # Usar subheader para o nome do produto
            
        with col2:
            st.image(produto['Imagem'], caption=f"R${float(produto['Preço']):.2f}", width=100)  # Converter o preço para float antes de formatar

        with col3:
            st.write(f"**Descrição**: {produto['Descrição']}")  # Usar negrito para a descrição



    # Lógica para exibição dos produtos
    if tabs == 'Recomendações':
        if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
            if "username" in st.session_state:
                st.markdown('---')
                # Obter recomendações específicas para o usuário
                produtos_selecionados = user_rec.get_recommendations(st.session_state.pet_data)
                st.title(f"Recomendações para {st.session_state.pet_data.get('Nome do Pet', '')}") 
                for produto in produtos_selecionados:
                    exibir_produto(produto)
                
                st.markdown('---')
                produtos_especie = user_rec.get_recommendations(st.session_state.pet_data)
                st.title(f"Recomendações para {st.session_state.pet_data.get('Especie', '')}") 
                for produto in produtos_especie:
                    exibir_produto(produto)
                
                st.markdown('---')
                st.title("Recomendações referentes as últimas compras")

            

        st.markdown('---')
        st.title("Recomendações Gerais")
        st.image('images\pets.png', use_column_width=True)
        
        # Obter recomendações gerais
        produtos_gerais = general_rec.get_recommendations()
        for produto in produtos_gerais:
            exibir_produto(produto)



    if tabs == 'Login/Logout':

        # Loading config file
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Creating the authenticator object
        authenticator = Authenticate(
            config['credentials'],
            config['cookie']['name'], 
            config['cookie']['key'], 
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        # creating a login widget
        name, authentication_status, st.session_state.username = authenticator.login('Login', 'main')
        if authentication_status:
            authenticator.logout('Logout', 'main')
            st.write(f'Welcome *{name}*')
            
            # email do usuario 
            users_data = load_users_data()   
            st.session_state.user_email = get_email_from_username(st.session_state.username)
            user_data = users_data.get(st.session_state.user_email, {})
            st.session_state.owner_data = user_data.get('owner_data', {})
            st.session_state.pet_data = user_data.get('pet_data', {})
            
            # st.session_state.clear()
            # print()
            
        elif authentication_status is False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')

        # Creating a password reset widget
        if authentication_status:
            try:
                if authenticator.reset_password(st.session_state.username, 'Reset password'):
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)

        # Creating a new user registration widget
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

        # Creating a forgot password widget
        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
            if username_forgot_pw:
                st.success('New password sent securely')
                # Random password to be transferred to user securely
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)

        # Creating a forgot username widget
        try:
            username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
            if username_forgot_username:
                st.success('Username sent securely')
                # Username to be transferred to user securely
            else:
                st.error('Email not found')
        except Exception as e:
            st.error(e)

        # Creating an update user details widget
        if authentication_status:
            try:
                if authenticator.update_user_details(st.session_state.username, 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)

        # Saving config file
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        

if __name__ == '__main__':
    main_app()