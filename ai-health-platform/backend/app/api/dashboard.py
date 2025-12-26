"""
Dashboard API - Aggregated insights
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.health_record import Prediction, AgentAction
from app.models.habit import Habit, HabitLog
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete dashboard summary"""
    
    # Latest predictions
    latest_predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).limit(3).all()
    
    # Habit stats
    total_habits = db.query(Habit).filter(
        Habit.user_id == current_user.id,
        Habit.is_active == True
    ).count()
    
    # Logs in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_logs = db.query(HabitLog).join(Habit).filter(
        Habit.user_id == current_user.id,
        HabitLog.logged_at >= week_ago,
        HabitLog.completed == True
    ).count()
    
    # Completion rate
    expected_completions = total_habits * 7
    completion_rate = (recent_logs / expected_completions * 100) if expected_completions > 0 else 0
    
    # Recent agent actions
    recent_actions = db.query(AgentAction).filter(
        AgentAction.user_id == current_user.id
    ).order_by(AgentAction.created_at.desc()).limit(5).all()
    
    return {
        "latest_predictions": [
            {
                "disease_type": p.disease_type,
                "risk_level": p.risk_level,
                "risk_score": p.risk_score,
                "created_at": p.created_at
            }
            for p in latest_predictions
        ],
        "habit_stats": {
            "total_active": total_habits,
            "completion_rate": round(completion_rate, 1),
            "completed_this_week": recent_logs
        },
        "recent_agent_actions": [
            {
                "action_type": a.action_type,
                "message": a.message,
                "created_at": a.created_at
            }
            for a in recent_actions
        ]
    }
