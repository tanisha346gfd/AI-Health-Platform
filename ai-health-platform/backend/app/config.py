"""
Configuration management for AI Health Platform
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App
    APP_NAME: str = "AI Health Companion"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./health_platform.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # LLM
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-70b-versatile"  # Fast and capable
    
    # ML Models
    MODELS_DIR: str = "models"
    
    # Agent
    AGENT_LOOP_INTERVAL_HOURS: int = 1
    AGENT_ENABLED: bool = True
    
    # Safety
    MAX_PREDICTION_AGE_DAYS: int = 30
    CONFIDENCE_THRESHOLD: float = 0.6
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500",  # Live Server default
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()


# Disease-Habit Mapping (Core Feature)
DISEASE_HABIT_MAPPING = {
    "diabetes": {
        "recommended_habits": [
            {
                "name": "30-min Daily Exercise",
                "description": "Walking, jogging, or any cardio activity",
                "frequency": "daily",
                "impact": "high",
                "reason": "Improves insulin sensitivity and glucose metabolism"
            },
            {
                "name": "Blood Glucose Monitoring",
                "description": "Check blood sugar levels",
                "frequency": "daily",
                "impact": "high",
                "reason": "Early detection of fluctuations"
            },
            {
                "name": "Low-Carb Meals",
                "description": "Focus on vegetables, lean protein, healthy fats",
                "frequency": "daily",
                "impact": "high",
                "reason": "Reduces blood sugar spikes"
            },
            {
                "name": "Adequate Sleep (7-8 hours)",
                "description": "Consistent sleep schedule",
                "frequency": "daily",
                "impact": "medium",
                "reason": "Poor sleep affects insulin resistance"
            }
        ],
        "risk_factors": ["BMI", "Glucose", "Age", "Blood Pressure", "Insulin"]
    },
    "heart_disease": {
        "recommended_habits": [
            {
                "name": "Cardio Exercise",
                "description": "Swimming, cycling, brisk walking",
                "frequency": "daily",
                "impact": "high",
                "reason": "Strengthens heart muscle and improves circulation"
            },
            {
                "name": "Mediterranean Diet",
                "description": "Fish, olive oil, nuts, whole grains",
                "frequency": "daily",
                "impact": "high",
                "reason": "Reduces cholesterol and inflammation"
            },
            {
                "name": "Stress Management",
                "description": "Meditation, yoga, deep breathing",
                "frequency": "daily",
                "impact": "medium",
                "reason": "Reduces blood pressure and heart strain"
            },
            {
                "name": "Blood Pressure Monitoring",
                "description": "Regular BP checks",
                "frequency": "weekly",
                "impact": "high",
                "reason": "Early detection of hypertension"
            }
        ],
        "risk_factors": ["Age", "Chest Pain Type", "Blood Pressure", "Cholesterol", "Max Heart Rate"]
    },
    "pcos": {
        "recommended_habits": [
            {
                "name": "Regular Exercise",
                "description": "Mix of cardio and strength training",
                "frequency": "5x per week",
                "impact": "high",
                "reason": "Improves insulin sensitivity and hormone balance"
            },
            {
                "name": "Low-GI Diet",
                "description": "Complex carbs, high fiber",
                "frequency": "daily",
                "impact": "high",
                "reason": "Stabilizes insulin and reduces inflammation"
            },
            {
                "name": "Weight Management",
                "description": "Track weight weekly",
                "frequency": "weekly",
                "impact": "high",
                "reason": "5-10% weight loss can restore ovulation"
            },
            {
                "name": "Stress Reduction",
                "description": "Mindfulness, adequate sleep",
                "frequency": "daily",
                "impact": "medium",
                "reason": "High cortisol worsens PCOS symptoms"
            }
        ],
        "risk_factors": ["BMI", "Menstrual Irregularity", "Insulin Resistance", "Androgens"]
    }
}


# Input Validation Ranges
VALIDATION_RANGES = {
    "age": (0, 120),
    "weight_kg": (20, 300),
    "height_cm": (50, 250),
    "bmi": (10, 60),
    "glucose": (40, 400),
    "blood_pressure_systolic": (70, 250),
    "blood_pressure_diastolic": (40, 150),
    "heart_rate": (30, 220),
    "cholesterol": (100, 600),
    "pregnancies": (0, 20),
    "skin_thickness": (0, 100),
    "insulin": (0, 1000),
}


# Risk Level Thresholds
RISK_THRESHOLDS = {
    "low": 0.3,
    "moderate": 0.6,
    "high": 1.0
}


def get_risk_level(score: float) -> str:
    """Convert risk score to categorical level"""
    if score < RISK_THRESHOLDS["low"]:
        return "low"
    elif score < RISK_THRESHOLDS["moderate"]:
        return "moderate"
    else:
        return "high"
