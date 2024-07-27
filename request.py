import streamlit as st
from google.cloud import firestore
import pandas as pd
import base64
from PIL import Image
import io

def get_db():
    return firestore.Client.from_service_account_json('key.json')

def render_image(image_b64):
    if image_b64:
        try:
            image_bytes = base64.b64decode(image_b64)
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size
            new_size = (int(width * 0.5), int(height * 0.5))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            st.image(image, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.write("No image available")

def display_contributed_items():
    st.header("Available Items")

    db = get_db()
    contributions_ref = db.collection('contributions')

    def get_contributions():
        return [doc.to_dict() for doc in contributions_ref.stream()]

    contributions = get_contributions()

    if contributions:
        df = pd.DataFrame(contributions)
        required_fields = ['item_name', 'description', 'location', 'amount', 'mobile', 'username']
        for field in required_fields:
            if field not in df.columns:
                df[field] = None

        df = df[['item_name', 'description', 'location', 'amount', 'mobile', 'username']]
        st.write(df)
    else:
        st.write("No items available")

def request():
    st.header("Request Item")

    with st.form("request_form"):
        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        amount = st.number_input("Amount", min_value=0, step=1, format="%d")  # Updated to accept only integers
        mobile = st.text_input("Mobile Number")

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            db = get_db()
            request_data = {
                "item_name": item_name,
                "description": description,
                "amount": amount,
                "mobile": mobile,
                "username": st.session_state['username']  # Add username to the request
            }
            db.collection('requests').add(request_data)
            st.success("Item requested successfully!")
            st.experimental_rerun()  # Refresh to show the new request

    st.header("Search Available Items")
    search_term = st.text_input("Enter item name to search", "")
    search_button = st.button("Search")

    if search_button and search_term:
        db = get_db()
        contributions_ref = db.collection('contributions')
        query = contributions_ref.where('item_name', '==', search_term).get()

        if query:
            results = [doc.to_dict() for doc in query]

            if results:
                df = pd.DataFrame(results)
                required_fields = ['item_name', 'description', 'location', 'amount', 'mobile', 'username', 'image']
                for field in required_fields:
                    if field not in df.columns:
                        df[field] = None

                df = df[['item_name', 'description', 'location', 'amount', 'mobile', 'username', 'image']]
                st.write(df)

                for index, row in df.iterrows():
                    st.write(f"Item Name: {row['item_name']}")
                    st.write(f"Description: {row['description']}")
                    st.write(f"Location: {row['location']}")
                    st.write(f"Amount: {row['amount']}")
                    st.write(f"Mobile: {row['mobile']}")
                    st.write(f"Username: {row['username']}")
                    render_image(row.get('image', None))
                    st.write("-----")
            else:
                st.write("No items found")
        else:
            st.write("No items found")

    display_contributed_items()

if __name__ == "__main__":
    request()
