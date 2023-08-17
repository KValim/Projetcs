import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
def load_config():
    config_path = './config.yaml'
    with open(config_path) as file:
        return yaml.load(file, Loader=SafeLoader)

def save_config(config):
    file_path='./config.yaml'
    print(file_path)
    
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def login_widget():
    config = load_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login('Login', 'main')
    return authenticator, name, authentication_status, username

def authenticate_users(authenticator):
    if st.session_state["authentication_status"]:
    
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

def password_reset(authenticator, username):
    if authenticator.reset_password(username, 'Reset password'):
        st.success('Password modified successfully')

def register_new_user(authenticator):
    print('0')
    config = load_config()
    print('1')
    user_details = authenticator.register_user('Register user', preauthorization=False)
    print('2')
    if user_details:
        print('3')
        conconfig['credentials']['usernames'][user_details['username']] = {
            'email': user_details['email'],
            'name': user_details['name'],
            'password': user_details['password_hash']
        }
        save_config(config)


def forgot_password(authenticator):
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
    if username_of_forgotten_password:
        st.success('New password to be sent securely')
    else:
        st.error('Username not found')

def forgot_username(authenticator):
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username('Forgot username')
    if username_of_forgotten_username:
        st.success('Username to be sent securely')
    else:
        st.error('Email not found')

def update_user_details(authenticator, username):
    config = load_config()  
    if authenticator.update_user_details(username, 'Update user details'):
        st.success('Entries updated successfully')
        save_config(config)

def get_email_from_username(username):
    config_path = './config.yaml'

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config['credentials']['usernames'][username]['email']