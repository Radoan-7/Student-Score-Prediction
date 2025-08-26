import streamlit as st
import numpy as np
import joblib
import warnings

warnings.filterwarnings("ignore")


model = joblib.load("best_model.pkl")


st.set_page_config(
    page_title="Student Exam Score Predictor",
    page_icon="📈",
    layout="centered",
)


st.markdown("""
    <style>
        /* Global background with smooth gradient animation */
        body {
            background: linear-gradient(270deg, #1d3557, #457b9d, #1d3557);
            background-size: 600% 600%;
            animation: gradientShift 12s ease infinite;
            font-family: 'Poppins', sans-serif;
            color: #f1f1f1;
        }

        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Main container with glassmorphism */
        .main-container {
            background: rgba(255, 255, 255, 0.08);
            padding: 35px;
            border-radius: 22px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.35);
            transition: transform 0.4s ease;
        }
        .main-container:hover {
            transform: translateY(-6px) scale(1.01);
        }

        /* Hero Title */
        .hero-container {
            text-align: center;
            margin-bottom: 35px;
            animation: slideIn 1.2s ease-out;
        }
        .hero-title {
            font-size: 50px;
            font-weight: 900;
            background: linear-gradient(90deg, #ff7c43, #e63946, #06d6a0, #118ab2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 6s linear infinite;
            letter-spacing: 2px;
            text-shadow: 0 0 15px rgba(255,124,67,0.6), 0 0 28px rgba(6,214,160,0.4);
        }
        .hero-subtitle {
            font-size: 18px;
            color: #f1f1f1cc;
            margin-top: -10px;
            margin-bottom: 25px;
            font-style: italic;
            animation: fadeIn 2s ease-in;
        }

        /* Animations */
        @keyframes shine {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes slideIn {
            0% {opacity: 0; transform: translateY(-40px);}
            100% {opacity: 1; transform: translateY(0);}
        }
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }

        /* Sliders */
        .stSlider > div {
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            border-radius: 12px;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.3);
        }
        .stSlider .st-bo {
            background: linear-gradient(90deg, #06d6a0, #118ab2);
            height: 6px;
            border-radius: 4px;
        }
        .stSlider .st-bq {
            background: #e63946;
        }
        .stSlider .st-bp {
            background: #ff7c43;
            border-radius: 50%;
            box-shadow: 0 0 12px rgba(255,124,67,0.8);
        }

        /* Selectbox */
        .stSelectbox > div {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 8px;
            color: #f1f1f1;
            font-weight: 500;
            box-shadow: inset 0 0 12px rgba(0,0,0,0.3);
        }

        /* Predict button */
        .stButton > button {
            background: linear-gradient(90deg, #e63946, #ff7c43);
            border: none;
            padding: 14px 36px;
            border-radius: 35px;
            color: white;
            font-weight: bold;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.35s ease;
            box-shadow: 0 0 15px rgba(255,124,67,0.6);
            animation: pulse 2.5s infinite;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #ff7c43, #e63946);
            transform: scale(1.08);
            box-shadow: 0 0 25px rgba(255,124,67,0.8);
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 15px rgba(255,124,67,0.4); }
            50% { box-shadow: 0 0 25px rgba(255,124,67,0.9); }
            100% { box-shadow: 0 0 15px rgba(255,124,67,0.4); }
        }

        /* Result display box */
        .result-box {
            margin-top: 30px;
            background: rgba(255, 255, 255, 0.12);
            padding: 28px;
            border-radius: 18px;
            font-size: 24px;
            font-weight: bold;
            color: #fff;
            text-align: center;
            animation: fadeIn 1s ease;
            border: 2px solid rgba(255,124,67,0.4);
            box-shadow: 0 0 18px rgba(6,214,160,0.5);
        }

        /* Progress bar */
        .progress-bar {
            height: 22px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.2);
            overflow: hidden;
            margin-top: 18px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #06d6a0, #118ab2);
            transition: width 1s ease-in-out;
            box-shadow: 0 0 15px rgba(6,214,160,0.6);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="hero-container">
        <div class="hero-title">📈 Student Exam Score Predictor</div>
        <div class="hero-subtitle">"Your effort, lifestyle, and focus — turned into success predictions"</div>
    </div>
""", unsafe_allow_html=True)


with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # Input Fields
    study_hours = st.slider("Study Hours per Day", 0.0, 12.0, 2.0)
    attendance = st.slider("Attendance Percentage", 0.0, 100.0, 80.0)
    mental_health = st.slider("Mental Health Rating (1-10)", 1, 10, 5)
    sleep_hours = st.slider("Sleep Hours per Night", 0.0, 12.0, 7.0)
    part_time_job = st.selectbox("Part-Time Job", ["No", "Yes"])

    ptj_encoded = 1 if part_time_job == "Yes" else 0

    # Prediction
    if st.button("Predict Exam Score"):
        input_data = np.array([[study_hours, attendance, mental_health, sleep_hours, ptj_encoded]])
        prediction = model.predict(input_data)[0]
        prediction = max(0, min(100, prediction))

        # Display result
        st.markdown(f"""
            <div class='result-box'>
                Predicted Exam Score: <br><span style='font-size:34px;'>{prediction:.2f}</span>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {prediction}%"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
