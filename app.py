import streamlit as st
from streamlit_option_menu import option_menu
from contribute import contribute
from request import request

def main_app():
    st.title("Swap n Share")

    # Sidebar navigation
    selected = option_menu(
        menu_title="",
        options=["Request", "Contribute"],
        icons=["arrow-down-circle", "arrow-up-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Request":
        request()
    elif selected == "Contribute":
        contribute()

def main():
    if 'username' in st.session_state:
        # Redirect to the main application
        main_app()  
    else:
        st.warning("You need to log in to access this page.")
        st.stop()  # Stop execution until user logs in

if __name__ == "__main__":
    main()
