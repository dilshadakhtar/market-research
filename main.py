import streamlit as st
import pandas as pd
import re
import random
from streamlit_gsheets import GSheetsConnection
from streamlit_sortables import sort_items
from streamlit_star_rating import st_star_rating

# Set up the connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Custom styling
st.markdown("""
    <style>
        .main {background-color: #f9f9f9; font-family: Arial, sans-serif;}
        h1 {color: #2D6A4F; text-align: center; font-size: 2.8em;}
        h2 {color: #1B4332; font-size: 2em;}
        .step-header {background-color: #2D6A4F; color: white; padding: 10px; border-radius: 10px; font-size: 1.2em; margin-bottom: 20px;}
        .stButton>button {background-color: #2D6A4F; color: white; border-radius: 12px; font-size: 18px; padding: 12px 30px;}
        .stRadio > div, .stSelectbox > div, .stTextInput > div {background-color: #ffffff; padding: 12px; border-radius: 12px;}
        .stCheckbox > label {font-size: 1.1em;}
        .question {font-size: 1.5em; font-weight: bold; color: #2D6A4F;}
        .highlight {border: 2px solid red !important; border-radius: 12px; padding: 10px;}
        .scale-label {display: flex; justify-content: space-between; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🌿 Food Habits Survey")

st.markdown("<div class='h2'>Welcome to our Marketing Research survey!  ?</div>", unsafe_allow_html=True)

email = st.text_input("**Enter your email (optional):**")

# Demographic Questions
st.header("📊 Demographic Information")

st.markdown("<div class='question'>Q1: What is your age group?</div>", unsafe_allow_html=True)
age_group = st.radio("", ["18–25", "26–40", "41–55", "56+"], index=None, key='age_group')

st.markdown("<div class='question'>Q2: What is your occupation?</div>", unsafe_allow_html=True)
occupation = st.selectbox("", ["Student", "Working Professional [WFO/Hybrid]", "Working Professional [WFH]", "Business Owner", "Other"],index=None, key='occupation')

st.markdown("<div class='question'>Q3: Which city do you belong to?</div>", unsafe_allow_html=True)
city = st.text_input("", key='city')

st.markdown("<div class='question'>Q4: What is your marital status?</div>", unsafe_allow_html=True)
marital_status = st.radio("", ["Single", "Married"],index=None, key='marital_status')

st.markdown("<div class='question'>Q5: What is your family size?</div>", unsafe_allow_html=True)
family_size = st.radio("", ["1 (Living alone)", "2–3 members", "4–5 members", "6+ members"],index=None, key='family_size')

st.markdown("<div class='question'>Q6: What is your gender?</div>", unsafe_allow_html=True)
gender = st.radio("", ["Male", "Female", "Non-binary/Third gender", "Prefer not to say"],index=None, key='gender')

# Email validation
def is_valid_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Food Habits Questions
st.header("🍽️ Food Habits")

st.markdown("<div class='question'>Q1: How often do you dine out or order food in a typical month?</div>", unsafe_allow_html=True)
dining_frequency = st.radio("", ["1–2 times", "3–4 times", "5–6 times", "7+ times"],index=None, key='dining_frequency')

st.markdown("<div class='question'>Q2: What is your preferred option?</div>", unsafe_allow_html=True)
preference = st.radio("", ["Dine-in", "Takeaway", "Delivery", "No preference"],index=None, key='preference')


st.markdown("<div class='question'>Q3: How much do you typically spend on dining out in a single order?</div>", unsafe_allow_html=True)
dine_spend = st.radio("", ["< 500", "501 - 1000", "1001 - 2000", "2000+"],index=None, key='dine_spend')

st.markdown("<div class='question'>Q4: How much do you typically spend on  delivery/takeaway in a single order?</div>", unsafe_allow_html=True)
delivery_spend = st.radio("", ["< 500", "501 - 1000", "1001 - 1500", "1500+"],index=None, key='delivery_spend')

st.markdown("<div class='question'>Q5: Who influences your decisions the most?</div>", unsafe_allow_html=True)
influence = st.radio("", ["Myself", "Children", "Parents", "Friends/Peers", "Spouse/Partner"],index=None, key='influence')

st.markdown("<div class='question'>Q6: How often do you check online reviews before selecting a restaurant?</div>", unsafe_allow_html=True)
online_reviews = st.radio("", ["Always", "Often", "Sometimes", "Rarely", "Never"],index=None, key='online_reviews')


# Ranking factors
st.markdown("<div class='question'>Q7: Rate the following factors that influence your choice between dine-in and take away/delivery (1⭐ = Least Important, 5⭐ = Most Important):</div>", unsafe_allow_html=True)
ranking_choices = [
    "Time constraints",
    "Social experience",
    "Convenience of home dining",
    "Ambiance and service quality",
    "Health concerns (e.g., avoiding crowded places)"
]

inlfuence = {factor: st_star_rating(label=factor, maxValue=5, defaultValue=0) for factor in ranking_choices}

inlfuence_str = ", ".join([f"{factor}: {rating}" for factor, rating in inlfuence.items()])


# Star ratings
st.markdown("<div class='question'>Q8: Rate the following factors that influence your decision on where to eat (1⭐ = Least Important, 5⭐ = Most Important):</div>", unsafe_allow_html=True)
decision_factors = [
    "Past Experience", "Online reviews (Google, Yelp, Zomato)", "Social media (Instagram, TikTok, YouTube)",
    "Word of mouth", "Promotions/Discounts", "Location of restaurants"
]
star_ratings = {factor: st_star_rating(label=factor, maxValue=5, defaultValue=0) for factor in decision_factors}
star_ratings_str = ", ".join([f"{factor}: {rating}" for factor, rating in star_ratings.items()])


st.markdown("<div class='question'>Q9:Have you ever changed your mind about a restaurant due to negative online reviews?</div>", unsafe_allow_html=True)
changed_mind = st.radio("", ["Yes, frequently", "Yes, occasionally", "No, never"],index=None, key='changed_mind')

st.markdown("<div class='question'>Q10: Which of these factors influence your choice of food? Select all that apply.</div>", unsafe_allow_html=True)
options = {
    "Calorie counts": st.checkbox("Calorie counts"),
    "Vegan/vegetarian options": st.checkbox("Vegan/vegetarian options"),
    "Low-carb/keto choices": st.checkbox("Low-carb/keto choices"),
    "Organic or locally sourced ingredients": st.checkbox("Organic or locally sourced ingredients"),
    "Gluten-free options": st.checkbox("Gluten-free options"),
    "None of the above": st.checkbox("None of the above")
}

# Collect selected options
factors = [option for option, checked in options.items() if checked]
print(factors)

# Validation check
def validate_fields():
    errors = []
    if not age_group: errors.append("Age group")
    if not occupation: errors.append("Occupation")
    if not city.strip(): errors.append("City")
    if not marital_status: errors.append("Marital status")
    if not family_size: errors.append("Family Size")
    if not gender: errors.append("Gender")
    if not dining_frequency: errors.append("Dining frequency")
    if not preference: errors.append("Preference")
    if not dine_spend: errors.append("Dine Spend")
    if not delivery_spend: errors.append("Delivery Spend")
    if not influence: errors.append("Influence")
    if not online_reviews: errors.append("Online reviews")
    if not changed_mind: errors.append("Changed mind")
    return errors


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
    errors = validate_fields()
    if errors:
        st.error(f"Please fill out the following fields: {', '.join(errors)}")
    elif not is_valid_email(email):
        st.error("📧 Please enter a valid email address.")
    else:
        # Fetch existing data
        sheet_data = conn.read()
        
        # Create DataFrame for new entry
        new_row = pd.DataFrame([[
            email, age_group, occupation, city, marital_status, family_size, gender, 
            dining_frequency, preference, dine_spend, delivery_spend, 
            influence, online_reviews, inlfuence_str, star_ratings_str, changed_mind, ", ".join(factors)
        ]], columns=[
             "Email", "Age Group", "Occupation", "City", "Marital Status", "Family Size", "Gender",
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
