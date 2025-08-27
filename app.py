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

    

def signup(engine, first_name, last_name, email, password):
    with engine.connect() as connection:
        txt = f'''INSERT INTO customers (first_name, last_name, email, password)
                  VALUES ("{first_name}", "{last_name}", "{email}", "{password}");'''
        query = text(txt)
        connection.execute(query)
        connection.commit()
        return True

def login(engine, email, password):
    with engine.connect() as connection:
        txt = f'''SELECT customer_id, first_name, last_name, email, password
          FROM customers
          WHERE email = "{email}" AND password = "{password}" LIMIT 1;'''
        query = text(txt)
        result = connection.execute(query)
        row = result.fetchone() # fetchone() gives us one row if the email+password exists, or None if not
        if row is not None:
            return True
        else:
            return False

def displayproducts(engine):
    # Load data
    with engine.connect() as connection:
        query = text("SELECT * FROM products;")
        result = connection.execute(query)
        df = pd.DataFrame(result.all())
    
    # Show products table
    st.subheader("Available products:")
    st.dataframe(df)

    return df

def showorders():
     # to do
     pass

def buy():
    #to do
    pass

def updatecart(engine, df):
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

    # Add to cart
    left, center, right = st.columns(3)
    if right.button("Add to cart"):
        prod_id = df[df["name"] == product_chosen]["product_id"].values[0]
        prod_price = df[df["name"] == product_chosen]["price"].values[0]
        prod_total = prod_price * quantity_chosen
        st.session_state.cart[prod_id] = [
            product_chosen, 
            quantity_chosen, 
            prod_price, 
            prod_total]
        
def showcart():
    st.subheader("Your cart:")
    if st.session_state.cart == {}:
        st.write("Your cart is currently empty. Add something to the cart!")
    else:
        grand_total = 0
        for product in st.session_state.cart:
            prod_name = st.session_state.cart[product][0]
            prod_qnty = float(st.session_state.cart[product][1])
            prod_price = float(st.session_state.cart[product][2])
            prod_total = st.session_state.cart[product][3]
            grand_total += prod_price * prod_qnty
            st.write(f"You have {prod_qnty} {prod_name} in your cart, each of them costs {prod_price}, the total for this product type in the cart is {prod_total}")
            st.divider()
        st.write(f"THE TOTAL OF YOUR ORDER IS: {grand_total}")

def updatewishlist():
    # to do
    pass

if __name__ == '__main__':
    main()