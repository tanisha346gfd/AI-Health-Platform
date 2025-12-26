"""
Health records and predictions models
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class HealthProfile(Base):
    __tablename__ = "health_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Basic measurements
    gender = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    
    # Vital signs
    blood_pressure_systolic = Column(Integer, nullable=True)
    blood_pressure_diastolic = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    
    # Lab values
    glucose = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    hdl = Column(Float, nullable=True)
    ldl = Column(Float, nullable=True)
    triglycerides = Column(Float, nullable=True)
    hba1c = Column(Float, nullable=True)
    
    # Lifestyle factors
    smoking = Column(String, nullable=True)
    alcohol = Column(String, nullable=True)
    exercise_frequency = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_profile")
    
    def __repr__(self):
        return f"<HealthProfile user_id={self.user_id}>"


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prediction details
    disease_type = Column(String, nullable=False)  # 'diabetes', 'heart_disease'
    risk_score = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_level = Column(String, nullable=False)  # 'low', 'medium', 'high'
    
    # Input data (stored for reference)
    input_data = Column(JSON, nullable=False)
    
    # Model info
    model_version = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    
    # Recommendations generated
    recommendations = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction {self.disease_type}: {self.risk_level}>"


class AgentAction(Base):
    __tablename__ = "agent_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Action details
    action_type = Column(String, nullable=False)  # 'reminder', 'suggestion', 'alert'
    message = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)
    
    # Status
    delivered = Column(DateTime, nullable=True)
    acknowledged = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="agent_actions")
    
    def __repr__(self):
        return f"<AgentAction {self.action_type}: {self.message[:30]}...>"