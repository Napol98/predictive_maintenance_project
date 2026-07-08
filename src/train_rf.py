# src/train_rf.py

import joblib
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from preprocess import load_and_preprocess


def train_random_forest():
    X_train, X_test, y_train, y_test = load_and_preprocess()

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        n_jobs=-1,
        class_weight="balanced",
        random_state=42,
    )

    print("Training Random Forest...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n=== Classification Report (Random Forest) ===")
    print(classification_report(y_test, y_pred, digits=4))

    print("\n=== Confusion Matrix (Random Forest) ===")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)

    auc = roc_auc_score(y_test, y_proba)
    print(f"\nROC-AUC: {auc:.4f}")

    models_dir = Path("../models")
    models_dir.mkdir(parents=True, exist_ok=True)

    model_path = models_dir / "rf_model.joblib"
    joblib.dump(model, model_path)
    print(f"\nRandom Forest model saved to: {model_path.resolve()}")

    # Save confusion matrix plot
    plt.figure(figsize=(4, 3))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Greens",
        xticklabels=["No Failure", "Failure"],
        yticklabels=["No Failure", "Failure"],
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix - Random Forest")

    plots_dir = models_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plots_dir / "confusion_matrix_rf.png", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    train_random_forest()
