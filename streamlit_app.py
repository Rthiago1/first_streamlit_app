import streamlit
import pandas as pd
import snowflake.connector
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect('Pick some fruits:',list(my_fruit_list.index),['Avocado','Strawberries'])
fruits = streamlit.multiselect('Pick some fruits:',list(my_fruit_list.index),['Avocado','Strawberries'])
streamlit.dataframe(my_fruit_list.loc[fruits])
#streamlit.text('Fruits Selected:',fruits)

# New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
# Normalize raw json data
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# transforms normalized fruityvice_response data into a dataframe
streamlit.dataframe(fruityvice_normalized)
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_rows)


#streamlit.dataframe(my_fruit_list)
