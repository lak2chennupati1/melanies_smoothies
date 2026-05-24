# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(':cup_with_straw: Customize your Smoothie! :cup_with_straw:')
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name on the Smoothie')

st.write('Name on the Smoothie will be: ', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('Search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredient_list = st.multiselect('Choose upto 5 ingradients:', my_dataframe, max_selections=5)
if ingredient_list:
    ingredients_string = ''
    for  fruits_chosen in ingredient_list:
        ingredients_string += fruits_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME']==fruits_chosen,'SEARCH_ON'].iloc[0]
        st.write('The search value for ' , fruits_chosen, 'is ' , search_on, '.')
        st.subheader(fruits_chosen + 'Nutrition Information')
        fruityvice_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    my_insert_stmt = """Insert into Smoothies.public.orders(ingredients,name_on_order)
    values('""" +ingredients_string +"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
