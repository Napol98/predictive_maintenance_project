# src/preprocess.py
import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_preprocess(path="D:/predictive_maintenance_project/data/raw/ai4i2020.csv"):

    # 1. Load data
    df = pd.read_csv(path)

    # 2. Define target column
    target_col = "Machine failure"  # change if your column name is different

    # 3. Basic cleaning (AI4I usually has no NAs, but safe to drop)
    df = df.dropna()

    # 4. Drop ID-like columns if present
    for col in ["UDI", "Product ID"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    # 5. Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 6. One-hot encode categorical variables (e.g., Type)
    X = pd.get_dummies(X, drop_first=True)

    # 7. Train-test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_and_preprocess()
    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)
