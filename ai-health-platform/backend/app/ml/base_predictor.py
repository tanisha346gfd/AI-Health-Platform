"""
Base predictor interface for all disease models
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from pydantic import BaseModel
import numpy as np


class ContributingFactor(BaseModel):
    """Individual factor contributing to risk"""
    name: str
    value: float
    impact: str  # 'high', 'medium', 'low'
    modifiable: bool
    description: str


class PredictionResult(BaseModel):
    """Standardized prediction output"""
    disease_type: str
    risk_score: float  # 0-1 probability
    risk_level: str  # 'low', 'moderate', 'high'
    confidence: float  # Model certainty
    explanation: str  # Natural language explanation
    contributing_factors: List[ContributingFactor]
    should_consult: bool  # Recommend doctor visit
    ood_detected: bool  # Out-of-distribution warning


class BaseHealthPredictor(ABC):
    """
    Abstract base class for all disease prediction models
    
    Ensures consistent interface across all predictors:
    - Load trained model
    - Validate input
    - Make prediction
    - Explain prediction
    - Detect anomalies
    """
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.training_stats = None
        self.load_model()
    
    @abstractmethod
    def load_model(self):
        """Load trained model and artifacts"""
        pass
    
    @abstractmethod
    def validate_input(self, features: Dict) -> Tuple[bool, str]:
        """
        Validate input features
        Returns: (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def prepare_features(self, features: Dict) -> np.ndarray:
        """Convert input dict to model-ready array"""
        pass
    
    @abstractmethod
    def predict(self, features: Dict) -> PredictionResult:
        """
        Main prediction method
        Returns structured prediction result
        """
        pass
    
    @abstractmethod
    def explain(self, features: Dict, prediction: float) -> Tuple[str, List[ContributingFactor]]:
        """
        Generate human-readable explanation
        Returns: (explanation_text, contributing_factors)
        """
        pass
    
    def detect_ood(self, features: Dict) -> bool:
        """
        Out-of-distribution detection
        Flags inputs that are very different from training data
        """
        if not self.training_stats:
            return False
        
        for feature, value in features.items():
            if feature not in self.training_stats:
                continue
            
            mean = self.training_stats[feature]['mean']
            std = self.training_stats[feature]['std']
            
            # Flag if > 3 standard deviations from mean
            z_score = abs((value - mean) / (std + 1e-6))
            if z_score > 3:
                return True
        
        return False
    
    def calculate_confidence(self, prediction_proba: np.ndarray) -> float:
        """
        Calculate model confidence
        Based on prediction probability and model ensemble variance
        """
        # For binary classification
        max_proba = max(prediction_proba)
        
        # Distance from decision boundary (0.5)
        # Closer to 0.5 = lower confidence
        confidence = abs(max_proba - 0.5) * 2
        
        # Ensure minimum confidence
        confidence = max(confidence, 0.5)
        
        return round(confidence, 3)
    
    def should_consult_doctor(self, risk_score: float, confidence: float, ood: bool) -> bool:
        """
        Determine if user should consult healthcare professional
        """
        # High risk + high confidence
        if risk_score > 0.7 and confidence > 0.7:
            return True
        
        # Low confidence regardless of risk
        if confidence < 0.6:
            return True
        
        # Out of distribution
        if ood:
            return True
        
        return False
