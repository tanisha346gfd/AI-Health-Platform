"""
Habit tracking API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.habit import Habit, HabitLog
from app.api.auth import get_current_user
from app.config import DISEASE_HABIT_MAPPING

router = APIRouter()


class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str = "daily"
    target_conditions: List[str]
    impact_level: str = "medium"
    rationale: str


class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    frequency: str
    target_conditions: List[str]
    impact_level: str
    streak_count: int
    total_completions: int
    
    class Config:
        from_attributes = True


class HabitLogCreate(BaseModel):
    completed: bool
    notes: Optional[str] = None


@router.post("/", response_model=HabitResponse)
async def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new habit"""
    habit = Habit(
        user_id=current_user.id,
        **habit_data.dict()
    )
    
    db.add(habit)
    db.commit()
    db.refresh(habit)
    
    return habit


@router.get("/", response_model=List[HabitResponse])
async def get_habits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user habits"""
    habits = db.query(Habit).filter(
        Habit.user_id == current_user.id,
        Habit.is_active == True
    ).all()
    
    return habits


@router.post("/{habit_id}/log")
async def log_habit(
    habit_id: int,
    log_data: HabitLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log habit completion"""
    habit = db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == current_user.id
    ).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Create log
    log = HabitLog(
        habit_id=habit.id,
        completed=log_data.completed,
        notes=log_data.notes
    )
    
    db.add(log)
    
    # Update habit stats
    if log_data.completed:
        habit.total_completions += 1
        habit.last_completed_at = datetime.utcnow()
        
        # Update streak
        if habit.last_completed_at:
            days_diff = (datetime.utcnow() - habit.last_completed_at).days
            if days_diff <= 1:
                habit.streak_count += 1
            else:
                habit.streak_count = 1
        else:
            habit.streak_count = 1
    
    db.commit()
    
    return {"message": "Habit logged successfully", "streak": habit.streak_count}


@router.get("/suggestions")
async def get_habit_suggestions(
    disease_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get habit suggestions based on disease risk"""
    if disease_type and disease_type in DISEASE_HABIT_MAPPING:
        return DISEASE_HABIT_MAPPING[disease_type]["recommended_habits"]
    
    # Return all suggestions
    all_suggestions = []
    for disease, data in DISEASE_HABIT_MAPPING.items():
        all_suggestions.extend(data["recommended_habits"])
    
    return all_suggestions
