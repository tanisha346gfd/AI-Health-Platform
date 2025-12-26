"""
Diabetes Risk Prediction Model (PIMA Dataset)
"""
import joblib
import numpy as np
from typing import Dict, List, Tuple
from app.ml.base_predictor import (
    BaseHealthPredictor, PredictionResult, ContributingFactor
)
from app.config import settings, get_risk_level


class DiabetesPredictor(BaseHealthPredictor):
    """Diabetes risk prediction using trained Random Forest model"""
    
    def __init__(self):
        model_path = f"{settings.MODELS_DIR}/diabetes_model.pkl"
        super().__init__(model_path)
    
    def load_model(self):
        """Load trained diabetes model"""
        try:
            artifacts = joblib.load(self.model_path)
            self.model = artifacts['model']
            self.scaler = artifacts['scaler']
            self.feature_names = artifacts['feature_names']
            self.training_stats = artifacts['training_stats']
            print(f"✅ Diabetes model loaded: {artifacts.get('version', 'unknown')}")
        except Exception as e:
            raise RuntimeError(f"Failed to load diabetes model: {e}")
    
    def validate_input(self, features: Dict) -> Tuple[bool, str]:
        """Validate diabetes-specific features"""
        required_fields = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]
        
        # Check required fields
        for field in required_fields:
            if field not in features:
                return False, f"Missing required field: {field}"
        
        # Validate ranges
        validations = {
            'Pregnancies': (0, 20),
            'Glucose': (40, 400),
            'BloodPressure': (40, 200),
            'SkinThickness': (0, 100),
            'Insulin': (0, 1000),
            'BMI': (10, 60),
            'DiabetesPedigreeFunction': (0, 3),
            'Age': (18, 120)
        }
        
        for field, (min_val, max_val) in validations.items():
            value = features[field]
            if not min_val <= value <= max_val:
                return False, f"{field} out of range ({min_val}-{max_val})"
        
        return True, ""
    
    def prepare_features(self, features: Dict) -> np.ndarray:
        """Prepare features for prediction (including engineered features)"""
        # Base features
        base_values = [
            features['Pregnancies'],
            features['Glucose'],
            features['BloodPressure'],
            features['SkinThickness'],
            features['Insulin'],
            features['BMI'],
            features['DiabetesPedigreeFunction'],
            features['Age']
        ]
        
        # Engineer features (same as training)
        age = features['Age']
        bmi = features['BMI']
        glucose = features['Glucose']
        
        # Age groups
        if age <= 30:
            age_group = 0
        elif age <= 45:
            age_group = 1
        elif age <= 60:
            age_group = 2
        else:
            age_group = 3
        
        # BMI categories
        if bmi < 18.5:
            bmi_cat = 0
        elif bmi < 25:
            bmi_cat = 1
        elif bmi < 30:
            bmi_cat = 2
        else:
            bmi_cat = 3
        
        # Glucose categories
        if glucose < 100:
            glucose_cat = 0
        elif glucose < 125:
            glucose_cat = 1
        else:
            glucose_cat = 2
        
        # Interaction features
        bmi_age = bmi * age
        glucose_bmi = glucose * bmi
        
        # Combine all features
        all_features = base_values + [
            age_group, bmi_cat, glucose_cat, bmi_age, glucose_bmi
        ]
        
        return np.array(all_features).reshape(1, -1)
    
    def predict(self, features: Dict) -> PredictionResult:
        """Generate diabetes risk prediction"""
        # Validate
        is_valid, error_msg = self.validate_input(features)
        if not is_valid:
            raise ValueError(f"Invalid input: {error_msg}")
        
        # Detect OOD
        ood_detected = self.detect_ood(features)
        
        # Prepare features
        X = self.prepare_features(features)
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction_proba = self.model.predict_proba(X_scaled)[0]
        risk_score = float(prediction_proba[1])  # Probability of diabetes
        risk_level = get_risk_level(risk_score)
        
        # Calculate confidence
        confidence = self.calculate_confidence(prediction_proba)
        
        # Generate explanation
        explanation, contributing_factors = self.explain(features, risk_score)
        
        # Should consult doctor?
        should_consult = self.should_consult_doctor(risk_score, confidence, ood_detected)
        
        return PredictionResult(
            disease_type="diabetes",
            risk_score=round(risk_score, 3),
            risk_level=risk_level,
            confidence=confidence,
            explanation=explanation,
            contributing_factors=contributing_factors,
            should_consult=should_consult,
            ood_detected=ood_detected
        )
    
    def explain(self, features: Dict, prediction: float) -> Tuple[str, List[ContributingFactor]]:
        """Generate natural language explanation"""
        risk_level = get_risk_level(prediction)
        
        # Get feature importance from model
        feature_importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        
        # Analyze contributing factors
        contributing_factors = []
        
        # BMI
        bmi = features['BMI']
        if bmi >= 30:
            contributing_factors.append(ContributingFactor(
                name="BMI",
                value=bmi,
                impact="high",
                modifiable=True,
                description=f"BMI of {bmi:.1f} is in the obese range (≥30)"
            ))
        elif bmi >= 25:
            contributing_factors.append(ContributingFactor(
                name="BMI",
                value=bmi,
                impact="medium",
                modifiable=True,
                description=f"BMI of {bmi:.1f} is in the overweight range (25-30)"
            ))
        
        # Glucose
        glucose = features['Glucose']
        if glucose >= 126:
            contributing_factors.append(ContributingFactor(
                name="Glucose",
                value=glucose,
                impact="high",
                modifiable=True,
                description=f"Fasting glucose of {glucose} mg/dL is in diabetic range (≥126)"
            ))
        elif glucose >= 100:
            contributing_factors.append(ContributingFactor(
                name="Glucose",
                value=glucose,
                impact="medium",
                modifiable=True,
                description=f"Fasting glucose of {glucose} mg/dL is in prediabetic range (100-125)"
            ))
        
        # Age
        age = features['Age']
        if age >= 45:
            contributing_factors.append(ContributingFactor(
                name="Age",
                value=age,
                impact="medium",
                modifiable=False,
                description=f"Age {age} increases diabetes risk"
            ))
        
        # Blood Pressure
        bp = features['BloodPressure']
        if bp >= 140:
            contributing_factors.append(ContributingFactor(
                name="Blood Pressure",
                value=bp,
                impact="medium",
                modifiable=True,
                description=f"Blood pressure of {bp} mmHg is elevated (≥140)"
            ))
        
        # Family History (Diabetes Pedigree)
        pedigree = features['DiabetesPedigreeFunction']
        if pedigree > 0.5:
            contributing_factors.append(ContributingFactor(
                name="Family History",
                value=pedigree,
                impact="medium",
                modifiable=False,
                description="Strong family history of diabetes"
            ))
        
        # Generate explanation text
        if risk_level == "low":
            explanation = f"Your diabetes risk is LOW ({prediction*100:.1f}%). "
            explanation += "Your current health metrics are within healthy ranges. "
            explanation += "Continue maintaining a healthy lifestyle with regular exercise and balanced diet."
        
        elif risk_level == "moderate":
            explanation = f"Your diabetes risk is MODERATE ({prediction*100:.1f}%). "
            if contributing_factors:
                top_factors = [f.name for f in contributing_factors[:2]]
                explanation += f"Key factors: {', '.join(top_factors)}. "
            explanation += "Consider lifestyle changes such as weight management, regular exercise (150 min/week), "
            explanation += "and monitoring blood glucose levels. Consult a healthcare provider for personalized advice."
        
        else:  # high
            explanation = f"Your diabetes risk is HIGH ({prediction*100:.1f}%). "
            if contributing_factors:
                top_factors = [f.name for f in contributing_factors[:3]]
                explanation += f"Significant factors: {', '.join(top_factors)}. "
            explanation += "We strongly recommend consulting a healthcare professional for proper screening and personalized guidance. "
            explanation += "Early intervention can prevent or delay diabetes onset."
        
        # Add disclaimer
        explanation += " ⚠️ This is a risk assessment, not a medical diagnosis."
        
        return explanation, contributing_factors
