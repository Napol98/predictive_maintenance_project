# src/train_model.py

import matplotlib.pyplot as plt
import seaborn as sns

import joblib
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from preprocess import load_and_preprocess


def train_logistic_regression():
    # 1. Load preprocessed data
    X_train, X_test, y_train, y_test = load_and_preprocess()

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    # 2. Define model
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",  # helps with class imbalance
        n_jobs=-1,                # use all cores
    )

    # 3. Train model
    print("Training Logistic Regression...")
    model.fit(X_train, y_train)

    # 4. Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # 5. Evaluation
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, digits=4))

    print("\n=== Confusion Matrix ===")
    print(confusion_matrix(y_test, y_pred))

    auc = roc_auc_score(y_test, y_proba)
    print(f"\nROC-AUC: {auc:.4f}")

    # 6. Save model and feature columns
    models_dir = Path(__file__).resolve().parent.parent / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = models_dir / "log_reg_model.joblib"
    cols_path = models_dir / "feature_columns.txt"

    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path.resolve()}")

    with open(cols_path, "w") as f:
        for col in X_train.columns:
            f.write(col + "\n")
    print(f"Feature columns saved to: {cols_path.resolve()}")


    # 6a. Save confusion matrix plot
    import numpy as np

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Failure", "Failure"],
                yticklabels=["No Failure", "Failure"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix - Logistic Regression")

    plots_dir = models_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plots_dir / "confusion_matrix_log_reg.png", bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    train_logistic_regression()
