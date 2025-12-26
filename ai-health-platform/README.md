# 🏥 AI Health Companion Platform

An intelligent health monitoring and prediction platform powered by Machine Learning and Natural Language Processing.

## 🎯 Project Overview

This platform provides:
- **AI-Powered Health Chat**: Context-aware conversational AI with intent detection
- **ML-Based Health Predictions**: Diabetes, Heart Disease, and PCOS risk assessment
- **Real Medical Datasets**: Trained on verified clinical datasets (PIMA Indians, UCI Heart Disease)
- **Modern Web Interface**: Responsive frontend with real-time predictions

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance async Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **Groq API**: LLM integration for intelligent chat
- **scikit-learn**: Machine learning models
- **imbalanced-learn**: SMOTE for class balancing

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript (ES6+)**: Async API integration
- **Chart.js**: Health trend visualization

### Machine Learning
- **Models**: Random Forest, Gradient Boosting, Logistic Regression
- **Datasets**: PIMA Indians Diabetes, UCI Heart Disease, PCOS Clinical
- **Techniques**: Feature engineering, cross-validation, SMOTE oversampling

## 📊 Model Performance

| Model | Dataset | ROC-AUC | Accuracy |
|-------|---------|---------|----------|
| Diabetes | PIMA Indians (768 samples) | 0.829 | 77.3% |
| Heart Disease | UCI Cleveland (303 samples) | 0.947 | 88.5% |
| PCOS | Clinical PCOS (541 samples) | 0.795 | 76.2% |

## 🚀 Key Features

### 1. Intent-Aware AI Chat
- **12 Health Intents**: Mental health, physical symptoms, nutrition, fitness, sleep, etc.
- **Crisis Detection**: Automatic detection of mental health emergencies
- **Conversation Memory**: Context-aware responses across sessions
- **Specialized Prompts**: Intent-specific system prompts for accurate responses

### 2. Diabetes Risk Prediction
- Features: Glucose, BMI, Blood Pressure, Age, Pregnancy history
- Dataset: PIMA Indians Diabetes Dataset (NIH)
- Model: Random Forest with SMOTE balancing

### 3. Heart Disease Risk Prediction
- Features: Age, Sex, Chest Pain Type, Cholesterol, ECG, etc.
- Dataset: UCI Heart Disease Dataset (Cleveland)
- Model: Random Forest Classifier

### 4. PCOS Risk Assessment
- Features: Cycle regularity, BMI, Hormonal indicators, Lifestyle factors
- Dataset: Clinical PCOS data based on Rotterdam criteria
- Model: Gradient Boosting with 18 clinical features

### 5. Mental Wellness Check
- PHQ-2/GAD-2 inspired screening
- Mood tracking and recommendations

## 📁 Project Structure

```
ai-health-platform/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   │   ├── auth.py       # JWT authentication
│   │   │   ├── chat.py       # Chat endpoints
│   │   │   ├── health.py     # Prediction endpoints
│   │   │   └── dashboard.py  # Dashboard data
│   │   ├── llm/
│   │   │   ├── intent_router.py    # Intent detection system
│   │   │   └── groq_provider.py    # LLM integration
│   │   ├── ml/               # ML inference modules
│   │   │   ├── diabetes_model.py
│   │   │   ├── heart_model.py
│   │   │   └── pcos_model.py
│   │   ├── models/           # SQLAlchemy models
│   │   └── schemas/          # Pydantic schemas
│   ├── ml_training/          # Training pipelines
│   │   ├── train_diabetes.py
│   │   ├── train_heart.py
│   │   ├── train_pcos.py
│   │   └── datasets/
│   ├── models/               # Saved ML models (.pkl)
│   └── requirements.txt
├── frontend/
│   ├── index.html           # Main application
│   ├── dashboard.html       # Health dashboard
│   └── onboarding.html      # User onboarding
└── README.md
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js (optional, for frontend development)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Train ML models
python ml_training/datasets/download_pcos.py
python ml_training/train_diabetes.py
python ml_training/train_heart.py
python ml_training/train_pcos.py

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
python -m http.server 3000
```

### Environment Variables
Create `.env` in backend directory:
```env
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=sqlite:///./health_companion.db
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login (returns JWT)

### Health Predictions
- `POST /api/health/predict/diabetes` - Diabetes risk prediction
- `POST /api/health/predict/heart` - Heart disease prediction
- `POST /api/health/predict/pcos` - PCOS risk assessment

### Chat
- `POST /api/chat/send` - Send message to AI assistant
- `GET /api/chat/history` - Get chat history

## 🔬 Machine Learning Pipeline

### Training Process
1. **Data Loading**: Load verified clinical datasets
2. **EDA**: Statistical analysis and visualization
3. **Preprocessing**: Handle missing values, feature scaling
4. **Class Balancing**: SMOTE for imbalanced datasets
5. **Model Training**: Cross-validation with multiple algorithms
6. **Evaluation**: ROC-AUC, Precision, Recall, F1-Score
7. **Deployment**: Save model with scaler for inference

### Feature Importance (Example: PCOS Model)
```
Cycle_length: 0.207
BMI: 0.125
AMH: 0.122
FSH_LH: 0.112
Hair_growth: 0.104
```

## 🔐 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- SQL injection prevention via ORM

## 🤖 Intent Detection System

The chatbot uses a sophisticated intent detection system:

```python
class HealthIntent(Enum):
    MENTAL_HEALTH = "mental_health"
    PHYSICAL_SYMPTOMS = "physical_symptoms"
    NUTRITION_DIET = "nutrition_diet"
    FITNESS_EXERCISE = "fitness_exercise"
    SLEEP_FATIGUE = "sleep_fatigue"
    DIABETES_RELATED = "diabetes_related"
    HEART_RELATED = "heart_related"
    PCOS_RELATED = "pcos_related"
    CRISIS = "crisis"  # Emergency detection
```

Each intent has specialized prompts for accurate, context-aware responses.

## 📈 Future Enhancements

- [ ] Voice input support
- [ ] Wearable device integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)

## 👤 Author

Built as a full-stack AI/ML portfolio project demonstrating:
- Machine Learning model development
- Natural Language Processing
- Full-stack web development
- RESTful API design
- Database design and management

## 📄 License

MIT License - Feel free to use for educational purposes.

---

⚠️ **Disclaimer**: This application is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers for any medical conditions.
