"""
Habit tracking models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Habit details
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(String, default="daily")  # daily, weekly, custom
    target_conditions = Column(JSON, default=list)  # ['diabetes', 'heart_disease']
    impact_level = Column(String, default="medium")  # low, medium, high
    rationale = Column(Text, nullable=True)  # Why this habit helps
    
    # Stats
    streak_count = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)
    last_completed_at = Column(DateTime, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit")
    
    def __repr__(self):
        return f"<Habit {self.name}>"


class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    
    # Log details
    completed = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    
    # Timestamp
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    habit = relationship("Habit", back_populates="logs")
    
    def __repr__(self):
        return f"<HabitLog {self.habit_id} - {self.logged_at}>"