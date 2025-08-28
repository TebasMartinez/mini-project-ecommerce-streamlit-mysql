import functions as f
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

def main():
    st.title("StreamQL Shop")

    # Connect to database
    db = st.secrets["mysql"]
    engine = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}/{db.database}")

    # Session set up
    if "home_page" not in st.session_state:
        # page structure
        st.session_state.home_page = True
        st.session_state.product_page = False
        st.session_state.thanks_page = False
        # buttons / forms
        st.session_state.show_signup_form = False
        st.session_state.show_login_form = False
        st.session_state.show_orders = False
        # session variables and dict
        st.session_state.name = ""
        st.session_state.last_name = ""
        st.session_state.email = ""
        st.session_state.cart = {}
        st.session_state.cust_id = ""
        st.session_state.order_id = ""
        st.session_state.order_total = ""

    # HOME PAGE (user hasn't logged in)    
    if st.session_state.home_page:
        st.text("Please log in to see shop contents")
        with st.sidebar:
            left, right = st.columns(2) # creates 2 columns
            f.signup_button_and_form(engine, left)
            f.login_button_and_form(engine, right)
            

    # PRODUCTS PAGE (user is already logged in)
    if st.session_state.product_page:
        f.user_sidebar(engine)
        products_df = f.displayproducts(engine)
        f.updatecart(engine, products_df)
        f.showcart()
        f.buy(engine)

    # THANK YOU PAGE (user has bought something)
    if st.session_state.thanks_page:
        f.user_sidebar(engine)
        f.thankyou(engine)
        left, right = st.columns(2)
        f.backtoproducts(left)
        f.logout(right)

if __name__ == '__main__':
    main()