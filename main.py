import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Set up the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Streamlit UI
st.title("Name Collector")

# Input for name
name = st.text_input("Enter your name:")

# Submit button
if st.button("Submit"):
    if name:
        # Fetch existing data
        sheet_data = conn.read()
        st.write(sheet_data)
        # Append new row
        new_row = pd.DataFrame({"Name": name})
        
        # Update Google Sheet
        conn.update(data=new_row)
        st.cache_data.clear()
        st.rerun()

        
        st.success(f"Thanks {name}, your name has been added to the sheet!")
    else:
        st.error("Please enter a name before submitting.")
