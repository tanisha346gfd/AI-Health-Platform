"""
Intent Detection and Response Routing System
Fixes the generic response problem by detecting user intent and routing to specialized handlers
"""
from typing import List, Dict, Optional, Tuple
from enum import Enum
import re


class HealthIntent(Enum):
    MENTAL_HEALTH = "mental_health"
    PHYSICAL_SYMPTOMS = "physical_symptoms"
    NUTRITION_DIET = "nutrition_diet"
    FITNESS_EXERCISE = "fitness_exercise"
    SLEEP_FATIGUE = "sleep_fatigue"
    DIABETES_RELATED = "diabetes_related"
    HEART_RELATED = "heart_related"
    PCOS_RELATED = "pcos_related"
    GENERAL_HEALTH = "general_health"
    GREETING = "greeting"
    CRISIS = "crisis"
    UNKNOWN = "unknown"


# Intent keywords for detection
INTENT_KEYWORDS = {
    HealthIntent.CRISIS: [
        "suicide", "kill myself", "end my life", "want to die", "self harm",
        "hurt myself", "no reason to live", "better off dead"
    ],
    HealthIntent.MENTAL_HEALTH: [
        "anxious", "anxiety", "depressed", "depression", "sad", "stressed",
        "stress", "worried", "panic", "lonely", "hopeless", "overwhelmed",
        "mental", "therapy", "therapist", "feeling down", "unmotivated",
        "mood", "emotional", "cry", "crying", "scared", "fear"
    ],
    HealthIntent.SLEEP_FATIGUE: [
        "sleep", "sleepy", "tired", "fatigue", "exhausted", "insomnia",
        "can't sleep", "wake up", "drowsy", "energy", "rest", "nap",
        "sleeping", "oversleep", "restless"
    ],
    HealthIntent.NUTRITION_DIET: [
        "diet", "food", "eat", "eating", "nutrition", "weight loss",
        "lose weight", "gain weight", "calories", "protein", "carbs",
        "healthy food", "meal", "breakfast", "lunch", "dinner", "snack",
        "vegetarian", "vegan", "fasting", "vitamin", "supplement"
    ],
    HealthIntent.FITNESS_EXERCISE: [
        "gym", "exercise", "workout", "fitness", "muscle", "cardio",
        "running", "jogging", "yoga", "strength", "training", "sports",
        "physical activity", "walk", "swimming", "cycling", "abs"
    ],
    HealthIntent.PHYSICAL_SYMPTOMS: [
        "pain", "headache", "stomach", "fever", "cough", "cold", "flu",
        "nausea", "vomit", "diarrhea", "constipation", "rash", "itch",
        "swelling", "dizzy", "dizziness", "chest pain", "breathing",
        "sore throat", "infection", "hurt", "ache", "symptom"
    ],
    HealthIntent.DIABETES_RELATED: [
        "diabetes", "blood sugar", "glucose", "insulin", "diabetic",
        "sugar level", "hba1c", "prediabetes", "type 2", "type 1"
    ],
    HealthIntent.HEART_RELATED: [
        "heart", "cardiac", "blood pressure", "bp", "cholesterol",
        "palpitation", "cardiovascular", "pulse", "heartbeat"
    ],
    HealthIntent.PCOS_RELATED: [
        "pcos", "polycystic", "ovary", "period", "menstrual", "irregular cycle",
        "hormonal", "fertility", "acne", "facial hair", "hirsutism"
    ],
    HealthIntent.GREETING: [
        "hello", "hi", "hey", "good morning", "good evening", "how are you",
        "what can you do", "help me"
    ]
}


# Specialized system prompts for each intent
INTENT_PROMPTS = {
    HealthIntent.CRISIS: """You are a compassionate crisis support companion. This user may be in distress.

CRITICAL INSTRUCTIONS:
1. Express genuine concern and empathy FIRST
2. Let them know they're not alone
3. Ask if they're safe right now
4. Provide crisis helplines:
   - iCall: 9152987821
   - Vandrevala Foundation: 1860-2662-345
   - NIMHANS: 080-46110007
5. Encourage them to reach out to someone they trust
6. Stay calm and supportive

DO NOT: Give generic advice, minimize their feelings, or ignore the severity.""",

    HealthIntent.MENTAL_HEALTH: """You are an empathetic mental health companion (NOT a replacement for professional therapy).

YOUR APPROACH:
1. VALIDATE their feelings first - "It sounds like you're going through a difficult time..."
2. Ask ONE clarifying question to understand better:
   - How long have you been feeling this way?
   - What triggered these feelings?
   - Have you talked to anyone about this?
3. Offer ONE practical coping strategy relevant to their situation
4. Gently suggest professional support if symptoms persist

RESPONSE STYLE:
- Warm, non-judgmental, empathetic
- Use "I hear you", "That sounds challenging", "It's okay to feel..."
- Don't lecture or give multiple suggestions at once
- Focus on THEIR specific situation, not generic advice""",

    HealthIntent.SLEEP_FATIGUE: """You are a sleep and energy wellness advisor.

YOUR APPROACH:
1. Ask about their specific sleep pattern:
   - What time do they sleep/wake?
   - How many hours?
   - Quality of sleep?
   - Any disturbances?
2. Identify potential causes:
   - Screen time before bed?
   - Caffeine intake?
   - Stress/anxiety?
   - Physical activity level?
   - Medical conditions?
3. Give 2-3 SPECIFIC, actionable tips based on their situation
4. Suggest seeing a doctor if chronic

AVOID: Generic "sleep 8 hours" advice. Be specific to their situation.""",

    HealthIntent.NUTRITION_DIET: """You are a practical nutrition coach.

YOUR APPROACH:
1. Understand their goal:
   - Weight loss/gain?
   - Muscle building?
   - General health?
   - Managing a condition?
2. Ask about current eating habits
3. Give SPECIFIC meal/food suggestions
4. Include practical, easy-to-follow advice
5. Consider Indian food options when relevant

PROVIDE:
- Specific food examples, not just categories
- Portion guidance
- Timing recommendations
- Easy substitutions

AVOID: Extreme diets, generic "eat healthy" advice""",

    HealthIntent.FITNESS_EXERCISE: """You are a friendly fitness coach.

YOUR APPROACH:
1. Understand their fitness level (beginner/intermediate/advanced)
2. Know their goal (strength, cardio, flexibility, weight loss)
3. Ask about available equipment/gym access
4. Give SPECIFIC workout recommendations:
   - Exercise names
   - Sets and reps
   - Duration
   - Frequency
5. Include warm-up/cool-down advice
6. Consider any injuries/limitations

PROVIDE:
- Concrete exercise plans
- Progression tips
- Form cues for safety""",

    HealthIntent.PHYSICAL_SYMPTOMS: """You are a symptom guide (NOT a diagnostic tool).

YOUR APPROACH:
1. Ask clarifying questions ONE at a time:
   - Duration of symptoms?
   - Severity (1-10)?
   - Any other symptoms?
   - Recent changes in lifestyle?
2. Provide general information about possible causes
3. Give home care tips if appropriate
4. CLEARLY state when to see a doctor (red flags)

IMPORTANT:
- NEVER diagnose - use "This could be related to..." 
- Always recommend professional consultation for persistent symptoms
- Mention red flags that need immediate attention""",

    HealthIntent.DIABETES_RELATED: """You are a diabetes health educator.

YOUR APPROACH:
1. Understand if they're diagnosed, prediabetic, or concerned
2. Discuss their current management (if applicable)
3. Provide evidence-based information about:
   - Blood sugar management
   - Diet modifications
   - Exercise benefits
   - Monitoring importance
4. Emphasize regular medical check-ups

AVOID: Replacing medical advice or adjusting medications""",

    HealthIntent.HEART_RELATED: """You are a cardiovascular health educator.

YOUR APPROACH:
1. Understand their concern (prevention, management, symptoms)
2. Ask about risk factors:
   - Family history
   - Blood pressure
   - Cholesterol levels
   - Lifestyle factors
3. Provide heart-healthy lifestyle tips
4. Emphasize importance of regular check-ups
5. Mention warning signs that need immediate attention

CRITICAL: Chest pain + breathlessness = advise immediate medical attention""",

    HealthIntent.PCOS_RELATED: """You are a PCOS wellness guide.

YOUR APPROACH:
1. Understand their specific concerns:
   - Symptoms they're experiencing
   - Diagnosis status
   - Current management
2. Discuss holistically:
   - Lifestyle modifications
   - Diet considerations (low GI foods)
   - Exercise recommendations
   - Stress management
3. Address common concerns sensitively (fertility, weight, hair)
4. Recommend gynecologist consultation

BE: Empathetic about the emotional aspects of PCOS""",

    HealthIntent.GREETING: """You are a friendly health companion greeting a user.

Warmly welcome them and briefly mention you can help with:
- Physical health questions
- Mental wellness support
- Diet and nutrition advice
- Fitness guidance
- Health risk assessments

Ask what's on their mind today. Keep it brief and inviting.""",

    HealthIntent.GENERAL_HEALTH: """You are a knowledgeable health companion.

Provide helpful, accurate health information while:
1. Being conversational and friendly
2. Asking follow-up questions to understand better
3. Giving specific, actionable advice
4. Recommending professional consultation when appropriate

Avoid generic responses. Tailor your answer to what they specifically asked.""",

    HealthIntent.UNKNOWN: """You are a helpful health assistant. 

The user's request isn't clear. Politely ask them to clarify:
- What specific health topic they'd like to discuss
- What symptoms or concerns they have
- What goal they're trying to achieve

Be friendly and guide them to share more."""
}


def detect_intent(message: str, conversation_history: List[Dict] = None) -> Tuple[HealthIntent, float]:
    """
    Detect the user's health intent from their message.
    Returns (intent, confidence_score)
    """
    message_lower = message.lower()
    
    # Check for crisis first (highest priority)
    for keyword in INTENT_KEYWORDS[HealthIntent.CRISIS]:
        if keyword in message_lower:
            return HealthIntent.CRISIS, 1.0
    
    # Score each intent based on keyword matches
    intent_scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        if intent == HealthIntent.CRISIS:
            continue
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > 0:
            intent_scores[intent] = score
    
    if not intent_scores:
        # Check conversation history for context
        if conversation_history and len(conversation_history) >= 2:
            # Maintain previous context if no new intent detected
            return HealthIntent.GENERAL_HEALTH, 0.5
        return HealthIntent.UNKNOWN, 0.3
    
    # Get highest scoring intent
    best_intent = max(intent_scores, key=intent_scores.get)
    max_score = intent_scores[best_intent]
    confidence = min(max_score / 3, 1.0)  # Normalize confidence
    
    return best_intent, confidence


def get_system_prompt(intent: HealthIntent) -> str:
    """Get the specialized system prompt for the detected intent."""
    return INTENT_PROMPTS.get(intent, INTENT_PROMPTS[HealthIntent.GENERAL_HEALTH])


def format_conversation_context(history: List[Dict], max_turns: int = 5) -> str:
    """Format recent conversation history for context."""
    if not history:
        return ""
    
    recent = history[-max_turns*2:]  # Last N turns (user + assistant messages)
    context_parts = []
    
    for msg in recent:
        role = msg.get("role", "user")
        content = msg.get("content", "")[:500]  # Truncate long messages
        context_parts.append(f"{role.upper()}: {content}")
    
    return "\n".join(context_parts)


def build_contextual_prompt(
    user_message: str,
    intent: HealthIntent,
    conversation_history: List[Dict] = None
) -> str:
    """Build a full prompt with intent-specific instructions and conversation context."""
    
    base_prompt = get_system_prompt(intent)
    
    context_section = ""
    if conversation_history:
        context = format_conversation_context(conversation_history)
        if context:
            context_section = f"""

CONVERSATION HISTORY (for context):
{context}

Continue the conversation naturally based on this history. Don't repeat yourself."""
    
    return f"""{base_prompt}
{context_section}

RESPONSE GUIDELINES:
- Be specific to their situation, not generic
- Ask follow-up questions to understand better
- Keep response focused and helpful
- Use a warm, conversational tone
- If you asked a question before, acknowledge their answer"""


class ConversationMemory:
    """Manages conversation history for context-aware responses."""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversations: Dict[str, List[Dict]] = {}  # session_id -> messages
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to conversation history."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "role": role,
            "content": content
        })
        
        # Trim to max history
        if len(self.conversations[session_id]) > self.max_history * 2:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history * 2:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session."""
        return self.conversations.get(session_id, [])
    
    def clear_session(self, session_id: str):
        """Clear conversation history for a session."""
        if session_id in self.conversations:
            del self.conversations[session_id]


# Global conversation memory instance
conversation_memory = ConversationMemory()
