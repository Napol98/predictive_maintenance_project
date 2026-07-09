# # src/app.py

# import joblib
# import pandas as pd
# import streamlit as st
# from pathlib import Path

# # 1. Load model and feature columns
# MODEL_PATH = Path("../models/log_reg_model.joblib")
# COLS_PATH = Path("../models/feature_columns.txt")

# @st.cache_resource
# def load_model_and_columns():
#     model = joblib.load(MODEL_PATH)
#     with open(COLS_PATH, "r") as f:
#         feature_cols = [line.strip() for line in f.readlines()]
#     return model, feature_cols

# model, feature_cols = load_model_and_columns()

# st.title("Predictive Maintenance - Failure Prediction")

# st.write("Enter the machine parameters to predict the probability of failure.")

# # 2. Define inputs (adjust names to match your actual columns!)
# air_temp = st.number_input("Air temperature [K]", value=300.0)
# process_temp = st.number_input("Process temperature [K]", value=310.0)
# rot_speed = st.number_input("Rotational speed [rpm]", value=1500.0)
# torque = st.number_input("Torque [Nm]", value=40.0)
# tool_wear = st.number_input("Tool wear [min]", value=100.0)

# # Categorical: Type (L, M, H)
# machine_type = st.selectbox("Machine Type", options=["L", "M", "H"])

# # 3. Build a single-row DataFrame for these inputs
# input_dict = {
#     "Air temperature [K]": air_temp,
#     "Process temperature [K]": process_temp,
#     "Rotational speed [rpm]": rot_speed,
#     "Torque [Nm]": torque,
#     "Tool wear [min]": tool_wear,
#     "Type": machine_type,
# }

# raw_df = pd.DataFrame([input_dict])

# # 4. One-hot encode like during training
# #    We'll create dummies and then reindex to the training feature columns
# input_encoded = pd.get_dummies(raw_df, drop_first=True)

# # Ensure all expected columns exist; missing ones are filled with 0
# input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)

# if st.button("Predict Failure"):
#     proba = model.predict_proba(input_encoded)[0, 1]
#     pred = model.predict(input_encoded)[0]

#     st.write(f"**Failure probability:** {proba:.4f}")

#     if proba >= 0.7:
#         st.error("High risk of FAILURE")
#     elif proba >= 0.4:
#         st.warning("Medium risk – monitor closely")
#     else:
#         st.success("Low risk – no failure predicted")



#     st.subheader("Input summary")
#     st.write(raw_df)




# # src/app.py

# import joblib
# import pandas as pd
# import streamlit as st
# from pathlib import Path

# # ---------- CONFIG ----------
# st.set_page_config(
#     page_title="Predictive Maintenance Dashboard",
#     page_icon="🛠️",
#     layout="centered"
# )

# MODEL_PATH = Path("../models/log_reg_model.joblib")  # or rf_model.joblib if you prefer
# COLS_PATH = Path("../models/feature_columns.txt")


# # ---------- LOAD MODEL ----------
# @st.cache_resource
# def load_model_and_columns():
#     model = joblib.load(MODEL_PATH)
#     with open(COLS_PATH, "r") as f:
#         feature_cols = [line.strip() for line in f.readlines()]
#     return model, feature_cols


# model, feature_cols = load_model_and_columns()

# # ---------- SIDEBAR ----------
# st.sidebar.title("About this app")
# st.sidebar.markdown(
#     """
# This dashboard predicts whether a machine is likely to **fail**  
# based on operating conditions.

# **Tips:**
# - Adjust the sliders on the left.
# - Click **Predict Failure** to see the risk.
# """
# )

# st.sidebar.markdown("---")
# st.sidebar.markdown("**Model file:**")
# st.sidebar.code(MODEL_PATH.name)


# # ---------- MAIN TITLE ----------
# st.title("🛠️ Predictive Maintenance - Failure Prediction")

# st.markdown(
#     """
# Use the controls below to simulate machine conditions and estimate  
# the probability of **machine failure**.
# """
# )

# st.markdown("---")

# # ---------- INPUT FORM ----------
# st.subheader("1️⃣ Enter Machine Parameters")

# with st.form("input_form"):
#     col1, col2 = st.columns(2)

#     with col1:
#         # Temperatures in °C for the user
#         air_temp_c = st.number_input(
#             "Air temperature [°C]", 
#             value=27.0, 
#             help="Ambient temperature around the machine"
#         )
#         process_temp_c = st.number_input(
#             "Process temperature [°C]", 
#             value=37.0, 
#             help="Temperature of the process or material"
#         )
#         rot_speed = st.number_input(
#             "Rotational speed [rpm]", 
#             value=1500.0, 
#             min_value=0.0,
#             help="Speed of the spindle or rotating part"
#         )

#     with col2:
#         torque = st.number_input(
#             "Torque [Nm]", 
#             value=40.0, 
#             min_value=0.0,
#             help="Torque applied during operation"
#         )
#         tool_wear = st.number_input(
#             "Tool wear [min]", 
#             value=100.0, 
#             min_value=0.0,
#             help="Total time the tool has been in use"
#         )
#         machine_type = st.selectbox(
#             "Machine Type", 
#             options=["L", "M", "H"],
#             help="L = Low quality, M = Medium, H = High"
#         )

#     submitted = st.form_submit_button("🔍 Predict Failure")

# # ---------- PREDICTION ----------
# if submitted:
#     # Convert °C to K for the model
#     air_temp_k = air_temp_c + 273.15
#     process_temp_k = process_temp_c + 273.15

#     # Raw input as the model expects (K, not °C)
#     input_dict = {
#         "Air temperature [K]": air_temp_k,
#         "Process temperature [K]": process_temp_k,
#         "Rotational speed [rpm]": rot_speed,
#         "Torque [Nm]": torque,
#         "Tool wear [min]": tool_wear,
#         "Type": machine_type,
#     }

#     raw_df = pd.DataFrame([input_dict])

#     # One-hot encode and align with training features
#     input_encoded = pd.get_dummies(raw_df, drop_first=True)
#     input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)

#     # Make prediction
#     proba = model.predict_proba(input_encoded)[0, 1]
#     pred = model.predict(input_encoded)[0]

#     st.markdown("---")
#     st.subheader("2️⃣ Prediction Result")

#     # Display probability nicely
#     st.metric("Failure probability", f"{proba * 100:.2f}%")

#     # Risk level message
#     if proba >= 0.7:
#         st.error("High risk of **FAILURE** – immediate attention recommended.")
#     elif proba >= 0.4:
#         st.warning("Medium risk – monitor the machine closely.")
#     else:
#         st.success("Low risk – **no failure** predicted under current conditions.")

#     # Show user-friendly summary with °C
#     st.markdown("### 3️⃣ Input Summary (Human-Readable)")
#     display_df = pd.DataFrame(
#         [{
#             "Air temperature [°C]": air_temp_c,
#             "Process temperature [°C]": process_temp_c,
#             "Rotational speed [rpm]": rot_speed,
#             "Torque [Nm]": torque,
#             "Tool wear [min]": tool_wear,
#             "Machine Type": machine_type,
#         }]
#     )
#     st.table(display_df)
# else:
#     st.info("Fill in the machine parameters above and click **Predict Failure**.")


# src/app.py

# 



import joblib
import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime
import random
import time

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="🛠️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent  # this is /src

MODEL_PATH = BASE_DIR.parent / "models" / "log_reg_model.joblib"
COLS_PATH = BASE_DIR.parent / "models" / "feature_columns.txt"
HISTORY_PATH = BASE_DIR.parent / "data" / "history.csv"


# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model_and_columns():
    model = joblib.load(MODEL_PATH)

    # Compatibility fix for LogisticRegression models saved with a different scikit-learn version
    if model.__class__.__name__ == "LogisticRegression" and not hasattr(model, "multi_class"):
        model.multi_class = "auto"

    with open(COLS_PATH, "r") as f:
        feature_cols = [line.strip() for line in f.readlines()]

    return model, feature_cols



model, feature_cols = load_model_and_columns()


# ---------- HELPER: SAVE TO HISTORY ----------
def append_to_history(
    air_temp_c,
    process_temp_c,
    rot_speed,
    torque,
    tool_wear,
    machine_type,
    proba,
    pred,
):
    """Append a single prediction row to HISTORY_PATH (CSV)."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "air_temp_c": air_temp_c,
        "process_temp_c": process_temp_c,
        "rot_speed_rpm": rot_speed,
        "torque_nm": torque,
        "tool_wear_min": tool_wear,
        "machine_type": machine_type,
        "failure_probability": proba,
        "prediction": int(pred),
    }

    if HISTORY_PATH.exists():
        df_old = pd.read_csv(HISTORY_PATH)
        df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
    else:
        df_new = pd.DataFrame([row])

    df_new.to_csv(HISTORY_PATH, index=False)


# ---------- HELPER: BUILD ENCODED INPUT ----------
def build_encoded_input(air_temp_c, process_temp_c, rot_speed, torque, tool_wear, machine_type):
    air_temp_k = air_temp_c + 273.15
    process_temp_k = process_temp_c + 273.15

    input_dict = {
        "Air temperature [K]": air_temp_k,
        "Process temperature [K]": process_temp_k,
        "Rotational speed [rpm]": rot_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
        "Type": machine_type,
    }

    raw_df = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(raw_df, drop_first=True)
    input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)
    return input_encoded


# ---------- SIDEBAR: ABOUT + INPUT FORM ----------
st.sidebar.title("🛠️ About this app")
st.sidebar.markdown(
    """
This dashboard predicts whether a machine is likely to **fail**
based on operating conditions.

**Tips:**
- Adjust the values below.
- Click **Predict Failure** to log a new entry.
"""
)
st.sidebar.markdown("---")

st.sidebar.header("⚙️ Machine Parameters")

with st.sidebar.form("input_form"):
    air_temp_c = st.number_input(
        "Air temperature [°C]", value=27.0,
        help="Ambient temperature around the machine"
    )
    process_temp_c = st.number_input(
        "Process temperature [°C]", value=37.0,
        help="Temperature of the process or material"
    )
    rot_speed = st.number_input(
        "Rotational speed [rpm]", value=1500.0, min_value=0.0,
        help="Speed of the spindle or rotating part"
    )
    torque = st.number_input(
        "Torque [Nm]", value=40.0, min_value=0.0,
        help="Torque applied during operation"
    )
    tool_wear = st.number_input(
        "Tool wear [min]", value=100.0, min_value=0.0,
        help="Total time the tool has been in use"
    )
    machine_type = st.selectbox(
        "Machine Type", options=["L", "M", "H"],
        help="L = Low quality, M = Medium, H = High"
    )

    submitted = st.form_submit_button("🔍 Predict Failure", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**Model file:**")
st.sidebar.code(str(MODEL_PATH))

if HISTORY_PATH.exists():
    st.sidebar.markdown("**History file:**")
    st.sidebar.code(str(HISTORY_PATH))


# ---------- MAIN TITLE ----------
st.title("🛠️ Predictive Maintenance – Failure Prediction")
st.markdown(
    "Use the sidebar controls to simulate machine conditions and estimate "
    "the probability of **machine failure**."
)
st.markdown("---")


# ---------- PREDICTION RESULT ----------
if submitted:
    input_encoded = build_encoded_input(
        air_temp_c, process_temp_c, rot_speed, torque, tool_wear, machine_type
    )

    proba = model.predict_proba(input_encoded)[0, 1]
    pred = model.predict(input_encoded)[0]

    append_to_history(
        air_temp_c=air_temp_c,
        process_temp_c=process_temp_c,
        rot_speed=rot_speed,
        torque=torque,
        tool_wear=tool_wear,
        machine_type=machine_type,
        proba=proba,
        pred=pred,
    )

    st.subheader("📊 Prediction Result")

    # ---- Metric cards ----
    prediction_label = "⚠️ Failure Likely" if pred == 1 else "✅ Normal Operation"
    risk_level = "High" if proba >= 0.7 else "Medium" if proba >= 0.4 else "Low"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Failure Probability", f"{proba * 100:.2f}%")
    with col2:
        st.metric("Prediction", prediction_label)
    with col3:
        st.metric("Risk Level", risk_level)

    # ---- Alert banner ----
    if proba >= 0.7:
        st.error("🚨 High risk of **FAILURE** – immediate attention recommended.")
    elif proba >= 0.4:
        st.warning("⚠️ Medium risk – monitor the machine closely.")
    else:
        st.success("✅ Low risk – **no failure** predicted under current conditions.")

    # ---- Input summary ----
    st.markdown("#### Input Summary (Human-Readable)")
    display_df = pd.DataFrame(
        [{
            "Air temperature [°C]": air_temp_c,
            "Process temperature [°C]": process_temp_c,
            "Rotational speed [rpm]": rot_speed,
            "Torque [Nm]": torque,
            "Tool wear [min]": tool_wear,
            "Machine Type": machine_type,
            "Failure probability": f"{proba * 100:.2f}%",
            "Prediction (0=no,1=yes)": int(pred),
        }]
    )
    st.table(display_df)
else:
    st.info("Fill in the machine parameters in the sidebar and click **Predict Failure**.")


# ---------- LIVE SIMULATION (WOW FACTOR) ----------
st.markdown("---")
st.subheader("📡 Live Monitoring Simulation")
st.caption("Simulates random sensor readings every 2 seconds for 20 cycles, as if streaming from a real machine.")

sim_toggle = st.toggle("Start Live Simulation")

if sim_toggle:
    placeholder = st.empty()

    for i in range(20):
        sim_air_temp_c = random.uniform(20, 35)
        sim_process_temp_c = random.uniform(30, 45)
        sim_rpm = random.uniform(1000, 2800)
        sim_torque = random.uniform(10, 70)
        sim_tool_wear = random.uniform(0, 250)
        sim_machine_type = random.choice(["L", "M", "H"])

        sim_encoded = build_encoded_input(
            sim_air_temp_c, sim_process_temp_c, sim_rpm,
            sim_torque, sim_tool_wear, sim_machine_type
        )

        sim_proba = model.predict_proba(sim_encoded)[0, 1]

        with placeholder.container():
            st.write(f"**Cycle {i + 1}/20** — {time.strftime('%H:%M:%S')}")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Air Temp", f"{sim_air_temp_c:.1f} °C")
            c2.metric("Torque", f"{sim_torque:.1f} Nm")
            c3.metric("Tool Wear", f"{sim_tool_wear:.0f} min")
            c4.metric("Failure Risk", f"{sim_proba * 100:.1f}%")

            if sim_proba >= 0.7:
                st.error("🚨 High risk detected in live feed!")
            elif sim_proba >= 0.4:
                st.warning("⚠️ Moderate risk in live feed.")
            else:
                st.success("✅ Normal readings.")

        time.sleep(2)

    st.info("Simulation ended. Toggle off and on to restart.")


# ---------- HISTORY VIEW ----------
st.markdown("---")
st.subheader("📜 Prediction History")

if HISTORY_PATH.exists():
    hist_df = pd.read_csv(HISTORY_PATH)
    with st.expander("Show history table", expanded=False):
        st.dataframe(hist_df, use_container_width=True)
else:
    st.write("No history yet. Make a prediction to start logging.")




# ---------- BATCH PREDICTION ----------
st.markdown("---")
st.markdown("## 📁 Batch Prediction — Upload Machine Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV file with machine sensor readings",
    type=["csv"],
    help="CSV should contain Type, Air temperature [K], Process temperature [K], Rotational speed [rpm], Torque [Nm], Tool wear [min].",
    key="batch_prediction_uploader"
)

if uploaded_file is not None:
    try:
        batch_df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(batch_df)} rows from `{uploaded_file.name}`")

        with st.expander("Preview uploaded data", expanded=False):
            st.dataframe(batch_df.head(10), use_container_width=True)

        required_cols = [
            "Type",
            "Air temperature [K]",
            "Process temperature [K]",
            "Rotational speed [rpm]",
            "Torque [Nm]",
            "Tool wear [min]"
        ]

        missing_cols = [col for col in required_cols if col not in batch_df.columns]

        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
            st.stop()

        encoded_frames = []

        for _, row in batch_df.iterrows():
            # Your build_encoded_input() expects Celsius,
            # but uploaded AI4I CSV uses Kelvin.
            air_temp_c_batch = row["Air temperature [K]"] - 273.15
            process_temp_c_batch = row["Process temperature [K]"] - 273.15

            encoded_row = build_encoded_input(
                air_temp_c_batch,
                process_temp_c_batch,
                row["Rotational speed [rpm]"],
                row["Torque [Nm]"],
                row["Tool wear [min]"],
                row["Type"]
            )

            encoded_frames.append(encoded_row)

        batch_encoded = pd.concat(encoded_frames, ignore_index=True)
        batch_encoded = batch_encoded.reindex(columns=feature_cols, fill_value=0)

        probs = model.predict_proba(batch_encoded)[:, 1]
        preds = model.predict(batch_encoded)

        results_df = batch_df.copy()
        results_df["failure_probability"] = probs
        results_df["failure_probability_percent"] = results_df["failure_probability"].apply(
            lambda x: f"{x * 100:.2f}%"
        )
        results_df["prediction"] = preds

        def risk_label(p):
            if p >= 0.7:
                return "🔴 High Risk"
            elif p >= 0.3:
                return "🟡 Medium Risk"
            else:
                return "🟢 Low Risk"

        results_df["risk_level"] = results_df["failure_probability"].apply(risk_label)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Machines", len(results_df))
        col2.metric("High Risk", int((results_df["failure_probability"] >= 0.7).sum()))
        col3.metric("Avg. Risk Probability", f"{results_df['failure_probability'].mean():.1%}")

        st.markdown("### 🔍 Prediction Results")

        display_df = results_df.sort_values(
            "failure_probability",
            ascending=False
        )

        st.dataframe(
            display_df.style.background_gradient(
                subset=["failure_probability"],
                cmap="RdYlGn_r"
            ),
            use_container_width=True
        )

        csv_bytes = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Results as CSV",
            data=csv_bytes,
            file_name="batch_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Something went wrong processing the file: {e}")
        st.exception(e)
        st.info("Make sure your CSV columns match the expected input format.")


# import joblib
# import pandas as pd
# import streamlit as st
# import streamlit.components.v1 as components
# from pathlib import Path
# from datetime import datetime
# import random
# import time

# # ---------- CONFIG ----------
# st.set_page_config(
#     page_title="Predictive Maintenance Dashboard",
#     page_icon="🛠️",
#     layout="wide"
# )

# BASE_DIR = Path(__file__).resolve().parent

# MODEL_PATH = BASE_DIR.parent / "models" / "log_reg_model.joblib"
# COLS_PATH = BASE_DIR.parent / "models" / "feature_columns.txt"
# HISTORY_PATH = BASE_DIR.parent / "data" / "history.csv"


# # ---------- CUSTOM CSS (Dashboard Theme) ----------
# st.markdown("""
# <style>
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', sans-serif;
#     }
#     .main-title {
#         font-size: 2.2rem;
#         font-weight: 700;
#         color: #1f2937;
#     }
#     .subtitle {
#         color: #6b7280;
#         font-size: 1rem;
#         margin-bottom: 1.5rem;
#     }
#     div[data-testid="stMetric"] {
#         background-color: #ffffff;
#         border: 1px solid #e5e7eb;
#         border-radius: 12px;
#         padding: 15px;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.05);
#     }
#     .live-dot {
#         height: 12px;
#         width: 12px;
#         background-color: #2ecc71;
#         border-radius: 50%;
#         display: inline-block;
#         margin-right: 8px;
#         animation: pulse 1.2s infinite;
#     }
#     @keyframes pulse {
#         0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.6); }
#         70% { box-shadow: 0 0 0 8px rgba(46, 204, 113, 0); }
#         100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
#     }
#     .live-badge {
#         font-weight: 600;
#         color: #16a34a;
#     }
# </style>
# """, unsafe_allow_html=True)


# # ---------- LOAD MODEL ----------
# @st.cache_resource
# def load_model_and_columns():
#     model = joblib.load(MODEL_PATH)
#     with open(COLS_PATH, "r") as f:
#         feature_cols = [line.strip() for line in f.readlines()]
#     return model, feature_cols


# model, feature_cols = load_model_and_columns()


# # ---------- HELPER: SAVE TO HISTORY ----------
# def append_to_history(air_temp_c, process_temp_c, rot_speed, torque,
#                        tool_wear, machine_type, proba, pred):
#     HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
#     row = {
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "air_temp_c": air_temp_c,
#         "process_temp_c": process_temp_c,
#         "rot_speed_rpm": rot_speed,
#         "torque_nm": torque,
#         "tool_wear_min": tool_wear,
#         "machine_type": machine_type,
#         "failure_probability": proba,
#         "prediction": int(pred),
#     }
#     if HISTORY_PATH.exists():
#         df_old = pd.read_csv(HISTORY_PATH)
#         df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
#     else:
#         df_new = pd.DataFrame([row])
#     df_new.to_csv(HISTORY_PATH, index=False)


# # ---------- HELPER: BUILD ENCODED INPUT ----------
# def build_encoded_input(air_temp_c, process_temp_c, rot_speed, torque, tool_wear, machine_type):
#     air_temp_k = air_temp_c + 273.15
#     process_temp_k = process_temp_c + 273.15

#     input_dict = {
#         "Air temperature [K]": air_temp_k,
#         "Process temperature [K]": process_temp_k,
#         "Rotational speed [rpm]": rot_speed,
#         "Torque [Nm]": torque,
#         "Tool wear [min]": tool_wear,
#         "Type": machine_type,
#     }

#     raw_df = pd.DataFrame([input_dict])
#     input_encoded = pd.get_dummies(raw_df, drop_first=True)
#     input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)
#     return input_encoded


# # ---------- HELPER: ANIMATED SVG GAUGE (JS + HTML) ----------
# def render_gauge(value, label="Failure Risk", height=220):
#     """value = 0-100 percentage. Renders an animated circular gauge using SVG + JS."""
#     color = "#e74c3c" if value >= 70 else "#f39c12" if value >= 40 else "#2ecc71"
#     circumference = 440  # approx 2*pi*r for r=70

#     html = f"""
#     <div style="text-align:center; font-family:'Segoe UI', sans-serif;">
#       <svg width="180" height="180" viewBox="0 0 180 180">
#         <circle cx="90" cy="90" r="70" stroke="#e5e7eb" stroke-width="15" fill="none"/>
#         <circle id="arc-{label.replace(' ','')}" cx="90" cy="90" r="70"
#                 stroke="{color}" stroke-width="15" fill="none"
#                 stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}"
#                 stroke-linecap="round" transform="rotate(-90 90 90)"/>
#         <text x="90" y="97" text-anchor="middle" font-size="26" font-weight="bold" fill="{color}">
#           {value:.1f}%
#         </text>
#       </svg>
#       <p style="margin-top:-8px; color:#4b5563; font-weight:600;">{label}</p>
#     </div>
#     <script>
#       (function() {{
#         const arc = document.getElementById("arc-{label.replace(' ','')}");
#         const target = {circumference} - ({circumference} * {value} / 100);
#         let current = {circumference};
#         function step() {{
#           if (current > target) {{
#             current -= 5;
#             if (current < target) current = target;
#             arc.setAttribute("stroke-dashoffset", current);
#             requestAnimationFrame(step);
#           }}
#         }}
#         step();
#       }})();
#     </script>
#     """
#     components.html(html, height=height)


# # ---------- SIDEBAR ----------
# st.sidebar.title("🛠️ About this app")
# st.sidebar.markdown("""
# This dashboard predicts whether a machine is likely to **fail**
# based on operating conditions.

# **Tips:**
# - Adjust the values below.
# - Click **Predict Failure** to log a new entry.
# """)
# st.sidebar.markdown("---")
# st.sidebar.header("⚙️ Machine Parameters")

# with st.sidebar.form("input_form"):
#     air_temp_c = st.number_input("Air temperature [°C]", value=27.0,
#                                   help="Ambient temperature around the machine")
#     process_temp_c = st.number_input("Process temperature [°C]", value=37.0,
#                                       help="Temperature of the process or material")
#     rot_speed = st.number_input("Rotational speed [rpm]", value=1500.0, min_value=0.0,
#                                  help="Speed of the spindle or rotating part")
#     torque = st.number_input("Torque [Nm]", value=40.0, min_value=0.0,
#                               help="Torque applied during operation")
#     tool_wear = st.number_input("Tool wear [min]", value=100.0, min_value=0.0,
#                                  help="Total time the tool has been in use")
#     machine_type = st.selectbox("Machine Type", options=["L", "M", "H"],
#                                  help="L = Low quality, M = Medium, H = High")

#     submitted = st.form_submit_button("🔍 Predict Failure", use_container_width=True)

# st.sidebar.markdown("---")
# st.sidebar.markdown("**Model file:**")
# st.sidebar.code(str(MODEL_PATH))

# if HISTORY_PATH.exists():
#     st.sidebar.markdown("**History file:**")
#     st.sidebar.code(str(HISTORY_PATH))


# # ---------- MAIN TITLE ----------
# st.markdown('<div class="main-title">🛠️ Predictive Maintenance – Failure Prediction</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Use the sidebar controls to simulate machine conditions and estimate the probability of machine failure.</div>', unsafe_allow_html=True)


# # ---------- PREDICTION RESULT ----------
# if submitted:
#     input_encoded = build_encoded_input(
#         air_temp_c, process_temp_c, rot_speed, torque, tool_wear, machine_type
#     )

#     proba = model.predict_proba(input_encoded)[0, 1]
#     pred = model.predict(input_encoded)[0]

#     append_to_history(
#         air_temp_c=air_temp_c, process_temp_c=process_temp_c, rot_speed=rot_speed,
#         torque=torque, tool_wear=tool_wear, machine_type=machine_type,
#         proba=proba, pred=pred,
#     )

#     st.subheader("📊 Prediction Result")

#     prediction_label = "⚠️ Failure Likely" if pred == 1 else "✅ Normal Operation"
#     risk_level = "High" if proba >= 0.7 else "Medium" if proba >= 0.4 else "Low"

#     col_gauge, col_metrics = st.columns([1, 2])

#     with col_gauge:
#         render_gauge(proba * 100, label="Failure Risk")

#     with col_metrics:
#         c1, c2 = st.columns(2)
#         with c1:
#             st.metric("Prediction", prediction_label)
#         with c2:
#             st.metric("Risk Level", risk_level)

#         if proba >= 0.7:
#             st.error("🚨 High risk of **FAILURE** – immediate attention recommended.")
#         elif proba >= 0.4:
#             st.warning("⚠️ Medium risk – monitor the machine closely.")
#         else:
#             st.success("✅ Low risk – **no failure** predicted under current conditions.")

#     st.markdown("#### Input Summary (Human-Readable)")
#     display_df = pd.DataFrame([{
#         "Air temperature [°C]": air_temp_c,
#         "Process temperature [°C]": process_temp_c,
#         "Rotational speed [rpm]": rot_speed,
#         "Torque [Nm]": torque,
#         "Tool wear [min]": tool_wear,
#         "Machine Type": machine_type,
#         "Failure probability": f"{proba * 100:.2f}%",
#         "Prediction (0=no,1=yes)": int(pred),
#     }])
#     st.table(display_df)
# else:
#     st.info("Fill in the machine parameters in the sidebar and click **Predict Failure**.")


# # ---------- LIVE SIMULATION ----------
# st.markdown("---")
# st.subheader("📡 Live Monitoring Simulation")
# st.caption("Simulates random sensor readings every 2 seconds for 20 cycles, as if streaming from a real machine.")

# sim_toggle = st.toggle("Start Live Simulation")

# if sim_toggle:
#     st.markdown(
#         '<span class="live-dot"></span><span class="live-badge">LIVE — streaming simulated sensor data</span>',
#         unsafe_allow_html=True
#     )

#     placeholder = st.empty()

#     for i in range(20):
#         sim_air_temp_c = random.uniform(20, 35)
#         sim_process_temp_c = random.uniform(30, 45)
#         sim_rpm = random.uniform(1000, 2800)
#         sim_torque = random.uniform(10, 70)
#         sim_tool_wear = random.uniform(0, 250)
#         sim_machine_type = random.choice(["L", "M", "H"])

#         sim_encoded = build_encoded_input(
#             sim_air_temp_c, sim_process_temp_c, sim_rpm,
#             sim_torque, sim_tool_wear, sim_machine_type
#         )
#         sim_proba = model.predict_proba(sim_encoded)[0, 1]

#         with placeholder.container():
#             st.write(f"**Cycle {i + 1}/20** — {time.strftime('%H:%M:%S')}")

#             col_g, col_c = st.columns([1, 2])
#             with col_g:
#                 render_gauge(sim_proba * 100, label="Live Risk", height=200)
#             with col_c:
#                 c1, c2, c3 = st.columns(3)
#                 c1.metric("Air Temp", f"{sim_air_temp_c:.1f} °C")
#                 c2.metric("Torque", f"{sim_torque:.1f} Nm")
#                 c3.metric("Tool Wear", f"{sim_tool_wear:.0f} min")

#                 if sim_proba >= 0.7:
#                     st.error("🚨 High risk detected in live feed!")
#                 elif sim_proba >= 0.4:
#                     st.warning("⚠️ Moderate risk in live feed.")
#                 else:
#                     st.success("✅ Normal readings.")

#         time.sleep(2)

#     st.info("Simulation ended. Toggle off and on to restart.")


# # ---------- HISTORY VIEW ----------
# st.markdown("---")
# st.subheader("📜 Prediction History")

# if HISTORY_PATH.exists():
#     hist_df = pd.read_csv(HISTORY_PATH)
#     with st.expander("Show history table", expanded=False):
#         st.dataframe(hist_df, use_container_width=True)
# else:
#     st.write("No history yet. Make a prediction to start logging.")
