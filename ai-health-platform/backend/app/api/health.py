"""
Health profile and prediction API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.health_record import HealthProfile, Prediction
from app.api.auth import get_current_user
from app.ml.diabetes_model import DiabetesPredictor
from app.ml.heart_model import HeartDiseasePredictor
from app.ml.pcos_model import get_pcos_predictor, PCOSInput

router = APIRouter()


# Schemas
class HealthProfileCreate(BaseModel):
    gender: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    glucose: Optional[float] = None
    cholesterol: Optional[float] = None
    family_diabetes: bool = False
    family_heart_disease: bool = False
    smoking: bool = False
    exercise_frequency: Optional[str] = None


class HealthProfileResponse(BaseModel):
    id: int
    user_id: int
    gender: Optional[str]
    age: Optional[int]
    height_cm: Optional[float]
    weight_kg: Optional[float]
    bmi: Optional[float]
    blood_pressure_systolic: Optional[int]
    blood_pressure_diastolic: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DiabetesPredictionRequest(BaseModel):
    pregnancies: int = 0
    glucose: float
    blood_pressure: float
    skin_thickness: float = 0
    insulin: float = 0
    bmi: float
    diabetes_pedigree: float = 0.5
    age: int


class HeartPredictionRequest(BaseModel):
    age: int = Field(..., ge=20, le=100, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex: 0=Female, 1=Male")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type: 0-3")
    trestbps: int = Field(..., ge=80, le=200, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dl)")
    fbs: int = Field(default=0, ge=0, le=1, description="Fasting blood sugar > 120 mg/dl: 0=No, 1=Yes")
    restecg: int = Field(default=0, ge=0, le=2, description="Resting ECG results: 0-2")
    thalach: int = Field(..., ge=60, le=220, description="Maximum heart rate achieved")
    exang: int = Field(default=0, ge=0, le=1, description="Exercise induced angina: 0=No, 1=Yes")
    oldpeak: float = Field(default=0, ge=0, le=6, description="ST depression induced by exercise")
    slope: int = Field(default=1, ge=0, le=2, description="Slope of peak exercise ST segment")
    ca: int = Field(default=0, ge=0, le=4, description="Number of major vessels colored by fluoroscopy")
    thal: int = Field(default=2, ge=0, le=3, description="Thalassemia: 0=Normal, 1=Fixed defect, 2=Reversible defect")


class PCOSPredictionRequest(BaseModel):
    age: int = Field(..., ge=15, le=50, description="Age in years")
    bmi: float = Field(..., ge=15, le=50, description="Body Mass Index")
    weight: float = Field(..., ge=30, le=150, description="Weight in kg")
    cycle_length: int = Field(..., ge=1, le=4, description="Cycle: 1=regular, 2=slightly irregular, 3=irregular, 4=very irregular")
    cycle_regularity: int = Field(default=0, ge=0, le=1, description="0=Regular, 1=Irregular")
    weight_gain: int = Field(default=0, ge=0, le=1, description="Recent weight gain: 0=No, 1=Yes")
    hair_growth: int = Field(default=0, ge=0, le=1, description="Excess facial/body hair: 0=No, 1=Yes")
    skin_darkening: int = Field(default=0, ge=0, le=1, description="Skin darkening: 0=No, 1=Yes")
    pimples: int = Field(default=0, ge=0, le=1, description="Persistent acne: 0=No, 1=Yes")
    fast_food: int = Field(default=0, ge=0, le=1, description="Regular fast food: 0=No, 1=Yes")
    regular_exercise: int = Field(default=1, ge=0, le=1, description="Regular exercise: 0=No, 1=Yes")
    follicle_count_l: Optional[int] = Field(default=None, description="Left ovary follicle count")
    follicle_count_r: Optional[int] = Field(default=None, description="Right ovary follicle count")
    amh: Optional[float] = Field(default=None, description="Anti-Mullerian Hormone level")
    lh: Optional[float] = Field(default=None, description="Luteinizing Hormone level")
    fsh: Optional[float] = Field(default=None, description="Follicle Stimulating Hormone level")


class PredictionResponse(BaseModel):
    id: int
    disease_type: str
    risk_score: float
    risk_level: str
    confidence: float
    explanation: str
    should_consult: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Endpoints
@router.post("/profile", response_model=HealthProfileResponse)
async def create_or_update_profile(
    profile_data: HealthProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update health profile"""
    # Check if profile exists
    profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.id
    ).first()
    
    # Calculate BMI if height and weight provided
    bmi = None
    if profile_data.height_cm and profile_data.weight_kg:
        height_m = profile_data.height_cm / 100
        bmi = profile_data.weight_kg / (height_m ** 2)
    
    if profile:
        # Update existing
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, key, value)
        if bmi:
            profile.bmi = bmi
    else:
        # Create new
        profile = HealthProfile(
            user_id=current_user.id,
            **profile_data.dict(exclude_unset=True),
            bmi=bmi
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    return profile


@router.get("/profile", response_model=HealthProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's health profile"""
    profile = db.query(HealthProfile).filter(
        HealthProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Health profile not found")
    
    return profile


@router.post("/predict/diabetes", response_model=PredictionResponse)
async def predict_diabetes(
    data: DiabetesPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict diabetes risk"""
    try:
        # Prepare features
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
        
        # Get prediction
        predictor = DiabetesPredictor()
        result = predictor.predict(features)
        
        # Convert contributing factors to JSON
        factors_json = [
            {
                'name': f.name,
                'value': f.value,
                'impact': f.impact,
                'modifiable': f.modifiable,
                'description': f.description
            }
            for f in result.contributing_factors
        ]
        
        # Save prediction to database
        prediction = Prediction(
            user_id=current_user.id,
            disease_type=result.disease_type,
            risk_score=result.risk_score,
            risk_level=result.risk_level,
            confidence=result.confidence,
            explanation=result.explanation,
            contributing_factors=factors_json,
            input_features=features,
            ood_detected=result.ood_detected,
            should_consult=result.should_consult
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return prediction
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/predictions", response_model=List[PredictionResponse])
async def get_predictions(
    disease_type: Optional[str] = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's prediction history"""
    query = db.query(Prediction).filter(Prediction.user_id == current_user.id)
    
    if disease_type:
        query = query.filter(Prediction.disease_type == disease_type)
    
    predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
    
    return predictions


@router.get("/trends/{disease_type}")
async def get_risk_trends(
    disease_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk trend over time for a specific disease"""
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.disease_type == disease_type
    ).order_by(Prediction.created_at).all()
    
    if not predictions:
        return {"message": "No predictions found", "data": []}
    
    # Format for charting
    trend_data = [
        {
            'date': p.created_at.strftime('%Y-%m-%d'),
            'risk_score': p.risk_score,
            'risk_level': p.risk_level
        }
        for p in predictions
    ]
    
    # Calculate trend direction
    if len(predictions) >= 2:
        recent = predictions[-1].risk_score
        previous = predictions[-2].risk_score
        change = recent - previous
        
        if change > 0.1:
            trend = "increasing"
        elif change < -0.1:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "disease_type": disease_type,
        "trend": trend,
        "latest_risk": predictions[-1].risk_score,
        "data": trend_data
    }


@router.post("/predict/heart", response_model=PredictionResponse)
async def predict_heart_disease(
    data: HeartPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict heart disease risk using trained ML model"""
    try:
        # Prepare features
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
        
        # Get prediction
        predictor = HeartDiseasePredictor()
        result = predictor.predict(features)
        
        # Save prediction to database
        prediction = Prediction(
            user_id=current_user.id,
            disease_type='heart_disease',
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            explanation=f"Heart disease risk assessment. {'; '.join(result.get('recommendations', [])[:2])}",
            contributing_factors=result.get('recommendations', []),
            input_features=features,
            ood_detected=False,
            should_consult=result['risk_level'] in ['medium', 'high']
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return prediction
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail="Heart disease model not available. Please train model first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/predict/pcos")
async def predict_pcos(
    data: PCOSPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict PCOS risk using trained ML model"""
    try:
        # Convert request to PCOSInput
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
        
        # Get prediction
        predictor = get_pcos_predictor()
        result = predictor.predict(pcos_input)
        
        # Save prediction to database
        prediction = Prediction(
            user_id=current_user.id,
            disease_type='pcos',
            risk_score=result['risk_score'],
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            explanation=result.get('disclaimer', 'PCOS risk assessment based on clinical indicators'),
            contributing_factors=result.get('recommendations', []),
            input_features=data.dict(),
            ood_detected=False,
            should_consult=result['risk_level'] in ['medium', 'high']
        )
        
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        
        return {
            'id': prediction.id,
            'disease_type': 'pcos',
            'risk_score': result['risk_score'],
            'risk_level': result['risk_level'],
            'confidence': result['confidence'],
            'model_version': result.get('model_version', '1.0.0'),
            'recommendations': result.get('recommendations', []),
            'disclaimer': result.get('disclaimer', ''),
            'should_consult': prediction.should_consult,
            'created_at': prediction.created_at
        }
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail="PCOS model not available. Please train model first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
