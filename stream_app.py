import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruit_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # normalize the DF
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display the normalised DF on  https://demostreamapp-800odtu4mhh.streamlit.app/
    return fruityvice_normalized

def get_fruit_load_list(csr):
    with csr.cursor() as my_cur:
        my_cur.execute("insert into FRUIT_LOAD_LIST values('from streamlit')")
        return my_cur.fetchall()

streamlit.title('diner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('kindly select a fruit')
    else:
        fruit_data = get_fruit_data(fruit_choice)
        streamlit.dataframe(fruit_data)

except URLError as e:
    streamlit.error()


streamlit.header("This Fruit Load list contains:")

# add a button to UI
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list(my_cnx)
    streamlit.dataframe(my_data_row)




add_fruit = streamlit.text_input('What fruit would you like to add', "jackfruit")
streamlit.write('Thanks for adding ', add_fruit)
