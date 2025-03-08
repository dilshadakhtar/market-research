import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Set up the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Streamlit UI
st.title("Food Habits Survey")

# Demographic Questions
st.header("Demographic Information")

age_group = st.radio("What is your age group?", ["18–25", "26–40", "41–55", "56+"])

occupation = st.selectbox("What is your occupation?", [
    "Student", "Working Professional [WFO/Hybrid]", "Working Professional [WFH]", "Business Owner", "Other (Please specify)"
])

city = st.text_input("Which city do you belong to?")

marital_status = st.radio("What is your marital status?", ["Single", "Married"])

family_size = st.radio("What is your family size?", [
    "1 (Living alone)", "2–3 members", "4–5 members", "6+ members"
])

gender = st.radio("What is your gender?", [
    "Male", "Female", "Non-binary/Third gender", "Prefer not to say"
])

# Food Habits Questions
st.header("Food Habits")

dining_frequency = st.radio("How often do you dine out or order food (takeout/delivery) in a typical month?", [
    "1–2 times", "3–4 times", "5–6 times", "7+ times"
])

preference = st.radio("Which option do you prefer the most?", [
    "Dine-in experience", "Take away", "Delivery", "No preference"
])

dine_spend = st.radio("How much do you typically spend on dining out in a single order?", [
    "< 500", "501 - 1000", "1001 - 2000", "2000+"
])

delivery_spend = st.radio("How much do you typically spend on delivery/takeaway in a single order?", [
    "< 500", "501 - 1000", "1001 - 2000", "2000+"
])

influence = st.radio("Who influences your decisions the most?", [
    "Myself", "Children", "Parents", "Friends/Peers", "Spouse/Partner"
])

online_reviews = st.radio("How often do you check online reviews before selecting a restaurant?", [
    "Always", "Often", "Sometimes", "Rarely", "Never"
])

changed_mind = st.radio("Have you ever changed your mind about a restaurant due to negative online reviews?", [
    "Yes, frequently", "Yes, occasionally", "No, never"
])

factors = st.multiselect("Which of these factors influence your choice of food?", [
    "Calorie counts", "Vegan/vegetarian options", "Low-carb/keto choices", 
    "Organic or locally sourced ingredients", "Gluten-free options"
])

# Submit button
if st.button("Submit"):
    # Fetch existing data
    sheet_data = conn.read()
    
    # Create DataFrame for new entry
    new_row = pd.DataFrame([[
        age_group, occupation, city, marital_status, family_size, gender,
        dining_frequency, preference, dine_spend, delivery_spend, 
        influence, online_reviews, changed_mind, ", ".join(factors)
    ]], columns=[
        "Age Group", "Occupation", "City", "Marital Status", "Family Size", "Gender",
        "Dining Frequency", "Preference", "Dine-out Spend", "Delivery Spend", 
        "Influencer", "Online Reviews", "Changed Mind", "Food Factors"
    ])
    
    # Append new row to existing data
    updated_data = pd.concat([sheet_data, new_row], ignore_index=True)
    
    # Update Google Sheets
    conn.update(data=updated_data)
    st.cache_data.clear()
    st.rerun()
    
    st.success("Thank you for completing the survey!")
