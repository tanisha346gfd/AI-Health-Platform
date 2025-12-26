"""
PCOS Prediction Model - Inference Module
Uses real trained ML model for PCOS risk prediction
"""
import pickle
import numpy as np
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PCOSInput(BaseModel):
    """Input schema for PCOS prediction based on clinical features"""
    age: int = Field(..., ge=15, le=50, description="Age in years")
    bmi: float = Field(..., ge=15, le=50, description="Body Mass Index")
    weight: float = Field(..., ge=30, le=150, description="Weight in kg")
    cycle_length: int = Field(..., ge=1, le=4, description="Cycle length category: 1=regular, 2=slightly irregular, 3=irregular, 4=very irregular/absent")
    cycle_regularity: int = Field(default=0, ge=0, le=1, description="0=Regular, 1=Irregular")
    weight_gain: int = Field(default=0, ge=0, le=1, description="Recent unexplained weight gain: 0=No, 1=Yes")
    hair_growth: int = Field(default=0, ge=0, le=1, description="Excess facial/body hair: 0=No, 1=Yes")
    skin_darkening: int = Field(default=0, ge=0, le=1, description="Skin darkening (acanthosis): 0=No, 1=Yes")
    pimples: int = Field(default=0, ge=0, le=1, description="Persistent acne: 0=No, 1=Yes")
    fast_food: int = Field(default=0, ge=0, le=1, description="Regular fast food consumption: 0=No, 1=Yes")
    regular_exercise: int = Field(default=1, ge=0, le=1, description="Regular exercise: 0=No, 1=Yes")
    follicle_count_l: Optional[int] = Field(default=None, description="Left ovary follicle count (from ultrasound)")
    follicle_count_r: Optional[int] = Field(default=None, description="Right ovary follicle count (from ultrasound)")
    amh: Optional[float] = Field(default=None, description="Anti-Mullerian Hormone level")
    lh: Optional[float] = Field(default=None, description="Luteinizing Hormone level")
    fsh: Optional[float] = Field(default=None, description="Follicle Stimulating Hormone level")


class PCOSPredictor:
    """
    PCOS Risk Prediction using trained ML model
    
    This predictor:
    1. Loads the trained model from pickle file
    2. Preprocesses input features
    3. Returns risk score with confidence
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), '..', 'models', 'pcos_model.pkl'
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
                f"PCOS model not found at {self.model_path}. "
                "Please run train_pcos.py first."
            )
        
        with open(self.model_path, 'rb') as f:
            model_package = pickle.load(f)
        
        self.model = model_package['model']
        self.scaler = model_package['scaler']
        self.feature_names = model_package['feature_names']
        self.model_info = {
            'model_name': model_package.get('model_name', 'Unknown'),
            'version': model_package.get('version', '1.0.0'),
            'metrics': model_package.get('metrics', {})
        }
    
    def _prepare_features(self, input_data: PCOSInput) -> np.ndarray:
        """Prepare feature array from input data"""
        
        # Map input to feature names expected by model
        feature_mapping = {
            'Age': input_data.age,
            'BMI': input_data.bmi,
            'Weight': input_data.weight,
            'Cycle_length': input_data.cycle_length,
            'Cycle_RI': input_data.cycle_regularity,
            'Weight_gain': input_data.weight_gain,
            'Hair_growth': input_data.hair_growth,
            'Skin_darkening': input_data.skin_darkening,
            'Pimples': input_data.pimples,
            'Fast_food': input_data.fast_food,
            'Regular_Exercise': input_data.regular_exercise,
            'Follicle_L': input_data.follicle_count_l or 6,  # Default average
            'Follicle_R': input_data.follicle_count_r or 6,
            'AMH': input_data.amh or 3.0,  # Default average
            'LH': input_data.lh or 8.0,
            'FSH': input_data.fsh or 6.0,
            'FSH_LH': (input_data.fsh or 6.0) / (input_data.lh or 8.0),
            'Waist_Hip_Ratio': 0.85  # Default average
        }
        
        # Build feature array in correct order
        features = []
        for fname in self.feature_names:
            if fname in feature_mapping:
                features.append(feature_mapping[fname])
            else:
                # Default value for unknown features
                features.append(0)
        
        return np.array([features])
    
    def predict(self, input_data: PCOSInput) -> Dict[str, Any]:
        """
        Make PCOS risk prediction
        
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
        model_confidence = self.model_info.get('metrics', {}).get('roc_auc', 0.8)
        
        return {
            'risk_score': float(risk_probability),
            'risk_level': risk_level,
            'prediction': int(prediction),
            'confidence': float(model_confidence),
            'model_version': self.model_info['version'],
            'recommendations': recommendations,
            'disclaimer': "This is a screening tool based on statistical analysis. It is NOT a diagnosis. Please consult a gynecologist for proper evaluation."
        }
    
    def _generate_recommendations(self, input_data: PCOSInput, risk_level: str) -> list:
        """Generate personalized recommendations based on input factors"""
        recommendations = []
        
        # Always recommend professional consultation for PCOS concerns
        recommendations.append("Consult a gynecologist for comprehensive PCOS evaluation")
        
        # BMI-based recommendations
        if input_data.bmi > 25:
            recommendations.append("Weight management through balanced diet and exercise may help improve symptoms")
        
        # Cycle-based recommendations
        if input_data.cycle_length >= 3:
            recommendations.append("Track your menstrual cycles and discuss irregularities with your doctor")
        
        # Lifestyle recommendations
        if input_data.fast_food == 1:
            recommendations.append("Consider reducing processed foods and adopting a low-glycemic diet")
        
        if input_data.regular_exercise == 0:
            recommendations.append("Regular physical activity (30 min/day) can help manage PCOS symptoms")
        
        # Symptom-specific recommendations
        if input_data.hair_growth == 1 or input_data.pimples == 1:
            recommendations.append("Discuss hormonal treatments with your doctor for skin/hair symptoms")
        
        # Risk-level specific
        if risk_level == "high":
            recommendations.append("Consider getting hormonal tests (LH, FSH, AMH, testosterone)")
            recommendations.append("Ultrasound examination may help confirm diagnosis")
        
        return recommendations[:5]  # Limit to top 5 recommendations


# Singleton instance
_predictor = None

def get_pcos_predictor() -> PCOSPredictor:
    """Get or create PCOS predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = PCOSPredictor()
    return _predictor
