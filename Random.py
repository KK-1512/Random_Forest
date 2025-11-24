import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle

st.set_page_config(page_title="Heat Treatment Hardness Prediction", layout="centered")

# ============================
# 1. Safe Model Loading
# ============================
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "hardness_model.pkl")

    if not os.path.exists(model_path):
        st.error(f"❌ Model file not found!\nExpected at: {model_path}")
        return None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model


model = load_model()

st.title("🔥 Heat Treatment Hardness Prediction Using Machine Learning")

st.write("""
This app predicts the **final hardness** (HRC) of steel after heat treatment  
based on its **chemical composition** and **process parameters**.
""")

if model is None:
    st.stop()

# ============================
# 2. Input Fields
# ============================
st.header("Enter Process & Composition Parameters")

col1, col2 = st.columns(2)

with col1:
    C = st.number_input("Carbon (C %)", 0.1, 1.0, 0.3, step=0.01)
    Mn = st.number_input("Manganese (Mn %)", 0.1, 2.0, 0.8, step=0.01)
    Si = st.number_input("Silicon (Si %)", 0.0, 1.5, 0.25, step=0.01)
    Cr = st.number_input("Chromium (Cr %)", 0.0, 3.0, 0.5, step=0.01)
    Ni = st.number_input("Nickel (Ni %)", 0.0, 2.0, 0.4, step=0.01)
    Mo = st.number_input("Molybdenum (Mo %)", 0.0, 1.0, 0.1, step=0.01)

with col2:
    AustenitizeTemp = st.number_input("Austenitizing Temperature (°C)", 700, 1100, 850)
    AustenitizeTime = st.number_input("Austenitizing Time (min)", 10, 180, 60)
    QuenchMedium = st.selectbox("Quenching Medium", ["Water", "Oil", "Polymer"])
    TemperingTemp = st.number_input("Tempering Temperature (°C)", 100, 700, 300)
    TemperingTime = st.number_input("Tempering Time (min)", 10, 240, 90)

# ============================
# 3. Predict Button
# ============================
if st.button("Predict Hardness"):
    input_data = pd.DataFrame([[
        C, Mn, Si, Cr, Ni, Mo,
        AustenitizeTemp, AustenitizeTime,
        QuenchMedium,
        TemperingTemp, TemperingTime
    ]], columns=[
        "C","Mn","Si","Cr","Ni","Mo",
        "AustenitizeTemp","AustenitizeTime",
        "QuenchMedium",
        "TemperingTemp","TemperingTime"
    ])

    prediction = model.predict(input_data)[0]

    st.success(f"### 🔧 Predicted Hardness: **{prediction:.2f} HRC**")
