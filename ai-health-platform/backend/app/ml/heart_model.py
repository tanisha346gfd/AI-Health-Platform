"""
Heart Disease Prediction Model - Inference Module
Uses real trained ML model from UCI Heart Disease dataset
"""
import pickle
import numpy as np
import os
from typing import Dict, Any


class HeartDiseasePredictor:
    """
    Heart Disease Risk Prediction using trained ML model
    
    This predictor:
    1. Loads the trained model from pickle file
    2. Preprocesses input features
    3. Returns risk score with confidence and recommendations
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), '..', 'models', 'heart_model.pkl'
        )
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_info = {}
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and scaler"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Heart disease model not found at {self.model_path}. "
                "Please run train_heart.py first."
            )
        
        with open(self.model_path, 'rb') as f:
            model_package = pickle.load(f)
        
        self.model = model_package['model']
        self.scaler = model_package['scaler']
        self.feature_names = model_package.get('feature_names', [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ])
        self.model_info = {
            'model_name': model_package.get('model_name', 'RandomForest'),
            'version': model_package.get('version', '1.0.0'),
            'metrics': model_package.get('metrics', {})
        }
    
    def _prepare_features(self, input_data: Dict[str, Any]) -> np.ndarray:
        """Prepare feature array from input data"""
        features = []
        for fname in self.feature_names:
            if fname in input_data:
                features.append(input_data[fname])
            else:
                raise ValueError(f"Missing required feature: {fname}")
        
        return np.array([features])
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make heart disease risk prediction
        
        Args:
            input_data: Dictionary with heart disease features
            
        Returns:
            dict with risk_score, risk_level, confidence, and recommendations
        """
        # Prepare features
        features = self._prepare_features(input_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction probability
        risk_probability = self.model.predict_proba(features_scaled)[0][1]
        prediction = self.model.predict(features_scaled)[0]
        
        # Determine risk level
        if risk_probability < 0.3:
            risk_level = "low"
        elif risk_probability < 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        # Generate recommendations based on risk factors
        recommendations = self._generate_recommendations(input_data, risk_level)
        
        # Calculate confidence based on model's cross-validation performance
        model_confidence = self.model_info.get('metrics', {}).get('roc_auc', 0.85)
        
        return {
            'risk_score': float(risk_probability),
            'risk_level': risk_level,
            'prediction': int(prediction),
            'confidence': float(model_confidence),
            'model_version': self.model_info['version'],
            'recommendations': recommendations,
            'disclaimer': "This is a screening tool based on statistical analysis. It is NOT a diagnosis. Please consult a cardiologist for proper evaluation."
        }
    
    def _generate_recommendations(self, input_data: Dict[str, Any], risk_level: str) -> list:
        """Generate personalized recommendations based on input factors"""
        recommendations = []
        
        # Always recommend professional consultation
        recommendations.append("Consult a cardiologist for comprehensive heart health evaluation")
        
        # Blood pressure recommendations
        if input_data.get('trestbps', 0) > 140:
            recommendations.append("Your resting blood pressure is elevated. Monitor regularly and discuss with your doctor")
        
        # Cholesterol recommendations
        if input_data.get('chol', 0) > 240:
            recommendations.append("Consider dietary changes to lower cholesterol levels")
        
        # Exercise recommendations
        if input_data.get('thalach', 150) < 120:
            recommendations.append("Low max heart rate during exercise. Discuss cardiac fitness with your doctor")
        
        # Chest pain recommendations
        if input_data.get('cp', 0) > 0:
            recommendations.append("Chest pain symptoms should be evaluated by a healthcare professional")
        
        # Exercise-induced angina
        if input_data.get('exang', 0) == 1:
            recommendations.append("Exercise-induced angina indicates possible coronary issues - seek evaluation")
        
        # Lifestyle recommendations
        if risk_level in ['medium', 'high']:
            recommendations.append("Maintain a heart-healthy diet low in saturated fats and sodium")
            recommendations.append("Regular moderate exercise (30 min, 5 days/week) as cleared by your doctor")
        
        # Blood sugar
        if input_data.get('fbs', 0) == 1:
            recommendations.append("Elevated fasting blood sugar - consider diabetes screening")
        
        return recommendations[:6]  # Limit to top 6 recommendations


# Singleton instance
_predictor = None

def get_heart_predictor() -> HeartDiseasePredictor:
    """Get or create heart disease predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = HeartDiseasePredictor()
    return _predictor
