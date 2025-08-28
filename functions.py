import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

# HOME PAGE FUNCTIONS 
def signup_button_and_form(engine, position):
    if position.button("Sign Up"):
                st.session_state.show_login_form = False
                st.session_state.show_signup_form = not st.session_state.show_signup_form
                st.rerun()
    if st.session_state.show_signup_form:
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
            st.rerun()

def login_button_and_form(engine, position):
    if position.button("Log in"):
                st.session_state.show_signup_form = False
                st.session_state.show_login_form = not st.session_state.show_login_form
                st.rerun()
    if st.session_state.show_login_form:
        with st.form("login_form"):
            st.header("Log in")
            st.session_state.email = st.text_input("Enter your email")
            password = st.text_input("Enter your password", type="password")
            submitted_login = st.form_submit_button("Submit")
        if submitted_login:
            success = login(engine, st.session_state.email, password)
            if success == True:
                st.success("You've succesfully logged in!")
                st.session_state.show_login_form = False
                st.session_state.home_page = False
                st.session_state.product_page = True
                st.rerun()
            else:
                st.write("Wrong email or password, please try again.")

def signup(engine, first_name, last_name, email, password):
    txt = f'''INSERT INTO customers (first_name, last_name, email, password)
              VALUES ("{first_name}", "{last_name}", "{email}", "{password}");'''
    mod_table(engine, txt)
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
            st.session_state.cust_id = row[0]
            st.session_state.name = row[1]
            st.session_state.last_name = row[2]
            return True
        else:
            return False

# USER FUNCTIONALITIES FUNCTIONS
def user_sidebar(engine):
    with st.sidebar:
        st.text(f"Welcome to the StreamQL Shop, {st.session_state.name} {st.session_state.last_name}")
        st.text(f"You've logged in with your email: {st.session_state.email}")
        customer_rank(engine)
        left, right = st.columns(2)
        showorders(engine, left)
        logout(right)

def showorders(engine, position):
    if position.button("My Orders"):
        st.session_state.show_orders = not st.session_state.show_orders 
    if st.session_state.show_orders:
        with engine.connect() as connection:
            txt = f''' SELECT o.order_date, p.name AS product_name, op.quantity, op.product_total, o.order_id, o.order_total  
                        FROM customers c
                        JOIN orders o ON c.customer_id = o.customer_id
                        JOIN orders_products op ON o.order_id = op.order_id
                        JOIN products p ON op.product_id = p.product_id
                        WHERE c.email = '{st.session_state.email}'
                        ORDER BY o.order_id DESC
                        '''
            query = text(txt)
            result = connection.execute(query)
            df = pd.DataFrame(result.all())
        
            if len(df) > 0:
                st.dataframe(df)
            else:
                st.text("You haven't ordered anything yet. Go to the Product Page and buy something! :)")

def customer_rank(engine):
    # Get number of total customers existing
    with engine.connect() as connection:
        txt = f'''SELECT COUNT(*)
                  FROM customers;'''
        query = text(txt)
        result = connection.execute(query)
        total_customers = result.scalar_one()

    # Get total_spent and customer rank of current customer
        txt = f'''WITH total_spent AS (
                  SELECT customer_id, 
                  COALESCE(SUM(order_total), 0) AS total_spent
                  FROM customers
                  LEFT JOIN orders USING(customer_id)
                  GROUP BY customer_id),
                  total_spent_ranked AS (
                  SELECT customer_id, 
	                  total_spent,
                      DENSE_RANK() OVER (ORDER BY total_spent DESC) as rank_
                  FROM total_spent)
                  SELECT customer_id, 
                  total_spent AS "Total Spent",
	                  rank_
                  FROM total_spent_ranked
                  WHERE customer_id = {st.session_state.cust_id}
                  ORDER BY rank_, customer_id;'''
        query = text(txt)
        result = connection.execute(query)
        row = result.fetchone()
        st.subheader("Customer Rank:")
        total_spent = row[1]
        cust_rank = row[2]
        if total_spent > 0:
            if cust_rank == 1:
                st.write(f'''You're customer number {cust_rank} out of {total_customers} customers. 
                            You've spent {round(total_spent,2)}€ in the StreamQL Shop. Keep buying to stay in the top!''')
            else:
                st.write(f'''You're customer number {cust_rank} out of {total_customers} customers. 
                            You've spent {round(total_spent,2)}€ in the StreamQL Shop. Keep buying to go up in the rank!''')
        else:
            st.write("You haven't placed any order yet. Buy something to enter our customer rank!")

# PRODUCT PAGE FUNCTIONS
def displayproducts(engine):
    # Load data
    with engine.connect() as connection:
        query = text("SELECT * FROM products;")
        result = connection.execute(query)
        df = pd.DataFrame(result.all())

    # Clean data
    df.rename(columns={"price":"price €"}, inplace=True)
    df = df[df["stock"] > 0]
    
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
        if prod_id not in st.session_state.cart: # Product isn't yet in the cart
            st.session_state.cart[prod_id] = [
                product_chosen, 
                quantity_chosen, 
                prod_price, 
                prod_total]
        else: # Product is already in the cart and the user adds more
            st.session_state.cart[prod_id][1] += quantity_chosen
            st.session_state.cart[prod_id][3] = st.session_state.cart[prod_id][1] * prod_price
        st.rerun()
        
def showcart():
    st.subheader("Your cart:")
    if st.session_state.cart == {}:
        st.write("Your cart is currently empty. Add something to the cart!")
    else:
        for prod_id, product in list(st.session_state.cart.items()):
            left, right = st.columns(2)
            prod_name = product[0]
            prod_qnty = float(product[1])
            prod_price = float(product[2])
            prod_total = round(product[3], 2)
            imgpath = f"images/{prod_id}.jpg"
            left.image(imgpath, width=300)
            right.write(f"{prod_name}")
            right.write(f"Quantity: {int(prod_qnty)}")
            right.write(f"Price per unit: {prod_price}€")
            right.write(f"Total product price: {prod_total}€")
            if right.button("Remove from cart", key=f"remove_{prod_id}"):
                del st.session_state.cart[prod_id]
                st.rerun()
            st.divider()
        cart_total = calc_cart_total()
        st.markdown(f"**THE TOTAL PRICE OF YOUR CART IS: {cart_total}€**")
    
def buy(engine):
    if st.button("Buy"):
        if st.session_state.cart == {}:
            st.write("Your cart is still empty! Add something to your cart :)")
        else:
            cart_total = calc_cart_total()
            st.session_state.order_total = cart_total

            # Add new order to orders table in the database
            txt = f'''INSERT INTO orders (order_date, order_total, customer_id)
                      VALUES (CURRENT_DATE(), "{cart_total}", "{st.session_state.cust_id}");'''
            mod_table(engine, txt)

            # Get the generated order ID
            with engine.connect() as connection:
                query = text('''SELECT order_id
                                FROM orders
                                ORDER BY order_id DESC
                                LIMIT 1;''')
                result = connection.execute(query)
                order_id = result.scalar()
                st.session_state.order_id = order_id
            
            for prod_id, prod_details in st.session_state.cart.items():
                # Cart is a dictionary where for each entry the key is the product ID
                # and the value is a list with the following data, in this order:
                # Product Name, Quantity, Product Price, Product Total Price

                # Add rows for every product in the order to the junction table orders_products in the database
                txt = f'''INSERT INTO orders_products (product_id, order_id, quantity, product_total)
                          VALUES ("{prod_id}", "{order_id}", "{prod_details[1]}", "{prod_details[3]}");'''
                mod_table(engine, txt)

                # Update stock in the products table in the database
                with engine.connect() as connection:
                    txt = f'''SELECT stock
                              FROM products
                              WHERE product_id = "{prod_id}";'''
                    query = text(txt)
                    result = connection.execute(query)
                    prev_stock = result.scalar()
                new_stock = prev_stock - prod_details[1]
                txt = f'''UPDATE products
                          SET stock = "{new_stock}"
                          WHERE product_id = "{prod_id}";'''
                mod_table(engine, txt)
                
            # Empty cart
            st.session_state.cart = {}

            # Move to Thank you page
            st.session_state.product_page = False
            st.session_state.thanks_page = True
            st.rerun()

# THANK YOU PAGE FUNCTIONS
def thankyou(engine):
    st.subheader("Thank you for your order! :D")

    # Get last order data
    with engine.connect() as connection:
        txt = f'''SELECT
                    p.name AS "Product", 
	                p.price AS "Product Price",
                    op.quantity AS "Product Quantity",
                    op.product_total AS "Product Total Price"
                  FROM products AS p
                  INNER JOIN orders_products AS op USING(product_id)
                  INNER JOIN orders AS o USING(order_id)
                  WHERE order_id = {st.session_state.order_id}
                  ORDER BY order_id;'''
        query = text(txt)
        result = connection.execute(query)
        df = pd.DataFrame(result.all())
    
    df.rename(columns={"Product Total Price":"Product Total Price €"}, inplace=True)

    # Display last order data
    st.text("Here are your order details:")
    st.text(f"Order number: {st.session_state.order_id}")
    st.text(f"Order total price: {st.session_state.order_total}€")
    st.dataframe(df)

def backtoproducts(position):
    if position.button("Back to products page"):
        st.session_state.order_id = ""
        st.session_state.order_total = ""
        st.session_state.thanks_page = False
        st.session_state.home_page = False
        st.session_state.product_page = True
        st.rerun()

def logout(position):
    if position.button("Log out"):
        st.session_state.order_id = ""
        st.session_state.order_total = ""
        st.session_state.name = ""
        st.session_state.last_name = ""
        st.session_state.email = ""
        st.session_state.cust_id = ""
        st.session_state.thanks_page = False
        st.session_state.product_page = False
        st.session_state.home_page = True
        st.rerun()

# COMMON USE FUNCTIONS
def calc_cart_total():
    """
    Calculates cart total price
    """
    cart_total = 0
    for product in st.session_state.cart:
        prod_total = st.session_state.cart[product][3]
        cart_total += prod_total
    return round(cart_total, 2)

def mod_table(engine, txt):
    """
    Takes a SQL query inside a string (txt) and
    runs it in the database connected through engine
    """
    with engine.connect() as connection:
        query = text(txt)
        connection.execute(query)
        connection.commit()