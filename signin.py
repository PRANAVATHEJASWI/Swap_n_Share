import streamlit as st
from google.cloud import firestore

def get_db():
    return firestore.Client.from_service_account_json('key.json')

def unique(username):
    db = get_db()
    duser = db.collection('users')
    check = duser.where('username', '==', username).limit(1).get()
    return len(check) == 1

def signin_page():
    st.title("Swap n Share")
    st.header("Create Account:")

    # Create a form for user signup
    with st.form("signup_form"):
        name = st.text_input("Enter your name")
        username = st.text_input("Enter username")
        password = st.text_input("Enter the password", type='password')
        email = st.text_input("Enter the Email")
        usn = st.text_input("Enter the USN")
        mobile = st.text_input("Enter Contact Number")

        accepted_tnc = st.checkbox("I have read and accept the Terms & Conditions")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not accepted_tnc:
                st.warning('You must accept the Terms & Conditions to create an account.', icon="⚠️")
            elif len(username) <= 6:
                st.warning('Username must have a minimum of 6 characters', icon="⚠️")
            elif len(password) <= 6:
                st.warning('Password must have a minimum of 6 characters', icon="⚠️")
            elif unique(username):
                st.warning('User Exists', icon="⚠️")
            elif len(mobile) != 10:
                st.error("Enter a valid Mobile number")
            elif len(usn) != 10:
                st.warning("Enter a Valid USN")
            elif "vvce.ac.in" not in email:
                st.error("Email must contain 'vvce.ac.in'")
            else:
                db = get_db()
                user_data = {
                    "name": name,
                    "username": username,
                    "password": password,
                    "email": email,
                    "usn": usn,
                    "mobile": mobile
                }
                users_ref = db.collection('users')
                users_ref.document(username).set(user_data)
                st.success("Account created successfully!")
                st.info("Account exists? [Click here to login](#Login)")

if __name__ == "__main__":
    signin_page()
