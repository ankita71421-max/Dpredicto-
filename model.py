import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ==========================================
# 1. Load Datasets
# ==========================================
train = pd.read_csv("archive (2)/Training.csv")
test = pd.read_csv("archive (2)/Testing.csv")

print(f"Original Training shape: {train.shape}")
print(f"Original Testing shape: {test.shape}")

# ==========================================
# 2. Clean Datasets & Strip Spaces
# ==========================================
train.columns = train.columns.str.strip()
test.columns = test.columns.str.strip()

# Drop artifact columns ('Unnamed: 133' and zero-variance 'fluid_overload')
train = train.drop(columns=["Unnamed: 133", "fluid_overload"], errors="ignore")
test = test.drop(columns=["fluid_overload"], errors="ignore")

print(f"\nCleaned Training shape: {train.shape}")
print(f"Cleaned Testing shape: {test.shape}")

# Check missing values
print(f"\nMissing values in Training: {train.isnull().sum().sum()}")
print(f"Missing values in Testing: {test.isnull().sum().sum()}")

# ==========================================
# 3. Separate Features and Target
# ==========================================
X_train = train.drop(columns=["prognosis"])
y_train = train["prognosis"]

X_test = test.drop(columns=["prognosis"])
y_test = test["prognosis"]

print("\nFeature shapes:")
print(f"X_train: {X_train.shape}")
print(f"y_train: {y_train.shape}")
print(f"X_test: {X_test.shape}")
print(f"y_test: {y_test.shape}")

# ==========================================
# 4. Train All 4 Models (for Comparison)
# ==========================================
nb_model = GaussianNB().fit(X_train, y_train)
dt_model = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
lr_model = LogisticRegression(C=1.0, max_iter=1000, random_state=42).fit(X_train, y_train)

print("\nAll 4 models trained successfully!")

# ==========================================
# 5. Evaluate All 4 Models on Test Set
# ==========================================
models = {
    "Naive Bayes": nb_model,
    "Decision Tree": dt_model,
    "Random Forest": rf_model,
    "Logistic Regression": lr_model
}

results = []
for name, model in models.items():
    preds = model.predict(X_test)
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, preds),
        "Precision": precision_score(y_test, preds, average="weighted", zero_division=0),
        "Recall": recall_score(y_test, preds, average="weighted", zero_division=0),
        "F1 Score": f1_score(y_test, preds, average="weighted", zero_division=0)
    })

results_df = pd.DataFrame(results)
print("\nModel Evaluation on Test Set:")
print(results_df.to_string(index=False))

# ==========================================
# 6. 5-Fold CV Across Unique Patterns (All 4 Models)
# ==========================================
unique_data = train.drop_duplicates()
X_unique = unique_data.drop(columns=["prognosis"])
y_unique = unique_data["prognosis"]

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print("\n5-Fold Cross-Validation on Unique Patterns:")
for name, model in models.items():
    scores = cross_val_score(model, X_unique, y_unique, cv=cv, scoring="accuracy")
    print(f"{name:20s}: Mean = {scores.mean():.4f}, Std = {scores.std():.4f}")

# ==========================================
# 7. Final Core Prediction System (LR + RF Ensemble)
# ==========================================
def predict_disease_ensemble(patient_df):
    """
    Final Model: 80% Logistic Regression + 20% Random Forest.
    Balances smooth linear probability scaling (LR) with non-linear pattern recognition (RF).
    """
    lr_probs = lr_model.predict_proba(patient_df)[0]
    rf_probs = rf_model.predict_proba(patient_df)[0]
    
    # Soft Voting Strategy
    avg_probs = (0.80 * lr_probs) + (0.20 * rf_probs)
    
    classes = lr_model.classes_
    sorted_indices = avg_probs.argsort()[::-1]
    
    top_1 = (classes[sorted_indices[0]].strip(), avg_probs[sorted_indices[0]])
    top_2 = (classes[sorted_indices[1]].strip(), avg_probs[sorted_indices[1]])
    
    return top_1, top_2

# ==========================================
# 8. Manual Case Evaluation using LR + RF Ensemble
# ==========================================
manual_cases = {
    "Case 1 - Fungal infection": [
        "itching",
        "skin_rash",
        "nodal_skin_eruptions",
        "dischromic_patches"
    ],
    "Case 2 - Common Cold": [
        "continuous_sneezing",
        "cough",
        "headache",
        "fatigue",
        "runny_nose"
    ],
    "Case 3 - Migraine": [
        "headache",
        "nausea",
        "vomiting",
        "sensitivity_to_light",
        "blurred_and_distorted_vision"
    ],
    "Case 4 - Malaria": [
        "chills",
        "high_fever",
        "sweating",
        "headache",
        "nausea"
    ]
}

print("\n" + "="*50)
print("     MANUAL CASE EVALUATION (LR + RF ENSEMBLE)")
print("="*50)

for case_name, symptoms in manual_cases.items():
    patient = pd.DataFrame(0, index=[0], columns=X_train.columns)
    
    for symptom in symptoms:
        if symptom in patient.columns:
            patient.loc[0, symptom] = 1
            
    top_1, top_2 = predict_disease_ensemble(patient)
    
    print(f"\n{case_name}")
    print(f"  Inputs         : {symptoms}")
    print(f"  Top Prediction : {top_1[0]} ({top_1[1]*100:.1f}% confidence)")
    print(f"  Alternative    : {top_2[0]} ({top_2[1]*100:.1f}% confidence)")

# ==========================================
# 9. Save LR & RF Models for Deployment
# ==========================================
joblib.dump(lr_model, "lr_model.pkl")
joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(list(X_train.columns), "feature_columns.pkl")

print("\n" + "="*50)
print("Saved 'lr_model.pkl', 'rf_model.pkl', and 'feature_columns.pkl' successfully!")
print("="*50)