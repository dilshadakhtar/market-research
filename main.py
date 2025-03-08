import streamlit as st
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
        
        # Append new row
        new_row = {"Name": name}
        sheet_data = sheet_data.append(new_row, ignore_index=True)
        
        # Update Google Sheet
        conn.update(sheet_data)
        
        st.success(f"Thanks {name}, your name has been added to the sheet!")
    else:
        st.error("Please enter a name before submitting.")
