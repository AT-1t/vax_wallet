import streamlit as st
import pandas as pd




import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("💉 Vax Wallet - Personal Vaccine Tracker")

# Initialize vaccine record CSV if not exists
if not os.path.exists("vaccine_records.csv"):
    df = pd.DataFrame(columns=["Name", "DOB", "Vaccine", "Date", "Doctor"])
    df.to_csv("vaccine_records.csv", index=False)

# Load existing data
df = pd.read_csv("vaccine_records.csv")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Add Record", "View Records", "Upload Consent Form", "About"])

# Add Record
if menu == "Add Record":
    st.subheader("➕ Add New Vaccine Record")

    name = st.text_input("Child's Full Name")
    dob = st.date_input("Date of Birth")
    vaccine = st.text_input("Vaccine Name (e.g., MMR, Tdap)")
    date = st.date_input("Vaccination Date")
    doctor = st.text_input("Doctor's Name")

    if st.button("Save Record"):
        new_data = pd.DataFrame([[name, dob, vaccine, date, doctor]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("vaccine_records.csv", index=False)
        st.success("✅ Record saved successfully!")

# View Records
elif menu == "View Records":
    st.subheader("📋 Vaccine Records")
    st.dataframe(df)

# Upload Consent Form
elif menu == "Upload Consent Form":
    st.subheader("📤 Upload Signed Consent Form")
    uploaded_file = st.file_uploader("Choose a signed consent form (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])

    if uploaded_file:
        save_path = os.path.join("consent_forms", uploaded_file.name)
        os.makedirs("consent_forms", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ File uploaded and saved successfully!")

# About
elif menu == "About":
    st.markdown("""
    ### 🧬 About Vax Wallet
    Vax Wallet helps parents:
    - Keep track of vaccinations
    - Upload consent forms signed by doctors
    - View and organize records easily

    Future features will include:
    - Moderated forums
    - Verified vaccine updates
    - De-identified public health data

    💡 Made by a beginner Python developer with a passion for health and safety.
    """)












