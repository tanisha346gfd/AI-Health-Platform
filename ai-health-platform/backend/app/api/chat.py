"""
Chat API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.api.auth import get_current_user
from app.llm.groq_provider import chat_with_groq

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    

@router.post("/", response_model=ChatResponse)
async def chat(
    data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI health coach"""
    try:
        # Get recent conversation history
        history = db.query(Conversation).filter(
            Conversation.user_id == current_user.id
        ).order_by(Conversation.created_at.desc()).limit(10).all()
        
        # Format messages
        messages = []
        for conv in reversed(history):
            messages.append({
                "role": conv.role,
                "content": conv.content
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": data.message
        })
        
        # Build user context
        context = f"User: {current_user.full_name}, Age: {current_user.age or 'Unknown'}"
        
        # Get response from LLM
        response = await chat_with_groq(messages, context)
        
        # Save conversation
        user_msg = Conversation(
            user_id=current_user.id,
            role="user",
            content=data.message
        )
        assistant_msg = Conversation(
            user_id=current_user.id,
            role="assistant",
            content=response
        )
        
        db.add(user_msg)
        db.add(assistant_msg)
        db.commit()
        
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat history"""
    history = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at).all()
    
    return [
        {
            "role": h.role,
            "content": h.content,
            "created_at": h.created_at
        }
        for h in history
    ]


@router.post("/public", response_model=ChatResponse)
async def public_chat(data: ChatMessage):
    """Public chat endpoint - no auth required"""
    try:
        messages = [{"role": "user", "content": data.message}]
        response = await chat_with_groq(messages, "Anonymous user")
        return {"response": response}
    except Exception as e:
        # Fallback response if LLM fails
        return {"response": "I'm here to help with your health questions! For personalized advice, please consult a healthcare professional. What would you like to know about health and wellness?"}
