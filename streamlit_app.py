# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(':cup_with_straw: Customize your Smoothie! :cup_with_straw:')
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name on the Smoothie')

st.write('Name on the Smoothie will be: ', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose upto 5 ingradients:', my_dataframe, max_selections=5)
if ingredient_list:

    ingredients_string = ''
    for  fruits_chosen in ingredient_list:
        ingredients_string += fruits_chosen + ' '
    #st.write(ingredients_string)
    
    my_insert_stmt = """Insert into Smoothies.public.orders(ingredients,name_on_order)
    values('""" +ingredients_string +"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/figs")
st.text(smoothiefroot_response.json())
