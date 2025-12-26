"""
Groq LLM Provider - Intent-Aware Health Companion
Fixes generic response problem with context-aware, intent-based responses
"""
from groq import Groq
from app.config import settings
from typing import List, Dict, Optional
from app.llm.intent_router import (
    detect_intent, 
    build_contextual_prompt, 
    conversation_memory,
    HealthIntent
)
import hashlib

# Lazy initialization to avoid import-time errors
_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def generate_session_id(user_context: str) -> str:
    """Generate a session ID from user context."""
    return hashlib.md5(user_context.encode()).hexdigest()[:16]


async def chat_with_groq(
    messages: List[Dict], 
    user_context: str = "",
    session_id: Optional[str] = None
) -> str:
    """
    Send messages to Groq LLM with intent detection and conversation memory.
    
    This fixes the generic response problem by:
    1. Detecting user intent from the message
    2. Using specialized prompts for each intent
    3. Maintaining conversation history for context
    4. Providing specific, tailored responses
    """
    try:
        # Get the user's message
        user_message = messages[-1]["content"] if messages else ""
        
        # Generate session ID if not provided
        if not session_id:
            session_id = generate_session_id(user_context or "anonymous")
        
        # Get conversation history
        history = conversation_memory.get_history(session_id)
        
        # Detect intent from the message
        intent, confidence = detect_intent(user_message, history)
        
        # Build context-aware system prompt
        system_prompt = build_contextual_prompt(
            user_message=user_message,
            intent=intent,
            conversation_history=history
        )
        
        # Add user context if available
        if user_context and user_context != "Anonymous user":
            system_prompt += f"\n\nUSER INFO: {user_context}"
        
        # Store user message in memory
        conversation_memory.add_message(session_id, "user", user_message)
        
        # Call the LLM
        client = get_client()
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        
        # Store AI response in memory
        conversation_memory.add_message(session_id, "assistant", ai_response)
        
        return ai_response
        
    except Exception as e:
        # Provide a helpful fallback instead of generic message
        intent, _ = detect_intent(messages[-1]["content"] if messages else "")
        return get_fallback_response(intent, str(e))


def get_fallback_response(intent: HealthIntent, error: str = "") -> str:
    """Get intent-specific fallback response when LLM fails."""
    
    fallbacks = {
        HealthIntent.MENTAL_HEALTH: """I hear that you're going through something difficult. While I'm having a technical issue, please know:

💚 Your feelings are valid
📞 If you need to talk, iCall helpline: 9152987821
🤝 Consider reaching out to someone you trust

I'll be back to chat properly soon. Is there something specific I can help with once I'm working again?""",
        
        HealthIntent.SLEEP_FATIGUE: """I noticed you mentioned sleep/energy concerns. While I work through a technical hiccup, here are some quick tips:

😴 Try the 4-7-8 breathing technique
📱 Reduce screen time 1 hour before bed
🌡️ Keep your room cool (65-68°F)

What specific aspect of your sleep would you like to discuss?""",
        
        HealthIntent.NUTRITION_DIET: """I see you're interested in nutrition! While I reconnect, consider:

🥗 What's your main nutrition goal?
- Weight management?
- Building muscle?
- General health?

Let me know and I'll give you specific recommendations!""",
        
        HealthIntent.FITNESS_EXERCISE: """Fitness question noted! While I get back online:

💪 What's your current fitness level?
🎯 What's your main goal?
🏋️ Do you have gym access?

Share these details and I'll create a specific plan for you!""",
        
        HealthIntent.PHYSICAL_SYMPTOMS: """I noticed you mentioned a symptom. While I'm having a connection issue:

⚠️ If symptoms are severe or concerning, please consult a doctor
📝 Note: When did it start? How severe (1-10)?

I'll provide more guidance once I'm back!""",
        
        HealthIntent.CRISIS: """I'm concerned about you and want to make sure you're okay.

🆘 Please reach out right now:
📞 iCall: 9152987821
📞 Vandrevala Foundation: 1860-2662-345

You're not alone. Please talk to someone who can help. 💚""",
    }
    
    return fallbacks.get(intent, """I'm having a brief technical issue, but I'm here for you!

Could you tell me more about:
- What specific health topic interests you?
- What goal are you trying to achieve?

I'll give you personalized guidance once I reconnect!""")