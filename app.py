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
        st.session_state.home_page = False
        st.session_state.product_page = True
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
                    else:
                        st.write("Wrong email or password, please try again")

    # PRODUCT PAGE (user is already logged in)
    if st.session_state.product_page:
        with st.sidebar:
            st.text(f"Welcome to the StreamQL Shop, {st.session_state.name} {st.session_state.last_name}")
            st.text(f"You've logged in with your email: {st.session_state.email}")
            # TO DO: SHOW PREVIOUS ORDERS
        products_df = displayproducts(engine)
        updatecart(products_df)


        # TO DO: show products

        # TO DO: add to cart

        # TO DO: buy

    # TO DO: user bought something
        # to do: come back to product page

    

def signup(engine, first_name, last_name, email, password):
    with engine.connect() as connection:
        txt = f'''INSERT INTO customers (first_name, last_name, email, password)
                  VALUES ("{first_name}", "{last_name}", "{email}", "{password}");'''
        query = text(txt)
        connection.execute(query)
        connection.commit()
        return True

def login(engine, email, password):
    #to do
    pass

def displayproducts(engine):
    # Load data
    with engine.connect() as connection:
        query = text("SELECT * FROM products;")
        result = connection.execute(query)
        df = pd.DataFrame(result.all())
    
    # Show products table
    st.subheader("Available products:")
    st.dataframe(df)

    # Product and quantity dropdown
    st.subheader("Buy now!")
    left, right = st.columns(2)
    product_chosen = left.selectbox("Choose a product", [x for x in df["name"]])
    with engine.connect() as connection:
        txt = f'''SELECT stock
                  FROM products
                  WHERE name = "{product_chosen}";'''
        query = text(txt)
        result = connection.execute(query)
        stock = result.scalar_one()
    quantity_chosen = right.selectbox("Choose a quantity", [x for x in range(1, stock+1)])

    return df

def showorders():
     # to do
     pass

def buy():
    #to do
    pass

def updatecart(df):
    # Add to cart
    left, center, right = st.columns(3)
    if right.button("Add to cart"):
        prod_id = df[df["name"] == product_chosen]["product_id"]
        prod_price = df[df["name"] == product_chosen]["price"]
        prod_total = prod_price * quantity_chosen
        st.session_state.cart[prod_id] = [
            product_chosen, 
            f"Quantity: {quantity_chosen}", 
            f"Price: {prod_price}", 
            f"Product Total: {prod_total}"]

def updatewishlist():
    # to do
    pass

if __name__ == '__main__':
    main()