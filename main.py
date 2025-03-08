import streamlit as st
import pandas as pd
import re
import random
from streamlit_gsheets import GSheetsConnection
from streamlit_sortables import sort_items
from streamlit_star_rating import st_star_rating

# Set up the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Streamlit UI with custom styling
st.markdown("""
    <style>
        .main {background-color: #f4f4f8;}
        h1 {color: #4CAF50; text-align: center;}
        h2 {color: #333366;}
        .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px; font-size: 16px; padding: 10px 24px;}
        .stRadio > div {background-color: #ffffff; padding: 10px; border-radius: 10px;}
        .stSelectbox > div {background-color: #ffffff; padding: 10px; border-radius: 10px;}
        .stTextInput > div {background-color: #ffffff; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Food Habits Survey")

st.markdown("""
    Welcome to our food habits survey! Your responses will help us better understand dining preferences. 
    Please answer the following questions thoughtfully.
""")

email = st.text_input("**Enter your email (optional):**")

# Demographic Questions
st.header("📊 Demographic Information")

age_group = st.radio("**What is your age group?**", ["18–25", "26–40", "41–55", "56+"])

occupation = st.selectbox("**What is your occupation?**", [
    "Student", "Working Professional [WFO/Hybrid]", "Working Professional [WFH]", "Business Owner", "Other (Please specify)"
])

city = st.text_input("**Which city do you belong to?**")

marital_status = st.radio("**What is your marital status?**", ["Single", "Married"])

family_size = st.radio("**What is your family size?**", [
    "1 (Living alone)", "2–3 members", "4–5 members", "6+ members"
])

gender = st.radio("**What is your gender?**", [
    "Male", "Female", "Non-binary/Third gender", "Prefer not to say"
])


# Email validation
def is_valid_email(email):
    if not email:
        return True  # Optional field
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Food Habits Questions
st.header("🍽️ Food Habits")

dining_frequency = st.radio("**How often do you dine out or order food (takeout/delivery) in a typical month?**", [
    "1–2 times", "3–4 times", "5–6 times", "7+ times"
])

preference = st.radio("**Which option do you prefer the most?**", [
    "Dine-in experience", "Take away", "Delivery", "No preference"
])

dine_spend = st.radio("**How much do you typically spend on dining out in a single order?**", [
    "< 500", "501 - 1000", "1001 - 2000", "2000+"
])

delivery_spend = st.radio("**How much do you typically spend on delivery/takeaway in a single order?**", [
    "< 500", "501 - 1000", "1001 - 2000", "2000+"
])

influence = st.radio("**Who influences your decisions the most?**", [
    "Myself", "Children", "Parents", "Friends/Peers", "Spouse/Partner"
])

online_reviews = st.radio("**How often do you check online reviews before selecting a restaurant?**", [
    "Always", "Often", "Sometimes", "Rarely", "Never"
])

# Ranking factors
st.write("**Rank the following factors that influence your choice between dine-in and take away/delivery:**")
ranking_choices = [
    "Time constraints",
    "Social experience",
    "Convenience of home dining",
    "Ambiance and service quality",
    "Health concerns (e.g., avoiding crowded places)"
]
ranked_preferences = sort_items(ranking_choices)

# Star ratings
st.write("**Rate the following factors that influence your decision on where to eat (1⭐ = Least Important, 5⭐ = Most Important):**")
decision_factors = [
    "Past Experience", "Online reviews (Google, Yelp, Zomato)", "Social media (Instagram, TikTok, YouTube)",
    "Word of mouth", "Promotions/Discounts", "Location of restaurants"
]

star_ratings = {factor: st_star_rating(label=factor, maxValue=5, defaultValue=0) for factor in decision_factors}

star_ratings_str = ", ".join([f"{factor}: {rating}" for factor, rating in star_ratings.items()])


changed_mind = st.radio("**Have you ever changed your mind about a restaurant due to negative online reviews?**", [
    "Yes, frequently", "Yes, occasionally", "No, never"
])

factors = st.multiselect("**Which of these factors influence your choice of food?**", [
    "Calorie counts", "Vegan/vegetarian options", "Low-carb/keto choices", 
    "Organic or locally sourced ingredients", "Gluten-free options"
])

@st.dialog("🌟 Prompt Engineering Tip 🌟 ")
def tip():
    st.write("**Struggling to get the right answer from GPT?**")
    st.write("Try adding this simple instruction at the start of your question:")
    st.markdown("### *Take a deep breath, solve the problem step by step:*")
    st.info("This helps GPT slow down and think through each part of the problem carefully, just like a person would. As it encourages the model to break down the problem into manageable steps—mimicking the detailed reasoning often found in its training data—which can lead to more accurate and comprehensive answers.")
    st.write("**See the difference:**")
    st.write(" *Before using the prompt:* GPT gave the wrong answer.")
    st.image("Before.png", "Before Adding the Prompt")
    st.write("✅ *After using the prompt:* GPT provided the correct answer.")
    st.image("After1.png")
    st.image("After2.png", "After Adding the Prompt")
    st.link_button("Read More", "https://arxiv.org/pdf/2309.03409")

# Submit button
if st.button("Submit ✅"):
    if not (age_group and occupation and city and marital_status and family_size and gender and dining_frequency and preference and dine_spend and delivery_spend and influence and online_reviews and changed_mind and factors):
        st.error("⚠️ Please fill out all mandatory fields before submitting.")
    elif not is_valid_email(email):
        st.error("📧 Please enter a valid email address.")
    else:
        # Fetch existing data
        sheet_data = conn.read()
        
        # Create DataFrame for new entry
        new_row = pd.DataFrame([[
            age_group, occupation, city, marital_status, family_size, gender, email,
            dining_frequency, preference, dine_spend, delivery_spend, 
            influence, online_reviews, ranked_preferences, star_ratings_str, changed_mind, ", ".join(factors)
        ]], columns=[
            "Age Group", "Occupation", "City", "Marital Status", "Family Size", "Gender", "Email",
            "Dining Frequency", "Preference", "Dine-out Spend", "Delivery Spend", 
            "Influencer", "Online Reviews", "Preferences", "Influencing-Factor", "Changed Mind", "Food Factors"
        ])
        
        # Append new row to existing data
        updated_data = pd.concat([sheet_data, new_row], ignore_index=True)
        
        # Update Google Sheets
        conn.update(data=updated_data)
        st.cache_data.clear()
        st.success("🎉 Thank you for completing the survey! Your feedback means a lot.")
        st.balloons()
        tip()
