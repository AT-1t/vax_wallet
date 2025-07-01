import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Vax Wallet", layout="centered")

# Create folders if missing
os.makedirs("profile_pics", exist_ok=True)
os.makedirs("consent_forms", exist_ok=True)

# File paths
VACCINE_RECORDS_FILE = "vaccine_records.csv"
PROFILE_DATA_FILE = "profiles.json"

# Initialize vaccine record CSV if not exists
if not os.path.exists(VACCINE_RECORDS_FILE):
    df = pd.DataFrame(columns=["Name", "DOB", "Vaccine", "Date", "Doctor"])
    df.to_csv(VACCINE_RECORDS_FILE, index=False)

# Load existing vaccine records
df = pd.read_csv(VACCINE_RECORDS_FILE)

# Load profile data from JSON or start empty
if os.path.exists(PROFILE_DATA_FILE):
    with open(PROFILE_DATA_FILE, "r") as f:
        profiles = json.load(f)
else:
    profiles = {}

# Sidebar navigation menu
menu = st.sidebar.radio("Go to", ["Profile", "Add Record", "View Records", "Upload Consent Form", "About"])

# -------- PROFILE PAGE --------
if menu == "Profile":
    st.subheader("👤 My Profile")

    # User name input (adult or child)
    user_name = st.text_input("Your Full Name")

    # Load saved profile picture if exists
    profile_pic_path = ""
    if user_name:
        pic_filename = f"{user_name.replace(' ', '_')}.png"
        profile_pic_path = os.path.join("profile_pics", pic_filename)
        if os.path.exists(profile_pic_path):
            st.image(profile_pic_path, width=200, caption="Profile Picture")

    # Upload profile picture
    profile_pic = st.file_uploader("Upload Profile Picture (JPG or PNG)", type=["jpg", "jpeg", "png"])

    # Vaccines list
    vaccines = [
        "MMR (Measles, Mumps, Rubella)",
        "DTaP (Diphtheria, Tetanus, Pertussis)",
        "Polio (IPV)",
        "Hepatitis B",
        "Hib (Haemophilus influenzae type b)",
        "Varicella (Chickenpox)",
        "COVID-19",
    ]

    # Load saved vaccine checklist for user or empty list
    saved_vaccines = []
    if user_name and user_name in profiles:
        saved_vaccines = profiles[user_name].get("vaccines", [])

    st.markdown("### Vaccination Status")
    completed_vaccines = []
    for vaccine in vaccines:
        checked = vaccine in saved_vaccines
        if st.checkbox(vaccine, value=checked):
            completed_vaccines.append(vaccine)

    if st.button("Save Profile"):
        if not user_name:
            st.error("Please enter your full name to save profile.")
        else:
            # Save profile picture if uploaded
            if profile_pic:
                with open(profile_pic_path, "wb") as f:
                    f.write(profile_pic.getbuffer())

            # Save vaccine checklist in profiles dict
            profiles[user_name] = {
                "vaccines": completed_vaccines
            }
            with open(PROFILE_DATA_FILE, "w") as f:
                json.dump(profiles, f, indent=4)

            st.success(f"✅ Profile for {user_name} saved successfully!")

# -------- ADD RECORD PAGE --------
elif menu == "Add Record":
    st.subheader("➕ Add New Vaccine Record")

    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    vaccine = st.text_input("Vaccine Name (e.g., MMR, Tdap)")
    date = st.date_input("Vaccination Date")
    doctor = st.text_input("Doctor's Name")

    if st.button("Save Record"):
        if not name or not vaccine:
            st.error("Please enter both Name and Vaccine Name.")
        else:
            new_data = pd.DataFrame([[name, dob, vaccine, date, doctor]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(VACCINE_RECORDS_FILE, index=False)
            st.success("✅ Record saved successfully!")

# -------- VIEW RECORDS PAGE --------
elif menu == "View Records":
    st.subheader("📋 Vaccine Records")
    st.dataframe(df)

# -------- UPLOAD CONSENT FORM PAGE --------
elif menu == "Upload Consent Form":
    st.subheader("📤 Upload Signed Consent Form")
    uploaded_file = st.file_uploader("Choose a signed consent form (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])

    if uploaded_file:
        save_path = os.path.join("consent_forms", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("✅ File uploaded and saved successfully!")

# -------- ABOUT PAGE --------
elif menu == "About":
    st.markdown("""
    ### 🧬 About Vax Wallet
    Vax Wallet helps users:
    - Keep track of vaccinations
    - Upload consent forms signed by doctors
    - View and organize records easily

    Future features will include:
    - Moderated forums
    - Verified vaccine updates
    - De-identified public health data

    💡 Made by a beginner Python developer with a passion for health and safety.
    """)
