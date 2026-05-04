# import streamlit as st
# import pandas as pd
# import joblib
# from io import BytesIO

# # ==========================================
# # PAGE CONFIG
# # ==========================================
# st.set_page_config(page_title="Speed Predictor", layout="centered")

# # ==========================================
# # LOAD MODEL
# # ==========================================
# model = joblib.load('speed_prediction_model.pkl')
# feature_names = model.feature_names_in_

# # ==========================================
# # PREPROCESS FUNCTION
# # ==========================================
# def preprocess_row(row):
#     mac = str(row['machine_no']).upper().replace('DB', '').strip()
#     mac = pd.to_numeric(mac, errors='coerce')

#     plug = 1 if str(row['plug_type']).upper() == "PLUG" else 0

#     return [mac, row['input_val'], row['output_val'], plug]

# # ==========================================
# # UI
# # ==========================================
# st.title("📂 Upload Excel for Prediction")

# uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# # ==========================================
# # PROCESS FILE
# # ==========================================
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)

#     # ✅ Rename your messy columns to clean ones
#     df.rename(columns={
#         'MACHINE NO.': 'machine_no',
#         'Input SIZE (MM)': 'input_val',
#         'Output SIZE (MM)': 'output_val',
#         'PLUG/SINK': 'plug_type',
#         'PLUG/\nSINK': 'plug_type',
#         'Input SIZE \n(MM)': 'input_val',
#         'Output SIZE \n(MM)': 'output_val'
#     }, inplace=True)

#     expected_cols = ['machine_no', 'input_val', 'output_val', 'plug_type']

#     if not all(col in df.columns for col in expected_cols):
#         st.error("Column names not matching. Please check Excel format.")
#     else:
#         # Preprocess
#         processed = df.apply(preprocess_row, axis=1, result_type='expand')
#         processed.columns = feature_names

#         if processed.isnull().values.any():
#             st.error("Invalid Machine Number found.")
#         else:
#             preds = model.predict(processed)

#             df['Speed (mtr/min)'] = [p[0] for p in preds]
#             df['Frequency (Hz)'] = [p[1] for p in preds]

#             st.success("✅ Prediction Completed")
#             st.dataframe(df)

#             # ==========================================
#             # DOWNLOAD AS EXCEL
#             # ==========================================
#             def to_excel(dataframe):
#                 output = BytesIO()
#                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                     dataframe.to_excel(writer, index=False)
#                 return output.getvalue()

#             excel_data = to_excel(df)

#             st.download_button(
#                 label="📥 Download Excel File",
#                 data=excel_data,
#                 file_name="predicted_output.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             )



import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="⚙️ Smart Speed Predictor", layout="centered")

# ==========================================
# LOAD MODEL
# ==========================================
model = joblib.load('speed_prediction_model.pkl')
feature_names = model.feature_names_in_

# ==========================================
# CUSTOM UI
# ==========================================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.card {
    background: #161b22;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.4);
}
.title {
    text-align: center;
    color: #58a6ff;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #8b949e;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# PREPROCESS
# ==========================================
def preprocess_row(row):
    mac = str(row['machine_no']).upper().replace('DB', '').strip()
    mac = pd.to_numeric(mac, errors='coerce')

    plug = 1 if str(row['plug_type']).upper() == "PLUG" else 0

    return [mac, row['input_val'], row['output_val'], plug]

# ==========================================
# UI
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">⚙️ Speed Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload Excel → Get Speed & Frequency Predictions</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

# ==========================================
# PROCESS FILE
# ==========================================
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if df.shape[1] < 4:
        st.error("❌ Excel must have at least 4 columns.")
    else:
        # ✅ Force column sequence mapping
        df = df.iloc[:, :4]
        df.columns = ['machine_no', 'input_val', 'output_val', 'plug_type']

        # Preprocess
        processed = df.apply(preprocess_row, axis=1, result_type='expand')
        processed.columns = feature_names

        if processed.isnull().values.any():
            st.error("❌ Invalid Machine Number found in some rows.")
        else:
            with st.spinner("🔄 Predicting..."):
                preds = model.predict(processed)

            df['Speed (mtr/min)'] = [p[0] for p in preds]
            df['Frequency (Hz)'] = [p[1] for p in preds]

            st.success("✅ Prediction Completed Successfully")
            st.dataframe(df, use_container_width=True)

            # ==========================================
            # DOWNLOAD EXCEL
            # ==========================================
            def to_excel(dataframe):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    dataframe.to_excel(writer, index=False)
                return output.getvalue()

            excel_data = to_excel(df)

            st.download_button(
                label="📥 Download Results (Excel)",
                data=excel_data,
                file_name="predicted_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

st.markdown('</div>', unsafe_allow_html=True)