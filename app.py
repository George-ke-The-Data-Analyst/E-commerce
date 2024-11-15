import streamlit as st
import pandas as pd
import pickle

# Load data and model
data = pd.read_csv('Us-Ecommerce Dataset.csv')
with open('E-commerce_Recommender_System.pkl', 'rb') as file:
    model = pickle.load(file)

# Handle Cold-Start Problem: recommend popular products for new users
def get_cold_start_recommendations():
    popular_products = data['Product'].value_counts().head(10).index.tolist()
    return popular_products

# Get products already bought by a customer
def get_customer_purchase_history(customer_id):
    customer_data = data[data['customer_id'] == customer_id]
    purchased_products = customer_data['Product'].unique().tolist()
    return purchased_products

# Get recommendations for an existing customer based on their purchase history
def get_user_recommendations(customer_id):
    # For simplicity, recommending other products except what the user already bought
    purchased_products = get_customer_purchase_history(customer_id)
    recommended_products = data[~data['Product'].isin(purchased_products)]['Product'].value_counts().head(10).index.tolist()
    return recommended_products

# Handle User Feedback
def save_feedback(customer_id, product, rating):
    feedback = {'customer_id': customer_id, 'product': product, 'rating': rating}
    # Save feedback logic (e.g., store in database or CSV)

# Display Privacy Policy
def show_privacy_policy():
    if st.checkbox("I agree to the privacy policy"):
        return True
    else:
        st.warning("You must agree to the privacy policy to use the app.")
        return False

# Streamlit UI
st.title("Product Recommender")

# Show Privacy Policy and ensure user agreement
if not show_privacy_policy():
    st.stop()  # Stop the app until user agrees to privacy policy

# Customer ID Input
customer_id = st.number_input("Enter Customer ID", min_value=0)

# If customer has made purchases, show their history and recommendations
if customer_id in data['customer_id'].unique():
    st.write(f"Customer {customer_id}'s Purchase History:")
    purchased_products = get_customer_purchase_history(customer_id)
    st.write(purchased_products)

    # Get product recommendations based on the customer's purchase history
    if st.button("Get Recommendations"):
        recommendations = get_user_recommendations(customer_id)
        st.write(f"Recommended products for Customer {customer_id}:")
        st.write(recommendations)

        # Allow user feedback
        selected_product = st.selectbox("Rate a recommended product", recommendations)
        user_rating = st.slider('Rate this product (1-10)', 1, 10)

        if st.button("Submit Rating"):
            save_feedback(customer_id, selected_product, user_rating)
            st.success("Your feedback has been saved!")

# If the customer is new or ID does not exist, recommend cold-start products
else:
    st.write("New Customer or Customer ID not found.")
    recommendations = get_cold_start_recommendations()
    st.write("Recommended for you:")
    st.write(recommendations)

# Option to save the app data (feedback)
if st.button("Save Feedback Data"):
    st.write("Feedback data has been saved.")