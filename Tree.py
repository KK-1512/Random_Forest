import streamlit as st
import numpy as np
import pickle
import os

st.title("Decision Tree Heat Treatment Hardness Predictor")

# 🔥 Add image at top (upload the image to your repo)
st.image("LNT.jpg", use_column_width=True)

# Load model
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    model = pickle.load(open(os.path.join(base, "tree_model.pkl"), "rb"))
    return model

model = load_model()

# Features
C = st.number_input("C (%)", 0.10, 1.00, 0.30)
Mn = st.number_input("Mn (%)", 0.10, 2.00, 0.80)
Si = st.number_input("Si (%)", 0.00, 1.50, 0.25)
Cr = st.number_input("Cr (%)", 0.00, 3.00, 0.50)
Ni = st.number_input("Ni (%)", 0.00, 2.00, 0.40)
Mo = st.number_input("Mo (%)", 0.00, 1.00, 0.10)

AustenitizeTemp = st.number_input("Austenitize Temp (°C)", 700, 1100, 850)
AustenitizeTime = st.number_input("Austenitize Time (min)", 10, 180, 60)

Q = st.selectbox("Quench Medium", ["Water", "Oil", "Polymer"])

TemperingTemp = st.number_input("Tempering Temp (°C)", 100, 700, 300)
TemperingTime = st.number_input("Tempering Time (min)", 10, 240, 90)

# Manual one-hot encoding
q_water = 1 if Q == "Water" else 0
q_oil = 1 if Q == "Oil" else 0
# Polymer = (0,0)

row = np.array([[
    C, Mn, Si, Cr, Ni, Mo,
    AustenitizeTemp, AustenitizeTime,
    q_oil, q_water,
    TemperingTemp, TemperingTime
]])

if st.button("Predict Hardness"):
    pred = model.predict(row)[0]
    st.success(f"Predicted Hardness: {pred:.2f} HRC")
