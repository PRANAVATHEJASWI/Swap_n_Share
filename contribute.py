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

def display_requested_items():
    st.header("Requested Items")

    db = get_db()
    requests_ref = db.collection('requests')

    def get_requests():
        return [doc.to_dict() for doc in requests_ref.stream()]

    requests = get_requests()

    if requests:
        df = pd.DataFrame(requests)
        required_fields = ['item_name', 'description', 'amount', 'mobile', 'username']
        for field in required_fields:
            if field not in df.columns:
                df[field] = None

        df = df[['item_name', 'description', 'amount', 'mobile', 'username']]
        st.write(df)
    else:
        st.write("No items requested")

def contribute():
    if 'username' not in st.session_state or 'user_id' not in st.session_state:
        st.warning("User not logged in. Cannot contribute item.")
        st.stop()

    st.header("Contribute Item")

    with st.form("contribute_form"):
        item_name = st.text_input("Item Name")
        description = st.text_area("Description")
        location = st.text_input("Location")
        amount = st.number_input("Amount", min_value=0, step=1, format="%d")  # Updated to accept only integers
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not item_name or not description or not location or amount <= 0:
                st.error("All fields are required.")
                st.stop()

            db = get_db()
            user_ref = db.collection('users').document(st.session_state['user_id'])
            user_doc = user_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                username = user_data['username']
                mobile = user_data['mobile']

                image_b64 = None
                if image:
                    image_bytes = image.read()
                    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                else:
                    st.warning("No image uploaded. The item will be submitted without an image.")

                contribute_data = {
                    "item_name": item_name,
                    "description": description,
                    "location": location,
                    "amount": amount,
                    "username": username,
                    "mobile": mobile,
                    "image": image_b64
                }

                db.collection('contributions').add(contribute_data)
                st.success("Item contributed successfully!")
                st.experimental_rerun()  # Refresh the page to show the new contribution

    st.header("Search Requested Items")
    search_term = st.text_input("Enter item name to search", "")
    search_button = st.button("Search")

    if search_button and search_term:
        db = get_db()
        requests_ref = db.collection('requests')
        query = requests_ref.where('item_name', '==', search_term).get()

        if query:
            results = [doc.to_dict() for doc in query]

            if results:
                df = pd.DataFrame(results)
                required_fields = ['item_name', 'description', 'amount', 'mobile', 'username']
                for field in required_fields:
                    if field not in df.columns:
                        df[field] = None

                df = df[['item_name', 'description', 'amount', 'mobile', 'username']]
                st.write(df)

                for index, row in df.iterrows():
                    st.write(f"Item Name: {row['item_name']}")
                    st.write(f"Description: {row['description']}")
                    st.write(f"Amount: {row['amount']}")
                    st.write(f"Mobile: {row['mobile']}")
                    st.write(f"Username: {row['username']}")
                    st.write("-----")
            else:
                st.write("No items found")
        else:
            st.write("No items found")

    display_requested_items()

if __name__ == "__main__":
    contribute()
