# Predictive Maintenance Dashboard

This project is a Streamlit-based machine learning web application for predictive maintenance.  
The app predicts potential machine failure using input sensor and operational data.

Live app: https://predictivemaintenanceproject-nqioyma9arznrzartebdab.streamlit.app/

---

## Project Overview

Predictive maintenance helps identify possible machine failures before they happen.  
This dashboard allows users to input machine conditions and receive a failure prediction from a trained machine learning model.

The app includes:

- Interactive Streamlit dashboard
- Machine failure prediction
- Trained machine learning model loaded with Joblib
- Prediction history logging
- Data visualization using Matplotlib and Seaborn
- Docker support for reproducible local deployment

---

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Joblib
- Matplotlib
- Seaborn
- Docker

---

## Project Structure

```text
predictive-maintenance/
├── data/
│   └── history.csv
├── models/
│   └── log_reg_model.joblib
├── src/
│   └── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

## How to Run Locally Without Docker

### 1. Clone the repository

```bash
git clone <https://github.com/Napol98/predictive_maintenance_project.git>
cd predictive-maintenance
```

### 2. Create a virtual environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run src/app.py
```

Then open:

```text
http://localhost:8501

https://predictivemaintenanceproject-nqioyma9arznrzartebdab.streamlit.app/
```

---

## How to Run With Docker

Docker allows the app to run in a consistent environment without manually installing Python packages.

### 1. Build the Docker image

```bash
docker build -t predictive-maintenance-app .
```

### 2. Run the Docker container

For macOS/Linux:

```bash
docker run -p 8501:8501 -v "$(pwd)/data:/app/data" --name pred-app predictive-maintenance-app
```

For Windows PowerShell:

```powershell
docker run -p 8501:8501 -v "${PWD}/data:/app/data" --name pred-app predictive-maintenance-app
```

### 3. Open the app

```text
http://localhost:8501
```

---

## Docker Volume Note

The app writes prediction history to:

```text
data/history.csv
```

Docker containers are temporary by default.  
To keep the prediction history after stopping the container, this project uses a volume mount:

```bash
-v "$(pwd)/data:/app/data"
```

This connects the local `data/` folder to the container's `/app/data` folder.

---

## Machine Learning Model

The application uses a trained Logistic Regression model saved as:

```text
models/log_reg_model.joblib
```

The model is loaded by the Streamlit app to generate predictions based on user input.

---

## Future Improvements

Possible future improvements include:

- Add model performance metrics to the dashboard
- Add confusion matrix and classification report
- Improve UI design
- Add Docker Compose support
- Add database storage instead of CSV history
- Deploy Docker version to a cloud server

---

## Author

Created by: Tide

