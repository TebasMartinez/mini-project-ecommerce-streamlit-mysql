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
    loggedin = False
    while loggedin == False:
        left, right = st.columns(2) # creates 2 columns

        # Left button, sign up
        # if left.button("Sign Up"):
        st.header("Sign Up")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last name")
        email = st.text_input("Email")
        password = st.text_input("Password")
        if st.button("Submit"):
            signup(engine, first_name, last_name, email, password)

        # Right button, log in
        if right.button("Log in"):
            st.header("Log in")
            email = st.text_input("Enter your email")
            password = st.text_input("Enter your password")

        # once logged in
        loggedin = True

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

def login():
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