import pandas as pd
import pymysql
from sqlalchemy import create_engine, text
import streamlit as st

def main():
    st.title("Mini Project: E-commerce Store with Streamlit + MySQL")

    # connect to database
    db = st.secrets["mysql"]
    engine = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}/{db.database}")


    # FIRST PAGE
    if "show_signup_form" not in st.session_state:
        st.session_state.show_signup_form = False
        st.session_state.show_login_form = False
        st.session_state.name = ""
        st.session_state.last_name = ""
        st.session_state.email = ""

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
            email = st.text_input("Enter your email")
            password = st.text_input("Enter your password", type="password")
            submitted_login = st.form_submit_button("Submit")
        if submitted_login:
            login(email, password)
            st.success("You've succesfully logged in!")
            st.session_state.show_login_form = False


    # once logged in

    # show products

    # add to cart

    # buy

    # button to show previous orders

def signup(engine, first_name, last_name, email, password):
    with engine.connect() as connection:
        txt = f'''INSERT INTO customers (first_name, last_name, email, password)
                  VALUES ("{first_name}", "{last_name}", "{email}", "{password}");'''
        query = text(txt)
        connection.execute(query)
        connection.commit()
        return True

def login(email, password):
    #to do
    pass

def displayproducts():
    #to do
    pass

def showorders():
     # to do
     pass

def buy():
    #to do
    pass

def updatecart():
    #to do
    pass

def updatewishlist():
    # to do
    pass

if __name__ == '__main__':
    main()