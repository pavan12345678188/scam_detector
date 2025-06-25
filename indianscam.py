import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import pickle


df=pd.read_csv("indian_scam_dataset.csv")
# Load the trained model
with open("best_model.pkl", "rb") as file:
    model = pickle.load(file)

# Manual encoding maps based on cleaned dataset (already encoded values)
card_type_map = {"MasterCard": 0, "Rupay": 1, "Visa": 2}
location_map = {
    "Ahmedabad": 0, "Bangalore": 1, "Chennai": 2, "Delhi": 3,
    "Hyderabad": 4, "Jaipur": 5, "Kolkata": 6, "Mumbai": 7,
    "Pune": 8, "Surat": 9
}
purchase_category_map = {"Digital": 0, "POS": 1, "Others": 2}

st.title("📊 Indian Scam Transaction Detector")
st.write("Enter transaction details to check if it's fraudulent.")

# Input fields
customer_id = st.number_input("Customer ID", min_value=0)
merchant_id = st.number_input("Merchant ID", min_value=0)
amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
transaction_time = st.slider("Transaction Time (encoded)", min_value=0, max_value=1440)
card_type = st.selectbox("Card Type", list(card_type_map.keys()))
location = st.selectbox("Transaction Location", list(location_map.keys()))
purchase_category = st.selectbox("Purchase Category", list(purchase_category_map.keys()))
customer_age = st.slider("Customer Age", min_value=18, max_value=100, step=1)

# Encode categorical values
card_type_encoded = card_type_map[card_type]
location_encoded = location_map[location]
purchase_category_encoded = purchase_category_map[purchase_category]

# Prepare input for prediction
input_data = pd.DataFrame({
    "customer_id": [customer_id],
    "merchant_id": [merchant_id],
    "amount": [amount],
    "transaction_time": [transaction_time],
    "card_type": [card_type_encoded],
    "location": [location_encoded],
    "purchase_category": [purchase_category_encoded],
    "customer_age": [customer_age]
})

# Predict button
if st.button("Check Fraud"):
    try:
        prediction = model.predict(input_data)[0]
        if prediction == 1:
            st.error("🚨 Fraudulent Transaction Detected!")
        else:
            st.success("✅ This transaction seems safe.")
    except Exception as e:
        st.warning(f"Prediction failed: {e}")
