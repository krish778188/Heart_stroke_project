import streamlit as st
import pandas as pd
import joblib

model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

st.title("Heart Stroke Prediction")
st.markdown("Enter The Following Details")

age = st.slider("Age", 18, 100, 40)
sex = st. selectbox("SEX", ["M", "F"])
chest_pain = st.selectbox("Chest Pain Type", ["Atypical Angina", "Non-Anginal Pain", "Typical Angina", "Asymptomatic"])
resting_bp = st. number_input("Resting Blood Pressure (mm Hg)",80, 200, 100)
cholesterol = st.number_input ("Cholesterol (mg/dL)", 100, 600, value=None)
if cholesterol < 200:
    st.markdown("🟢 :green[**Normal**]")
elif 200 <= cholesterol < 240:
    st.markdown("🟠 :orange[**Borderline**]")
else:
    st.markdown("🔴 :red[**High Risk**]")
fbs_options = {
    0: "No",
    1: "Yes"
}
fasting_blood_sugar = st.selectbox(
    "Fasting Blood Sugar > 120 mg/dL",
    options=[0, 1],
    format_func=lambda x: fbs_options[x]
)
resting_ecg = st. selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.slider("Max Heart Rate", 60, 220, 150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
oldpeak = st.slider(
    "Oldpeak (ST Depression)",
    min_value=0.0,
    max_value=6.0,
    value=1.0,
    step=0.1,
    help="Look at your Exercise Stress Test report. Find the value labeled 'ST depression' or 'ST segment difference' relative to rest. It is usually a small number like 0.5 or 1.5."
)
st_slope_options = {
    "Up": "Upsloping (Better)",
    "Flat": "Flat (Neutral)",
    "Down": "Downsloping (Riskier)"
}
st_slope = st.selectbox(
    "ST Slope",
    options=["Up", "Flat", "Down"],
    format_func=lambda x: st_slope_options[x],
    help="Check the 'Conclusions' section of your Stress Test report. It will describe the ST segment as 'Upsloping', 'Flat', or 'Downsloping' at peak exercise."
)
st.warning("⚠️ **Disclaimer:** This tool is for educational purposes only and does not constitute medical advice. Please consult a doctor for a proper diagnosis.")
if st.button("Predict"):
    raw_input = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,
        'Sex_' + sex: 1,
        'ChestPainType_' + chest_pain: 1,
        'RestingECG_' + resting_ecg: 1,
        'ExerciseAngina_' + exercise_angina: 1,
        'ST_Slope_' + st_slope: 1
    }
    
    input_df = pd.DataFrame([raw_input])
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[expected_columns]
    
    scaler_input = scaler.transform(input_df)
    prediction = model.predict(scaler_input)[0]
    
    if prediction == 1:
        st.error("High Risk Of Heart Disease")
    else:
        st.success("Low Risk Of Heart Disease")
        
