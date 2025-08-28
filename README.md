# Mini Project: E-commerce Store with Streamlit + MySQL

## Running this repo
Set up following the steps below is necessary to run the app in this repo:

- Create a new python enviroment and install everything in `requirements.txt`.
- Generate database in MySQL either with: 
  - forward engineering the database in `mini-project-ecommerce-streamlit-mysql.mwb`, or
  - running the queries in `create_model.sql`.
- Generate initial data for the database by running the queries in `generate_data.sql`.
- Create a folder `.streamlit` with a text file `secrets.toml` with the following structure:
````
[mysql]
host = "localhost"
database = "miniproject_ecommerce"
user = "root"
password = "your-password"
````

You're ready to run the app! 
````
streamlit run app.py
````


## Database Design
![Schema](images/schema.png)