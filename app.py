from functions import signup, login, displayproducts, showorders, buy, updatecart, showcart
import pandas as pd
import pymysql
from sqlalchemy import create_engine, text
import streamlit as st

def main():
    st.title("StreamQL Shop")

    # Connect to database
    db = st.secrets["mysql"]
    engine = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}/{db.database}")

    # Session set up
    if "show_signup_form" not in st.session_state:
        # page structure
        st.session_state.show_signup_form = False
        st.session_state.show_login_form = False
        st.session_state.home_page = True
        st.session_state.product_page = False
        st.session_state.thanks_page = False
        # variables / dics
        st.session_state.name = ""
        st.session_state.last_name = ""
        st.session_state.email = ""
        st.session_state.cart = {}

    # HOME PAGE (user hasn't logged in)    
    if st.session_state.home_page == True:
        st.text("Please log in to see shop contents")
        with st.sidebar:
            left, right = st.columns(2) # creates 2 columns
            # SIGN UP button and form
            if not st.session_state.show_signup_form:
                if left.button("Sign Up"):
                    st.session_state.show_signup_form = True
                    st.session_state.show_login_form = False
            else:
                with st.form("signup_form"):
                    st.header("Sign Up")
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    submitted_signup = st.form_submit_button("Submit")
                if submitted_signup:
                    signup(engine, first_name, last_name, email, password)
                    st.success("User added successfully!")
                    st.session_state.show_signup_form = False

            # LOG IN button and form
            if not st.session_state.show_login_form:
                if right.button("Log in"):
                    st.session_state.show_login_form = True
                    st.session_state.show_signup_form = False
            else:
                with st.form("login_form"):
                    st.header("Log in")
                    st.session_state.email = st.text_input("Enter your email")
                    password = st.text_input("Enter your password", type="password")
                    submitted_login = st.form_submit_button("Submit")
                if submitted_login:
                    success, st.session_state.name, st.session_state.last_name = login(engine, st.session_state.email, password)
                    if success == True:
                        st.success("You've succesfully logged in!")
                        st.session_state.show_login_form = False
                        st.session_state.home_page = False
                        st.session_state.product_page = True
                        st.rerun()
                    else:
                        st.write("Wrong email or password, please try again")

    # PRODUCT PAGE (user is already logged in)
    if st.session_state.product_page:
        with st.sidebar:
            st.text(f"Welcome to the StreamQL Shop, {st.session_state.name} {st.session_state.last_name}")
            st.text(f"You've logged in with your email: {st.session_state.email}")
            # TO DO: SHOW PREVIOUS ORDERS
        products_df = displayproducts(engine)
        updatecart(engine, products_df)
        showcart()


        # TO DO: show products

        # TO DO: add to cart

        # TO DO: buy

    # TO DO: user bought something
        # to do: come back to product page

if __name__ == '__main__':
    main()