import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

# HOME PAGE FUNCTIONS 
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
            customer_id = row[0]
            first_name = row[1]
            last_name = row[2]
            return True, first_name, last_name, customer_id
        else:
            return False, "", "", ""

# USER FUNCTIONALITIES FUNCTION
def user_sidebar():
    with st.sidebar:
        st.text(f"Welcome to the StreamQL Shop, {st.session_state.name} {st.session_state.last_name}")
        st.text(f"You've logged in with your email: {st.session_state.email}")
        # TO DO: SHOW PREVIOUS ORDERS

def showorders():
     # to do
     pass

# PRODUCT PAGE FUNCTIONS
def displayproducts(engine):
    # Load data
    with engine.connect() as connection:
        query = text("SELECT * FROM products;")
        result = connection.execute(query)
        df = pd.DataFrame(result.all())
        df.rename(columns={"price":"price €"}, inplace=True)
    
    # Show products table
    st.subheader("Available products:")
    st.dataframe(df)

    return df

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

    # Add to cart button
    left, center, right = st.columns(3)
    if right.button("Add to cart"):
        prod_id = df[df["name"] == product_chosen]["product_id"].values[0]
        prod_price = df[df["name"] == product_chosen]["price €"].values[0]
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
        for product in st.session_state.cart:
            prod_name = st.session_state.cart[product][0]
            prod_qnty = float(st.session_state.cart[product][1])
            prod_price = float(st.session_state.cart[product][2])
            prod_total = round(st.session_state.cart[product][3], 2)
            st.write(f"You have {int(prod_qnty)} {prod_name} in your cart, each of them costs {prod_price}€, the total for this product type in the cart is {prod_total}€")
            st.divider()
        cart_total = calc_cart_total()
        st.write(f"THE TOTAL OF YOUR ORDER IS: {cart_total}€")

def buy(engine):
    if st.button("Buy"):
        if st.session_state.cart == {}:
            st.write("Your cart is still empty! Add something to your cart :)")
        else:
            cart_total = calc_cart_total()

            # Add new order to orders table in the database
            with engine.connect() as connection:
                txt = f'''INSERT INTO orders (order_date, order_total, customer_id)
                          VALUES (CURRENT_DATE(), "{cart_total}", "{st.session_state.cust_id}");'''
                query = text(txt)
                connection.execute(query)
                connection.commit()

            # Get the generated order ID
            with engine.connect() as connection:
                query = text('''SELECT order_id
                                FROM orders
                                ORDER BY order_id DESC
                                LIMIT 1;''')
                result = connection.execute(query)
                order_id = result.scalar()
            
            # Add rows for every product in the order to the junction table orders_products in the database
            for prod_id, prod_details in st.session_state.cart.items():
                with engine.connect() as connection:
                    txt = f'''INSERT INTO orders_products (product_id, order_id, quantity, product_total)
                              VALUES ("{prod_id}", "{order_id}", "{prod_details[1]}", "{prod_details[3]}");'''
                    query = text(txt)
                    connection.execute(query)
                    connection.commit()
            
            # Empty cart
            st.session_state.cart = {}
            
            # Move to Thank you page
            st.session_state.product_page = False
            st.session_state.thanks_page = True
            st.rerun()

# THANK YOU PAGE FUNCTIONS
def thankyou(engine):
    #to do
    pass

# COMMON USE FUNCTIONS
def calc_cart_total():
    cart_total = 0
    for product in st.session_state.cart:
        prod_total = st.session_state.cart[product][3]
        cart_total += prod_total
    return round(cart_total, 2)