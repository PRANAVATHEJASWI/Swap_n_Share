import streamlit as st
from streamlit_option_menu import option_menu
from login import login_page
from signin import signin_page
from app import main_app  # Import the main app function
from terms_and_condition import show_terms_and_conditions
def main():
    if 'username' in st.session_state:
        # Redirect to the main application
        main_app()  
    else:
        selected = option_menu(
                menu_title="",  
                options=["Login", "Create Account","T&C"], 
                icons=["house", "envelope"],
                menu_icon="cast",  
                default_index=0,  
                orientation="horizontal"
            )
        if selected == "Login":
            login_page()
        elif selected == "Create Account":
            signin_page()
        elif selected == "T&C":
            show_terms_and_conditions()

if __name__ == "__main__":
    main()