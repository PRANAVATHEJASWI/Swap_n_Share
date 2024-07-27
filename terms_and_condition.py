import streamlit as st

def show_terms_and_conditions():
    st.title("Terms and Conditions")

    st.markdown("""
    Welcome to the Swap and Share platform for our college community. This platform allows seniors to share study essentials with juniors, fostering a supportive and collaborative environment. By using our platform, you agree to adhere to the following terms and conditions.

    **General Rules**
    1. **Eligibility**: Only current students, faculty, and staff are eligible to use this platform. You must have a valid college ID to register and participate.
    2. **Registration**: Users must provide accurate information during the registration process. Misrepresentation of any information may lead to suspension or termination of your account.
    3. **Product Listing**: Seniors can list study essentials such as textbooks, stationery, and other academic resources. All listings must include clear descriptions and images of the products being offered.

    **Pricing Policy**
    1. **Free Listings**: Contributors are encouraged to give study essentials for free to support their juniors.
    2. **Price Cap**: If a product is not given for free, the price should not exceed more than 50% of the original retail price of the product. This ensures affordability and fairness for all users.
    3. **Fixed Price**: Once a price is listed, the contributor cannot ask the borrower for more than the agreed amount at the time of exchange. Any attempt to increase the price after agreement is strictly prohibited.

    **Exchange Process**
    1. **Agreement**: Both parties must agree on the terms of the exchange, including the condition of the product and the price if applicable, before meeting to exchange the item.
    2. **Condition of Products**: Contributors should ensure that all items are in good, usable condition. Any defects or issues must be clearly stated in the product description.
    3. **Exchange Location**: All exchanges should take place in a safe, agreed-upon location on campus. The platform is not responsible for any issues that arise from off-campus exchanges.

    **Privacy Policy**
    1. **Data Collection**: The platform will collect and store user information for the purpose of facilitating exchanges. Personal information will not be shared with third parties without user consent.
    2. **Security**: The platform employs security measures to protect user data. However, users are responsible for maintaining the confidentiality of their account information.

    **Changes to Terms and Conditions**
    The platform reserves the right to modify these terms and conditions at any time. Users will be notified of any changes, and continued use of the platform constitutes acceptance of the updated terms.

    **Contact Information**
    For any questions or concerns regarding these terms and conditions, please contact the team.

    By using the Swap and Share platform, you agree to comply with these terms and conditions. Thank you for contributing to a supportive and collaborative college community!
    """)

if __name__ == "__main__":
    show_terms_and_conditions()
