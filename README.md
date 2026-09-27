DPredicto — Disease Prediction System Using Machine Learning

DPredicto is a web-based educational disease prediction system developed as a BCA minor project. It combines machine learning, natural-language symptom processing, and a conversational chatbot to provide a predicted disease based on the symptoms and information provided by the user.

Disclaimer: DPredicto is an educational project and is not intended to provide medical diagnosis, treatment, or professional medical advice. Predictions should not be used as a substitute for consultation with a qualified healthcare professional.

Features
Patient basic information collection
Natural-language symptom input
Symptom extraction from free-text responses
Basic handling of negated symptoms
Conversational chatbot interaction
Adaptive follow-up questions based on reported symptoms
Disease prediction using machine learning
Combination of Logistic Regression and Random Forest models
Disease information including:
Overview
Diagnosis / relevant tests
Treatment information
Warning signs
Possible alternative conditions
SQLite database for storing patient, assessment, prediction, and follow-up information
Flask-based backend API
HTML, CSS and JavaScript-based frontend
Machine Learning

The project evaluates four classification algorithms:

Logistic Regression
Random Forest
Decision Tree
Naive Bayes

The models were evaluated using:

Accuracy
Precision
Recall
F1-Score
5-Fold Cross-Validation
Unique-pattern validation

Based on the project's unique-pattern validation, Logistic Regression and Random Forest were selected for the final prediction system.

The final prediction combines the probability outputs of the two selected models using:

Logistic Regression — 80%
Random Forest — 20%