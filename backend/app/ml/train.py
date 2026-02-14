"""
ML Model Training Pipeline for SwasthyaFlow AI
Hybrid ML + Rule-based Triage Classification
"""

import pandas as pd
import numpy as np
import json
import pickle
import os
from typing import Dict, List, Tuple, Any
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
import shap
import warnings
warnings.filterwarnings('ignore')


# Clinical Rule Engine
CRITICAL_RULES = {
    "chest_pain_emergency": {
        "symptoms": ["chest_pain"],
        "action": "HIGH",
        "department": "Emergency",
        "reason": "Potential cardiac emergency - chest pain requires immediate evaluation"
    },
    "stroke_symptoms": {
        "symptoms": ["speech_difficulty", "numbness", "confusion"],
        "min_match": 2,
        "action": "HIGH",
        "department": "Emergency",
        "reason": "Potential stroke - FAST protocol activation"
    },
    "respiratory_distress": {
        "symptoms": ["breathlessness"],
        "vitals": {"spo2": {"lt": 92}},
        "action": "HIGH",
        "department": "Emergency",
        "reason": "Respiratory distress with low oxygen saturation"
    },
    "seizure_emergency": {
        "symptoms": ["seizures"],
        "action": "HIGH",
        "department": "Emergency",
        "reason": "Active seizure requires immediate neurological evaluation"
    },
    "cardiac_warning": {
        "symptoms": ["palpitations", "dizziness", "fainting"],
        "min_match": 2,
        "action": "HIGH",
        "department": "Cardiology",
        "reason": "Multiple cardiac warning signs"
    },
    "gi_bleed": {
        "symptoms": ["blood_in_stool", "abdominal_pain"],
        "action": "HIGH",
        "department": "Emergency",
        "reason": "Potential GI bleeding"
    },
    "elderly_fever": {
        "symptoms": ["fever"],
        "age": {"gt": 65},
        "action": "MEDIUM",
        "department": "General Medicine",
        "reason": "Fever in elderly patient requires careful evaluation"
    },
    "pediatric_respiratory": {
        "symptoms": ["breathlessness", "wheezing"],
        "age": {"lt": 5},
        "action": "HIGH",
        "department": "Pediatrics",
        "reason": "Respiratory symptoms in young child"
    }
}


class TriageModelTrainer:
    """Train and evaluate triage classification model"""

    def __init__(self, model_dir: str = "data/models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)

        self.symptom_encoder = MultiLabelBinarizer()
        self.condition_encoder = MultiLabelBinarizer()
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.model = None
        self.shap_explainer = None

    def prepare_features(self, df: pd.DataFrame, fit: bool = True) -> np.ndarray:
        """Prepare feature matrix from dataframe"""

        # Parse JSON columns
        df['symptoms_list'] = df['symptoms'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
        df['conditions_list'] = df['pre_existing_conditions'].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        )

        # Encode symptoms
        if fit:
            symptom_features = self.symptom_encoder.fit_transform(df['symptoms_list'])
        else:
            symptom_features = self.symptom_encoder.transform(df['symptoms_list'])

        # Encode pre-existing conditions
        if fit:
            condition_features = self.condition_encoder.fit_transform(df['conditions_list'])
        else:
            condition_features = self.condition_encoder.transform(df['conditions_list'])

        # Numeric features
        numeric_cols = ['age', 'bp_systolic', 'bp_diastolic', 'heart_rate',
                       'temperature', 'spo2', 'respiratory_rate']
        numeric_features = df[numeric_cols].values

        if fit:
            numeric_features = self.scaler.fit_transform(numeric_features)
        else:
            numeric_features = self.scaler.transform(numeric_features)

        # Gender encoding
        gender_features = pd.get_dummies(df['gender'], prefix='gender').values

        # Combine all features
        X = np.hstack([symptom_features, condition_features, numeric_features, gender_features])

        return X

    def get_feature_names(self, df: pd.DataFrame) -> List[str]:
        """Get feature names for interpretability"""
        symptom_names = [f"symptom_{s}" for s in self.symptom_encoder.classes_]
        condition_names = [f"condition_{c}" for c in self.condition_encoder.classes_]
        numeric_names = ['age', 'bp_systolic', 'bp_diastolic', 'heart_rate',
                        'temperature', 'spo2', 'respiratory_rate']
        gender_names = ['gender_F', 'gender_M', 'gender_OTHER']

        return symptom_names + condition_names + numeric_names + gender_names

    def train(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Train the triage classification model"""

        print("Preparing features...")
        X = self.prepare_features(df, fit=True)
        y = self.label_encoder.fit_transform(df['risk_level'])

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"Training set: {len(X_train)}, Test set: {len(X_test)}")

        # Train Random Forest
        print("Training Random Forest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"\nModel Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred,
                                   target_names=self.label_encoder.classes_))

        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)
        print(f"\nCross-validation scores: {cv_scores}")
        print(f"Mean CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

        # Create SHAP explainer
        print("\nCreating SHAP explainer...")
        self.shap_explainer = shap.TreeExplainer(self.model)

        # Feature importance
        feature_names = self.get_feature_names(df)
        feature_importance = pd.DataFrame({
            'feature': feature_names[:len(self.model.feature_importances_)],
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 15 Important Features:")
        print(feature_importance.head(15))

        return {
            "accuracy": accuracy,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "feature_importance": feature_importance.to_dict('records')
        }

    def save_models(self):
        """Save trained models and encoders"""

        print(f"Saving models to {self.model_dir}...")

        with open(f"{self.model_dir}/triage_model.pkl", 'wb') as f:
            pickle.dump(self.model, f)

        with open(f"{self.model_dir}/symptom_encoder.pkl", 'wb') as f:
            pickle.dump(self.symptom_encoder, f)

        with open(f"{self.model_dir}/condition_encoder.pkl", 'wb') as f:
            pickle.dump(self.condition_encoder, f)

        with open(f"{self.model_dir}/label_encoder.pkl", 'wb') as f:
            pickle.dump(self.label_encoder, f)

        with open(f"{self.model_dir}/scaler.pkl", 'wb') as f:
            pickle.dump(self.scaler, f)

        with open(f"{self.model_dir}/shap_explainer.pkl", 'wb') as f:
            pickle.dump(self.shap_explainer, f)

        with open(f"{self.model_dir}/rule_engine.json", 'w') as f:
            json.dump(CRITICAL_RULES, f, indent=2)

        print("Models saved successfully!")

    def train_department_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Train department recommendation model"""

        print("\nTraining department recommendation model...")

        X = self.prepare_features(df, fit=False)
        dept_encoder = LabelEncoder()
        y = dept_encoder.fit_transform(df['department'])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        dept_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=12,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        dept_model.fit(X_train, y_train)

        y_pred = dept_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Department Model Accuracy: {accuracy:.4f}")

        # Save department model
        with open(f"{self.model_dir}/department_model.pkl", 'wb') as f:
            pickle.dump(dept_model, f)

        with open(f"{self.model_dir}/department_encoder.pkl", 'wb') as f:
            pickle.dump(dept_encoder, f)

        return {"accuracy": accuracy, "classes": list(dept_encoder.classes_)}


def main():
    """Main training pipeline"""

    # Load synthetic data
    print("Loading synthetic patient data...")
    try:
        df = pd.read_csv("data/synthetic/synthetic_patients.csv")
    except FileNotFoundError:
        print("Generating synthetic data first...")
        from app.ml.synthetic_data import SyntheticDataGenerator
        generator = SyntheticDataGenerator()
        df = generator.generate_dataset(n_records=10000)
        os.makedirs("data/synthetic", exist_ok=True)
        df.to_csv("data/synthetic/synthetic_patients.csv", index=False)

    print(f"Loaded {len(df)} records")

    # Initialize trainer
    trainer = TriageModelTrainer()

    # Train risk classification model
    results = trainer.train(df)

    # Train department model
    dept_results = trainer.train_department_model(df)

    # Save all models
    trainer.save_models()

    print("\n" + "="*50)
    print("Training Complete!")
    print(f"Risk Model Accuracy: {results['accuracy']:.4f}")
    print(f"Department Model Accuracy: {dept_results['accuracy']:.4f}")
    print("="*50)


if __name__ == "__main__":
    main()

