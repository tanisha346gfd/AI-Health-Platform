# 🏗️ AI Health Platform - System Architecture

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Backend Architecture](#backend-architecture)
4. [Machine Learning Pipeline](#machine-learning-pipeline)
5. [LLM Integration](#llm-integration)
6. [Database Design](#database-design)
7. [API Design](#api-design)
8. [Frontend Architecture](#frontend-architecture)
9. [Security Architecture](#security-architecture)
10. [Deployment Architecture](#deployment-architecture)

---

## System Overview

The AI Health Platform is a **full-stack health monitoring and prediction system** that combines:
- **Machine Learning** for disease risk prediction (Diabetes, Heart Disease, PCOS)
- **Natural Language Processing** for intelligent health conversations
- **Real-time data processing** for health monitoring
- **Modern web technologies** for user interaction

### Design Principles
1. **Separation of Concerns**: Clear boundaries between API, business logic, and data layers
2. **Scalability**: Stateless API design enables horizontal scaling
3. **Security First**: JWT authentication, input validation, and SQL injection prevention
4. **Ethical AI**: Transparent predictions with explanations and disclaimers
5. **User Privacy**: Minimal data collection, secure storage

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ index.html  │    │dashboard.html│   │onboarding.html│                    │
│  │ (Main App)  │    │ (Dashboard) │   │  (Setup)     │                      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘                      │
│         │                  │                  │                              │
│  ┌──────┴──────────────────┴──────────────────┴──────┐                      │
│  │              JavaScript API Layer                  │                      │
│  │     (api.js, app.js, chat.js, charts.js)         │                      │
│  └─────────────────────────┬─────────────────────────┘                      │
└────────────────────────────┼────────────────────────────────────────────────┘
                             │ REST API (HTTP/JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                     FastAPI Application (main.py)                        ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ││
│  │  │  Auth    │  │  Health  │  │  Chat    │  │  Habits  │  │Dashboard │  ││
│  │  │  Router  │  │  Router  │  │  Router  │  │  Router  │  │  Router  │  ││
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  ││
│  └───────┼─────────────┼─────────────┼─────────────┼─────────────┼────────┘│
└──────────┼─────────────┼─────────────┼─────────────┼─────────────┼──────────┘
           │             │             │             │             │
           ▼             ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SERVICE LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │  Health        │  │  Habit         │  │  Insight       │                 │
│  │  Service       │  │  Service       │  │  Service       │                 │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                 │
└──────────┼───────────────────┼───────────────────┼──────────────────────────┘
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ML LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                      Base Predictor                                       ││
│  │         (Feature validation, scaling, confidence calculation)            ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │   Diabetes     │  │    Heart       │  │     PCOS       │                 │
│  │   Predictor    │  │   Predictor    │  │   Predictor    │                 │
│  │  (RandomForest)│  │ (RandomForest) │  │(GradientBoost) │                 │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                 │
│          │                   │                   │                           │
│  ┌───────┴───────────────────┴───────────────────┴────────┐                 │
│  │              Model Explainer (SHAP/Feature Importance)  │                 │
│  └────────────────────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              LLM LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                    Intent Router                                    │     │
│  │    (Detects 12 health intents: mental_health, diabetes, crisis...)│     │
│  └──────────────────────────────┬─────────────────────────────────────┘     │
│                                 │                                            │
│  ┌──────────────────────────────▼─────────────────────────────────────┐     │
│  │                   Groq LLM Provider                                 │     │
│  │        (Llama 3.1 70B with intent-specific prompts)                │     │
│  └──────────────────────────────┬─────────────────────────────────────┘     │
│                                 │                                            │
│  ┌──────────────────────────────▼─────────────────────────────────────┐     │
│  │                Conversation Memory                                  │     │
│  │        (Context-aware responses across sessions)                   │     │
│  └────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │   SQLAlchemy   │  │    Pickle      │  │    JSON        │                 │
│  │   (SQLite DB)  │  │  (ML Models)   │  │   (Configs)    │                 │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                 │
│          │                   │                   │                           │
│  ┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐                 │
│  │   Users        │  │  diabetes_     │  │  Intent        │                 │
│  │   Predictions  │  │  model.pkl     │  │  Keywords      │                 │
│  │   Habits       │  │  heart_model   │  │  System        │                 │
│  │   Conversations│  │  pcos_model    │  │  Prompts       │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### Directory Structure Explained

```
backend/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app entry point & middleware setup
│   ├── config.py                # Configuration management (env vars, constants)
│   ├── database.py              # Database connection & session management
│   │
│   ├── api/                     # REST API endpoints (Controllers)
│   │   ├── auth.py              # JWT authentication endpoints
│   │   ├── chat.py              # AI chat endpoints
│   │   ├── health.py            # Health predictions endpoints
│   │   ├── habits.py            # Habit tracking endpoints
│   │   ├── dashboard.py         # Dashboard data aggregation
│   │   └── predictions.py       # Prediction history endpoints
│   │
│   ├── llm/                     # Language Model Integration
│   │   ├── groq_provider.py     # Groq API client & chat functions
│   │   ├── intent_router.py     # Intent detection & prompt routing
│   │   └── provider.py          # Abstract LLM provider interface
│   │
│   ├── ml/                      # Machine Learning Inference
│   │   ├── base_predictor.py    # Abstract base class for all predictors
│   │   ├── diabetes_model.py    # Diabetes risk prediction
│   │   ├── heart_model.py       # Heart disease prediction
│   │   ├── pcos_model.py        # PCOS risk prediction
│   │   └── explainer.py         # Model explanation utilities
│   │
│   ├── models/                  # SQLAlchemy ORM Models
│   │   ├── user.py              # User account model
│   │   ├── health_record.py     # Health profile & predictions
│   │   ├── habit.py             # Habit definitions & tracking
│   │   ├── prediction.py        # Prediction history
│   │   └── conversation.py      # Chat history
│   │
│   ├── schemas/                 # Pydantic Validation Schemas
│   │   ├── user.py              # User request/response schemas
│   │   ├── health.py            # Health data schemas
│   │   ├── habit.py             # Habit schemas
│   │   └── prediction.py        # Prediction I/O schemas
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── health_service.py    # Health data processing
│   │   ├── habit_service.py     # Habit management logic
│   │   └── insight_service.py   # Analytics & insights
│   │
│   ├── agent/                   # Autonomous Health Agent (Future)
│   │   ├── core.py              # Agent orchestration
│   │   ├── actions.py           # Available agent actions
│   │   ├── memory.py            # Agent memory/state
│   │   └── reasoner.py          # Decision-making logic
│   │
│   └── utils/                   # Utility Functions
│       ├── safety.py            # Medical safety checks
│       └── validation.py        # Input validation helpers
│
├── ml_training/                 # Model Training Pipeline
│   ├── train_diabetes.py        # Diabetes model training script
│   ├── train_heart.py           # Heart model training script
│   ├── train_pcos.py            # PCOS model training script
│   ├── evaluate.py              # Model evaluation utilities
│   └── datasets/                # Training data
│       ├── diabetes.csv         # PIMA Indians dataset
│       ├── heart.csv            # UCI Heart Disease dataset
│       ├── pcos.csv             # Clinical PCOS dataset
│       └── download_*.py        # Dataset download scripts
│
├── models/                      # Trained ML Models (.pkl files)
└── tests/                       # Unit & integration tests
```

### Request Flow

```
1. HTTP Request arrives at FastAPI
         │
         ▼
2. CORS Middleware checks origin
         │
         ▼
3. Authentication Middleware validates JWT
         │
         ▼
4. Router dispatches to appropriate endpoint
         │
         ▼
5. Pydantic validates request body
         │
         ▼
6. Service layer processes business logic
         │
         ▼
7. ML model or LLM generates predictions/responses
         │
         ▼
8. Database operations (if needed)
         │
         ▼
9. Response serialization & return
```

---

## Machine Learning Pipeline

### Overview

The ML pipeline follows a standardized process for all three disease predictors:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Dataset  │───▶│   EDA &  │───▶│  Feature │───▶│  Class   │  │
│  │ Loading  │    │ Cleaning │    │Engineering│    │Balancing │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                        │         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐        │         │
│  │  Model   │◀───│  Cross-  │◀───│  Train/  │◀───────┘         │
│  │  Export  │    │Validation│    │  Test    │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Model Details

#### 1. Diabetes Model (PIMA Indians Dataset)

| Aspect | Details |
|--------|---------|
| **Dataset** | PIMA Indians Diabetes (768 samples, NIH) |
| **Algorithm** | Random Forest Classifier |
| **Features** | 8 base + 5 engineered = 13 total |
| **Performance** | ROC-AUC: 0.829, Accuracy: 77.3% |
| **Balancing** | SMOTE (Synthetic Minority Oversampling) |

**Feature Engineering:**
```python
# Base Features
['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# Engineered Features
- age_group: Categorized age (0-3)
- bmi_category: Underweight/Normal/Overweight/Obese
- glucose_category: Normal/Prediabetes/Diabetes range
- bmi_age_interaction: BMI × Age
- glucose_bmi_interaction: Glucose × BMI
```

#### 2. Heart Disease Model (UCI Cleveland Dataset)

| Aspect | Details |
|--------|---------|
| **Dataset** | UCI Heart Disease - Cleveland (303 samples) |
| **Algorithm** | Random Forest Classifier |
| **Features** | 13 clinical features |
| **Performance** | ROC-AUC: 0.947, Accuracy: 88.5% |

**Features:**
```python
['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

# Feature Explanations:
- cp: Chest pain type (0-3)
- trestbps: Resting blood pressure
- chol: Serum cholesterol
- fbs: Fasting blood sugar > 120 mg/dl
- restecg: Resting ECG results
- thalach: Maximum heart rate achieved
- exang: Exercise-induced angina
- oldpeak: ST depression
```

#### 3. PCOS Model (Clinical PCOS Dataset)

| Aspect | Details |
|--------|---------|
| **Dataset** | Clinical PCOS (541 samples, Rotterdam criteria) |
| **Algorithm** | Gradient Boosting Classifier |
| **Features** | 18 clinical/lifestyle features |
| **Performance** | ROC-AUC: 0.795, Accuracy: 76.2% |

**Key Features:**
```python
# Symptom Features
['Hair_growth', 'Skin_darkening', 'Pimples', 'Weight_gain']

# Clinical Features  
['Cycle_length', 'Cycle_RI', 'AMH', 'FSH', 'LH', 'FSH_LH']

# Lifestyle Features
['BMI', 'Fast_food', 'Regular_Exercise']
```

### Inference Pipeline

```python
# Prediction Flow
def predict(features: Dict) -> PredictionResult:
    # 1. Validate input ranges
    is_valid, error = validate_input(features)
    
    # 2. Detect out-of-distribution inputs
    ood_detected = detect_ood(features)
    
    # 3. Feature engineering
    X = prepare_features(features)
    
    # 4. Scale features
    X_scaled = scaler.transform(X)
    
    # 5. Get prediction probability
    risk_score = model.predict_proba(X_scaled)[0][1]
    
    # 6. Calculate confidence
    confidence = calculate_confidence(prediction_proba)
    
    # 7. Generate explanation
    explanation = explain(features, risk_score)
    
    # 8. Return structured result
    return PredictionResult(
        risk_score=risk_score,
        risk_level=get_risk_level(risk_score),
        confidence=confidence,
        explanation=explanation,
        should_consult_doctor=should_consult(risk_score, confidence)
    )
```

---

## LLM Integration

### Intent Detection System

The platform uses a sophisticated intent detection system to provide context-aware responses:

```python
class HealthIntent(Enum):
    MENTAL_HEALTH = "mental_health"      # Anxiety, depression, stress
    PHYSICAL_SYMPTOMS = "physical_symptoms"  # Pain, fever, symptoms
    NUTRITION_DIET = "nutrition_diet"    # Food, weight, calories
    FITNESS_EXERCISE = "fitness_exercise" # Gym, workout, sports
    SLEEP_FATIGUE = "sleep_fatigue"      # Sleep issues, tiredness
    DIABETES_RELATED = "diabetes_related" # Blood sugar, insulin
    HEART_RELATED = "heart_related"      # Heart, BP, cholesterol
    PCOS_RELATED = "pcos_related"        # Menstrual, hormonal
    CRISIS = "crisis"                    # Emergency/suicide detection
    GREETING = "greeting"                # Hello, help requests
    GENERAL_HEALTH = "general_health"    # Generic health queries
    UNKNOWN = "unknown"                  # Unclassified
```

### Intent Detection Flow

```
User Message
     │
     ▼
┌─────────────────────┐
│ Keyword Matching    │ ──────────────────────────┐
│ (Pattern-based)     │                           │
└─────────────────────┘                           │
     │                                            │
     ▼                                            ▼
┌─────────────────────┐                  ┌─────────────────────┐
│ Confidence Scoring  │                  │ Crisis Detection    │
│ (Weighted matches)  │                  │ (Priority override) │
└─────────────────────┘                  └─────────────────────┘
     │                                            │
     ▼                                            │
┌─────────────────────┐                           │
│ Context Analysis    │◀──────────────────────────┘
│ (Conversation hist) │
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│ Intent + Confidence │
│ (Returned tuple)    │
└─────────────────────┘
```

### Specialized Prompts

Each intent has a tailored system prompt:

| Intent | Prompt Focus |
|--------|-------------|
| CRISIS | Immediate empathy, safety check, crisis hotlines |
| MENTAL_HEALTH | Validation, coping strategies, professional referral |
| SLEEP_FATIGUE | Sleep pattern analysis, specific tips |
| NUTRITION_DIET | Specific food suggestions, portion guidance |
| FITNESS_EXERCISE | Exercise plans, form tips, progression |
| DIABETES_RELATED | Blood sugar management, medication reminders |
| HEART_RELATED | Heart health, BP monitoring, lifestyle |
| PCOS_RELATED | Hormonal health, cycle tracking, symptoms |

### Conversation Memory

```python
class ConversationMemory:
    """Maintains context across conversation turns"""
    
    def __init__(self, max_history: int = 10):
        self.sessions: Dict[str, List[Dict]] = {}
        self.max_history = max_history
    
    def add_message(self, session_id: str, role: str, content: str):
        # Maintains sliding window of recent messages
        
    def get_history(self, session_id: str) -> List[Dict]:
        # Returns conversation context for LLM
```

---

## Database Design

### Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│       USERS         │       │    HEALTH_PROFILE   │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │───┐   │ id (PK)             │
│ email               │   │   │ user_id (FK)        │───┐
│ hashed_password     │   └──▶│ gender              │   │
│ full_name           │       │ age                 │   │
│ age                 │       │ height_cm           │   │
│ gender              │       │ weight_kg           │   │
│ created_at          │       │ bmi                 │   │
│ is_active           │       │ blood_pressure      │   │
└─────────────────────┘       │ glucose             │   │
                              │ cholesterol         │   │
                              │ family_history      │   │
                              │ created_at          │   │
                              └─────────────────────┘   │
                                                        │
┌─────────────────────┐       ┌─────────────────────┐   │
│    PREDICTIONS      │       │    CONVERSATIONS    │   │
├─────────────────────┤       ├─────────────────────┤   │
│ id (PK)             │       │ id (PK)             │   │
│ user_id (FK)        │◀──────│ user_id (FK)        │◀──┘
│ disease_type        │       │ role                │
│ risk_score          │       │ content             │
│ risk_level          │       │ created_at          │
│ confidence          │       └─────────────────────┘
│ explanation         │
│ recommendations     │       ┌─────────────────────┐
│ created_at          │       │       HABITS        │
└─────────────────────┘       ├─────────────────────┤
                              │ id (PK)             │
                              │ user_id (FK)        │
                              │ name                │
                              │ description         │
                              │ frequency           │
                              │ target_condition    │
                              │ is_active           │
                              │ created_at          │
                              └─────────────────────┘
```

### Models Summary

| Model | Purpose | Key Fields |
|-------|---------|------------|
| User | Account management | email, password_hash, profile |
| HealthProfile | Medical history | vitals, family history, lifestyle |
| Prediction | Risk assessments | disease_type, risk_score, explanation |
| Habit | Health habits | name, frequency, target_condition |
| Conversation | Chat history | role, content, timestamp |

---

## API Design

### RESTful Endpoints

#### Authentication (`/api/v1/auth`)
```
POST /register    - Create new user account
POST /login       - Authenticate and receive JWT
GET  /me          - Get current user profile
```

#### Health Predictions (`/api/v1/health`)
```
POST /predict/diabetes  - Diabetes risk assessment
POST /predict/heart     - Heart disease risk assessment
POST /predict/pcos      - PCOS risk assessment
GET  /predictions       - User's prediction history
```

#### Chat (`/api/v1/chat`)
```
POST /              - Send message to AI (authenticated)
POST /public        - Send message (no auth required)
GET  /history       - Get conversation history
```

#### Habits (`/api/v1/habits`)
```
GET    /            - List user's habits
POST   /            - Create new habit
PUT    /{id}        - Update habit
DELETE /{id}        - Delete habit
POST   /{id}/log    - Log habit completion
```

#### Dashboard (`/api/v1/dashboard`)
```
GET /summary        - Aggregated health summary
GET /trends         - Health trends over time
GET /insights       - AI-generated insights
```

### Response Format

```json
{
  "status": "success",
  "data": {
    "risk_score": 0.45,
    "risk_level": "medium",
    "confidence": 0.85,
    "explanation": "...",
    "recommendations": ["..."],
    "disclaimer": "This is not medical advice..."
  },
  "meta": {
    "model_version": "1.0.0",
    "timestamp": "2025-12-26T10:30:00Z"
  }
}
```

---

## Frontend Architecture

### Page Structure

```
frontend/
├── index.html        # Main app (chat + predictions)
├── dashboard.html    # Health dashboard with charts
├── onboarding.html   # New user setup wizard
├── css/
│   ├── main.css      # Global styles, variables
│   └── dashboard.css # Dashboard-specific styles
└── js/
    ├── api.js        # API client functions
    ├── app.js        # Main application logic
    ├── chat.js       # Chat interface handling
    └── charts.js     # Chart.js visualizations
```

### Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│                    HTML Pages                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Chat Panel  │  │ Prediction  │  │ Dashboard   │     │
│  │             │  │   Forms     │  │   Charts    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                  JavaScript Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  chat.js    │  │   app.js    │  │  charts.js  │     │
│  │ (WebSocket) │  │ (Forms/UI)  │  │ (Chart.js)  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    api.js                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ const API = {                                    │   │
│  │   baseUrl: 'http://localhost:8000/api/v1',      │   │
│  │   chat: (msg) => fetch(...),                    │   │
│  │   predictDiabetes: (data) => fetch(...),        │   │
│  │   getDashboard: () => fetch(...)                │   │
│  │ }                                                │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Authentication Flow

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Client  │         │   API    │         │ Database │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                    │                    │
     │  POST /login       │                    │
     │  {email, password} │                    │
     │───────────────────▶│                    │
     │                    │  Verify password   │
     │                    │───────────────────▶│
     │                    │◀───────────────────│
     │                    │                    │
     │                    │  Generate JWT      │
     │  {access_token}    │  (HS256, 7 days)  │
     │◀───────────────────│                    │
     │                    │                    │
     │  GET /api/health   │                    │
     │  Authorization:    │                    │
     │  Bearer <token>    │                    │
     │───────────────────▶│                    │
     │                    │  Validate JWT      │
     │                    │  Extract user_id   │
     │  {protected data}  │                    │
     │◀───────────────────│                    │
```

### Security Measures

| Layer | Protection |
|-------|-----------|
| **Transport** | HTTPS (in production) |
| **Authentication** | JWT with HS256 signing |
| **Password** | bcrypt hashing (cost factor 12) |
| **Input** | Pydantic validation, type checking |
| **Database** | SQLAlchemy ORM prevents SQL injection |
| **CORS** | Whitelist of allowed origins |
| **API** | Rate limiting (planned) |

---

## Deployment Architecture

### Development Setup

```
┌─────────────────────────────────────────────────────────┐
│                 Local Development                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐      ┌─────────────┐                   │
│  │  Frontend   │      │  Backend    │                   │
│  │  (Port 3000)│─────▶│  (Port 8000)│                   │
│  │  http-server│      │  uvicorn    │                   │
│  └─────────────┘      └──────┬──────┘                   │
│                              │                           │
│                       ┌──────▼──────┐                   │
│                       │   SQLite    │                   │
│                       │   (File DB) │                   │
│                       └─────────────┘                   │
│                                                          │
│  External Services:                                      │
│  ┌─────────────┐                                        │
│  │  Groq API   │ (Cloud LLM)                           │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

### Production Setup (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                               │
│  │   CDN        │◀──── Static Assets (Frontend)                 │
│  │  (CloudFlare)│                                               │
│  └──────┬───────┘                                               │
│         │                                                        │
│  ┌──────▼───────┐      ┌─────────────┐      ┌─────────────┐    │
│  │ Load Balancer│─────▶│  API Server │─────▶│  PostgreSQL │    │
│  │   (nginx)    │      │  (Gunicorn) │      │  (RDS/Cloud)│    │
│  └──────────────┘      └──────┬──────┘      └─────────────┘    │
│                               │                                  │
│                        ┌──────▼──────┐                          │
│                        │    Redis    │ (Sessions, Cache)        │
│                        └─────────────┘                          │
│                                                                  │
│  External Services:                                              │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │  Groq API   │  │  Sentry     │ (Error Monitoring)           │
│  └─────────────┘  └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Performance Considerations

### Optimization Strategies

1. **ML Model Loading**: Models loaded once at startup, kept in memory
2. **Database**: Connection pooling with SQLAlchemy
3. **LLM Calls**: Async requests, response streaming (planned)
4. **Frontend**: Lazy loading, minified assets (planned)

### Scalability Path

| Stage | Architecture | Capacity |
|-------|-------------|----------|
| MVP | Single server | ~100 users |
| Growth | Load balanced | ~10K users |
| Scale | Kubernetes | ~100K+ users |

---

## Future Architecture Enhancements

1. **Autonomous Health Agent**: Background agent for proactive health monitoring
2. **Real-time Updates**: WebSocket for live chat and notifications
3. **Microservices**: Split ML inference into separate service
4. **Event Sourcing**: Full audit trail of health data changes
5. **ML Pipeline**: MLflow for model versioning and A/B testing

---

*Last Updated: December 2025*
