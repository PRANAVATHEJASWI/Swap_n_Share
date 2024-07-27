import streamlit as st
from google.cloud import firestore

def get_db():
    db = firestore.Client.from_service_account_json('key.json')
    return db

def authenticate(username, password):
    db = get_db()
    auser = db.collection('users')
    query = auser.where('username', '==', username).limit(1).get()
    if query:
        user_doc = query[0]
        user_data = user_doc.to_dict()
        if user_data['password'] == password:
            return True, user_doc.id  # Return user_id
    return False, None

def usernotexist(username):
    db = get_db()
    auser = db.collection('users')
    query = auser.where('username', '==', username).get()
    return len(query) == 0

def login_page():
    st.title("Swap n Share")
    st.header("Login")

    with st.form("login_form"):
        username = st.text_input("Enter your username")
        password = st.text_input("Enter the password", type='password')
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if usernotexist(username):
                st.warning("User doesn't exist")
            else:
                is_authenticated, user_id = authenticate(username, password)
                if is_authenticated:
                    st.success("Login successful")
                    st.session_state['username'] = username
                    st.session_state['user_id'] = user_id  # Set user_id in session state
                    st.experimental_rerun()  # Redirect to the main page
                else:
                    st.warning("Incorrect password")

    st.markdown("Don't have an account? [Click here to create one](#)")
    st.markdown("If the link doesn't work, click the 'Create Account' option in the sidebar.")

if __name__ == "__main__":
    login_page()
