"""
Public Health Prediction API - No Authentication Required
These endpoints provide ML predictions without user login
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.ml.diabetes_model import DiabetesPredictor
from app.ml.heart_model import HeartDiseasePredictor
from app.ml.pcos_model import get_pcos_predictor, PCOSInput

router = APIRouter()


# Request Schemas
class DiabetesPredictionRequest(BaseModel):
    pregnancies: int = 0
    glucose: float = Field(..., ge=0, le=500, description="Glucose level (mg/dL)")
    blood_pressure: float = Field(..., ge=0, le=200, description="Blood pressure (mm Hg)")
    skin_thickness: float = Field(default=20, ge=0, le=100)
    insulin: float = Field(default=80, ge=0, le=900)
    bmi: float = Field(..., ge=10, le=70, description="Body Mass Index")
    diabetes_pedigree: float = Field(default=0.5, ge=0, le=2.5)
    age: int = Field(..., ge=1, le=120)


class HeartPredictionRequest(BaseModel):
    age: int = Field(..., ge=20, le=100, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex: 0=Female, 1=Male")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type: 0-3")
    trestbps: int = Field(..., ge=80, le=200, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dl)")
    fbs: int = Field(default=0, ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: int = Field(default=0, ge=0, le=2, description="Resting ECG results")
    thalach: int = Field(..., ge=60, le=220, description="Maximum heart rate achieved")
    exang: int = Field(default=0, ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(default=0, ge=0, le=6, description="ST depression")
    slope: int = Field(default=1, ge=0, le=2, description="Slope of peak exercise ST")
    ca: int = Field(default=0, ge=0, le=4, description="Major vessels colored")
    thal: int = Field(default=2, ge=0, le=3, description="Thalassemia")


class PCOSPredictionRequest(BaseModel):
    age: int = Field(..., ge=15, le=50, description="Age in years")
    bmi: float = Field(..., ge=15, le=50, description="Body Mass Index")
    weight: float = Field(..., ge=30, le=150, description="Weight in kg")
    cycle_length: int = Field(..., ge=1, le=4, description="1=regular, 2=slightly irregular, 3=irregular, 4=very irregular")
    cycle_regularity: int = Field(default=0, ge=0, le=1, description="0=Regular, 1=Irregular")
    weight_gain: int = Field(default=0, ge=0, le=1, description="Recent weight gain")
    hair_growth: int = Field(default=0, ge=0, le=1, description="Excess hair growth")
    skin_darkening: int = Field(default=0, ge=0, le=1, description="Skin darkening")
    pimples: int = Field(default=0, ge=0, le=1, description="Persistent acne")
    fast_food: int = Field(default=0, ge=0, le=1, description="Regular fast food")
    regular_exercise: int = Field(default=1, ge=0, le=1, description="Regular exercise")
    follicle_count_l: Optional[int] = Field(default=None)
    follicle_count_r: Optional[int] = Field(default=None)
    amh: Optional[float] = Field(default=None)
    lh: Optional[float] = Field(default=None)
    fsh: Optional[float] = Field(default=None)


# Response Schemas  
class PredictionResult(BaseModel):
    disease_type: str
    risk_score: float
    risk_level: str
    confidence: float
    explanation: str
    recommendations: List[str]
    should_consult: bool
    timestamp: datetime = datetime.now()


@router.post("/diabetes", response_model=PredictionResult)
async def predict_diabetes(data: DiabetesPredictionRequest):
    """
    Predict diabetes risk using ML model trained on PIMA Indians dataset.
    No authentication required.
    """
    try:
        features = {
            'Pregnancies': data.pregnancies,
            'Glucose': data.glucose,
            'BloodPressure': data.blood_pressure,
            'SkinThickness': data.skin_thickness,
            'Insulin': data.insulin,
            'BMI': data.bmi,
            'DiabetesPedigreeFunction': data.diabetes_pedigree,
            'Age': data.age
        }
        
        predictor = DiabetesPredictor()
        result = predictor.predict(features)
        
        # Generate recommendations based on risk factors
        recommendations = []
        if data.glucose > 140:
            recommendations.append("Your glucose level is elevated. Consider monitoring more frequently.")
        if data.bmi > 25:
            recommendations.append("Maintaining a healthy weight can reduce diabetes risk.")
        if data.age > 45:
            recommendations.append("Regular screening is recommended for adults over 45.")
        recommendations.append("Consult a healthcare provider for proper evaluation.")
        
        return PredictionResult(
            disease_type="diabetes",
            risk_score=result.risk_score,
            risk_level=result.risk_level,
            confidence=result.confidence,
            explanation=result.explanation,
            recommendations=recommendations[:5],
            should_consult=result.should_consult
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Diabetes model not available. Please ensure model is trained.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/heart", response_model=PredictionResult)
async def predict_heart_disease(data: HeartPredictionRequest):
    """
    Predict heart disease risk using ML model trained on UCI Heart Disease dataset.
    No authentication required.
    """
    try:
        features = {
            'age': data.age,
            'sex': data.sex,
            'cp': data.cp,
            'trestbps': data.trestbps,
            'chol': data.chol,
            'fbs': data.fbs,
            'restecg': data.restecg,
            'thalach': data.thalach,
            'exang': data.exang,
            'oldpeak': data.oldpeak,
            'slope': data.slope,
            'ca': data.ca,
            'thal': data.thal
        }
        
        predictor = HeartDiseasePredictor()
        result = predictor.predict(features)
        
        return PredictionResult(
            disease_type="heart_disease",
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            explanation=result.get('disclaimer', 'Heart disease risk assessment based on clinical indicators.'),
            recommendations=result.get('recommendations', [])[:5],
            should_consult=result['risk_level'] in ['medium', 'high']
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Heart disease model not available. Please ensure model is trained.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/pcos", response_model=PredictionResult)
async def predict_pcos(data: PCOSPredictionRequest):
    """
    Predict PCOS risk using ML model trained on clinical PCOS dataset.
    No authentication required.
    """
    try:
        pcos_input = PCOSInput(
            age=data.age,
            bmi=data.bmi,
            weight=data.weight,
            cycle_length=data.cycle_length,
            cycle_regularity=data.cycle_regularity,
            weight_gain=data.weight_gain,
            hair_growth=data.hair_growth,
            skin_darkening=data.skin_darkening,
            pimples=data.pimples,
            fast_food=data.fast_food,
            regular_exercise=data.regular_exercise,
            follicle_count_l=data.follicle_count_l,
            follicle_count_r=data.follicle_count_r,
            amh=data.amh,
            lh=data.lh,
            fsh=data.fsh
        )
        
        predictor = get_pcos_predictor()
        result = predictor.predict(pcos_input)
        
        return PredictionResult(
            disease_type="pcos",
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            explanation=result.get('disclaimer', 'PCOS risk assessment based on clinical indicators.'),
            recommendations=result.get('recommendations', [])[:5],
            should_consult=result['risk_level'] in ['medium', 'high']
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="PCOS model not available. Please ensure model is trained.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
