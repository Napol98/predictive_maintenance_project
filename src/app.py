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

import joblib
import pandas as pd
import streamlit as st
from pathlib import Path
from datetime import datetime
import os

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="🛠️",
    layout="centered"
)

# MODEL_PATH = Path("../models/log_reg_model.joblib")  # or rf_model.joblib
# COLS_PATH = Path("../models/feature_columns.txt")
# HISTORY_PATH = Path("../data/history.csv")  # file to store prediction history

BASE_DIR = Path(__file__).resolve().parent  # this is /src

MODEL_PATH = BASE_DIR.parent / "models" / "log_reg_model.joblib"
COLS_PATH = BASE_DIR.parent / "models" / "feature_columns.txt"
HISTORY_PATH = BASE_DIR.parent / "data" / "history.csv"

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model_and_columns():
    model = joblib.load(MODEL_PATH)
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

    # Create parent directory if needed
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
        "prediction": int(pred),  # 0 or 1
    }

    # If file exists, append; otherwise create
    if HISTORY_PATH.exists():
        df_old = pd.read_csv(HISTORY_PATH)
        df_new = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
    else:
        df_new = pd.DataFrame([row])

    df_new.to_csv(HISTORY_PATH, index=False)


# ---------- SIDEBAR ----------
st.sidebar.title("About this app")
st.sidebar.markdown(
    """
This dashboard predicts whether a machine is likely to **fail**  
based on operating conditions.

**Tips:**
- Adjust the sliders.
- Click **Predict Failure** to log a new entry.
"""
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Model file:**")
st.sidebar.code(MODEL_PATH)

# Show history link
if HISTORY_PATH.exists():
    st.sidebar.markdown("**History file:**")
    st.sidebar.code(str(HISTORY_PATH))


# ---------- MAIN TITLE ----------
st.title("🛠️ Predictive Maintenance - Failure Prediction")

st.markdown(
    """
Use the controls below to simulate machine conditions and estimate  
the probability of **machine failure**.
"""
)

st.markdown("---")

# ---------- INPUT FORM ----------
st.subheader("1️⃣ Enter Machine Parameters")

with st.form("input_form"):
    col1, col2 = st.columns(2)

    with col1:
        air_temp_c = st.number_input(
            "Air temperature [°C]",
            value=27.0,
            help="Ambient temperature around the machine"
        )
        process_temp_c = st.number_input(
            "Process temperature [°C]",
            value=37.0,
            help="Temperature of the process or material"
        )
        rot_speed = st.number_input(
            "Rotational speed [rpm]",
            value=1500.0,
            min_value=0.0,
            help="Speed of the spindle or rotating part"
        )

    with col2:
        torque = st.number_input(
            "Torque [Nm]",
            value=40.0,
            min_value=0.0,
            help="Torque applied during operation"
        )
        tool_wear = st.number_input(
            "Tool wear [min]",
            value=100.0,
            min_value=0.0,
            help="Total time the tool has been in use"
        )
        machine_type = st.selectbox(
            "Machine Type",
            options=["L", "M", "H"],
            help="L = Low quality, M = Medium, H = High"
        )

    submitted = st.form_submit_button("🔍 Predict Failure")

# ---------- PREDICTION ----------
if submitted:
    # Convert °C to K for the model
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

    # One-hot encode and align with training features
    input_encoded = pd.get_dummies(raw_df, drop_first=True)
    input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)

    # Make prediction
    proba = model.predict_proba(input_encoded)[0, 1]
    pred = model.predict(input_encoded)[0]

    # Save to history
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

    st.markdown("---")
    st.subheader("2️⃣ Prediction Result")

    st.metric("Failure probability", f"{proba * 100:.2f}%")

    if proba >= 0.7:
        st.error("High risk of **FAILURE** – immediate attention recommended.")
    elif proba >= 0.4:
        st.warning("Medium risk – monitor the machine closely.")
    else:
        st.success("Low risk – **no failure** predicted under current conditions.")

    # Input summary (human readable)
    st.markdown("### 3️⃣ Input Summary (Human-Readable)")
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
    st.info("Fill in the machine parameters above and click **Predict Failure**.")

# ---------- HISTORY VIEW ----------
st.markdown("---")
st.subheader("📜 Prediction History")

if HISTORY_PATH.exists():
    hist_df = pd.read_csv(HISTORY_PATH)

    with st.expander("Show history table", expanded=False):
        st.dataframe(hist_df, use_container_width=True)
else:
    st.write("No history yet. Make a prediction to start logging.")


st.write("BASE_DIR:", BASE_DIR)
st.write("MODEL_PATH:", MODEL_PATH)
st.write("MODEL_PATH exists?", MODEL_PATH.exists())
st.write("Models folder exists?", (BASE_DIR.parent / "models").exists())
if (BASE_DIR.parent / "models").exists():
    st.write("Files in models folder:", list((BASE_DIR.parent / "models").iterdir()))
else:
    st.write("Files in BASE_DIR.parent:", list(BASE_DIR.parent.iterdir()))
