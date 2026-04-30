import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Speed Predictor", layout="centered")

# ==========================================
# LOAD MODEL
# ==========================================
model = joblib.load('speed_prediction_model.pkl')
feature_names = model.feature_names_in_

# ==========================================
# CUSTOM CSS (PREMIUM UI)
# ==========================================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}

.container {
    max-width: 500px;
    margin: auto;
    padding: 30px;
    border-radius: 16px;
    background: #161b22;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
}

.title {
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    color: white;
    margin-bottom: 20px;
}

.input-label {
    color: #c9d1d9;
    font-size: 14px;
    margin-top: 10px;
}

.result-box {
    background: #0d1117;
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
    text-align: center;
    border: 1px solid #30363d;
}

.result-value {
    font-size: 26px;
    color: #58a6ff;
    font-weight: bold;
}

button[kind="primary"] {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    background-color: #238636;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# PREPROCESS
# ==========================================
def preprocess(machine_no, input_val, output_val, plug_type):
    mac = str(machine_no).upper().replace('DB', '').strip()
    mac = pd.to_numeric(mac, errors='coerce')
    plug = 1 if plug_type == "PLUG" else 0

    return pd.DataFrame([[mac, input_val, output_val, plug]],
                        columns=feature_names)

# ==========================================
# UI
# ==========================================
st.markdown('<div class="container">', unsafe_allow_html=True)

st.markdown('<div class="title">⚙️ Speed Predictor</div>', unsafe_allow_html=True)

machine_no = st.text_input("Machine Number", placeholder="e.g. DB12")
input_val = st.number_input("Input Size", min_value=0.0, format="%.2f")
output_val = st.number_input("Output Size", min_value=0.0, format="%.2f")
plug_type = st.selectbox("Plug Type", ["PLUG", "SINK"])

predict = st.button("Predict")

# ==========================================
# PREDICTION
# ==========================================
if predict:
    df = preprocess(machine_no, input_val, output_val, plug_type)

    if df.isnull().values.any():
        st.error("Invalid Machine Number")
    else:
        pred = model.predict(df)
        mtr = pred[0][0]
        hz = pred[0][1]

        st.markdown(f"""
        <div class="result-box">
            <div>Speed</div>
            <div class="result-value">{mtr:.2f} mtr/min</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">
            <div>Frequency</div>
            <div class="result-value">{hz:.2f} Hz</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)