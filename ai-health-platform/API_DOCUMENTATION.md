# 📚 AI Health Platform - API Documentation

## Overview

This document provides comprehensive API documentation for the AI Health Platform. The API is built with FastAPI and follows RESTful principles.

**Base URL**: `http://localhost:8000/api/v1`

**Interactive Docs**: http://localhost:8000/docs (Swagger UI)

---

## Table of Contents
1. [Authentication](#authentication)
2. [Health Predictions](#health-predictions)
3. [Chat API](#chat-api)
4. [Habits API](#habits-api)
5. [Dashboard API](#dashboard-api)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Code Examples](#code-examples)

---

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### Register New User

Create a new user account.

```http
POST /api/v1/auth/register
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male",
  "is_active": true,
  "created_at": "2025-12-26T10:30:00Z"
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400 | Invalid email format or weak password |
| 409 | Email already registered |

---

### Login

Authenticate and receive JWT token.

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
```

**Request Body:**
```
username=user@example.com&password=securepassword123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 401 | Invalid email or password |
| 403 | Account disabled |

---

### Get Current User

Get authenticated user's profile.

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male",
  "is_active": true,
  "created_at": "2025-12-26T10:30:00Z"
}
```

---

## Health Predictions

### Diabetes Risk Prediction

Assess diabetes risk based on health metrics.

```http
POST /api/v1/health/predict/diabetes
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "pregnancies": 2,
  "glucose": 120,
  "blood_pressure": 70,
  "skin_thickness": 20,
  "insulin": 80,
  "bmi": 25.5,
  "diabetes_pedigree": 0.5,
  "age": 35
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| pregnancies | int | 0-20 | Number of pregnancies (0 for males) |
| glucose | float | 40-400 | Plasma glucose concentration (mg/dL) |
| blood_pressure | float | 40-200 | Diastolic blood pressure (mm Hg) |
| skin_thickness | float | 0-100 | Triceps skin fold thickness (mm) |
| insulin | float | 0-1000 | 2-hour serum insulin (mu U/ml) |
| bmi | float | 10-60 | Body Mass Index (kg/m²) |
| diabetes_pedigree | float | 0-3 | Diabetes pedigree function |
| age | int | 18-120 | Age in years |

**Response (200 OK):**
```json
{
  "disease_type": "diabetes",
  "risk_score": 0.45,
  "risk_level": "medium",
  "confidence": 0.85,
  "explanation": "Based on your health metrics, you have a moderate risk of developing Type 2 diabetes.",
  "contributing_factors": [
    {
      "feature": "Glucose",
      "value": 120,
      "impact": "medium",
      "description": "Blood glucose in pre-diabetic range (100-125 mg/dL)"
    },
    {
      "feature": "BMI",
      "value": 25.5,
      "impact": "low",
      "description": "BMI in overweight range (25-30)"
    }
  ],
  "recommendations": [
    "Schedule a fasting glucose test with your doctor",
    "Maintain regular physical activity (150 min/week)",
    "Consider reducing refined carbohydrates",
    "Monitor blood glucose regularly"
  ],
  "model_version": "1.0.0",
  "timestamp": "2025-12-26T10:30:00Z",
  "disclaimer": "This is a screening tool based on statistical analysis. It is NOT a medical diagnosis. Please consult a healthcare provider for proper evaluation."
}
```

**Risk Level Interpretation:**

| Risk Level | Score Range | Recommendation |
|------------|-------------|----------------|
| low | 0-30% | Continue healthy lifestyle, routine checkups |
| medium | 30-60% | Consult doctor, lifestyle modifications |
| high | 60-100% | Urgent medical consultation recommended |

---

### Heart Disease Prediction

Assess cardiovascular disease risk.

```http
POST /api/v1/health/predict/heart
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "age": 55,
  "sex": 1,
  "cp": 2,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.5,
  "slope": 1,
  "ca": 0,
  "thal": 2
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| age | int | 20-100 | Age in years |
| sex | int | 0-1 | 0 = Female, 1 = Male |
| cp | int | 0-3 | Chest pain type: 0=Typical angina, 1=Atypical, 2=Non-anginal, 3=Asymptomatic |
| trestbps | int | 80-200 | Resting blood pressure (mm Hg) |
| chol | int | 100-600 | Serum cholesterol (mg/dl) |
| fbs | int | 0-1 | Fasting blood sugar > 120 mg/dl: 0=No, 1=Yes |
| restecg | int | 0-2 | Resting ECG: 0=Normal, 1=ST-T abnormality, 2=LV hypertrophy |
| thalach | int | 60-220 | Maximum heart rate achieved |
| exang | int | 0-1 | Exercise induced angina: 0=No, 1=Yes |
| oldpeak | float | 0-6 | ST depression induced by exercise |
| slope | int | 0-2 | Slope of peak exercise ST: 0=Upsloping, 1=Flat, 2=Downsloping |
| ca | int | 0-4 | Number of major vessels colored by fluoroscopy |
| thal | int | 0-3 | Thalassemia: 0=Normal, 1=Fixed defect, 2=Reversible, 3=Unknown |

**Response (200 OK):**
```json
{
  "disease_type": "heart_disease",
  "risk_score": 0.72,
  "risk_level": "high",
  "confidence": 0.88,
  "prediction": 1,
  "recommendations": [
    "Consult a cardiologist for comprehensive heart health evaluation",
    "Your resting blood pressure is elevated. Monitor regularly",
    "Consider dietary changes to lower cholesterol levels",
    "Maintain a heart-healthy diet low in saturated fats and sodium",
    "Regular moderate exercise (30 min, 5 days/week) as cleared by your doctor"
  ],
  "model_version": "1.0.0",
  "disclaimer": "This is a screening tool based on statistical analysis. It is NOT a diagnosis. Please consult a cardiologist for proper evaluation."
}
```

---

### PCOS Risk Assessment

Assess Polycystic Ovary Syndrome risk.

```http
POST /api/v1/health/predict/pcos
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "age": 28,
  "bmi": 27.5,
  "weight": 70,
  "cycle_length": 3,
  "cycle_regularity": 1,
  "weight_gain": 1,
  "hair_growth": 1,
  "skin_darkening": 0,
  "pimples": 1,
  "fast_food": 1,
  "regular_exercise": 0,
  "follicle_count_l": 15,
  "follicle_count_r": 12,
  "amh": 5.5,
  "lh": 12,
  "fsh": 5
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| age | int | 15-50 | Age in years |
| bmi | float | 15-50 | Body Mass Index |
| weight | float | 30-150 | Weight in kg |
| cycle_length | int | 1-4 | 1=Regular, 2=Slightly irregular, 3=Irregular, 4=Very irregular/absent |
| cycle_regularity | int | 0-1 | 0=Regular, 1=Irregular |
| weight_gain | int | 0-1 | Recent unexplained weight gain: 0=No, 1=Yes |
| hair_growth | int | 0-1 | Excess facial/body hair: 0=No, 1=Yes |
| skin_darkening | int | 0-1 | Skin darkening (acanthosis): 0=No, 1=Yes |
| pimples | int | 0-1 | Persistent acne: 0=No, 1=Yes |
| fast_food | int | 0-1 | Regular fast food consumption: 0=No, 1=Yes |
| regular_exercise | int | 0-1 | Regular exercise: 0=No, 1=Yes |
| follicle_count_l | int | optional | Left ovary follicle count (from ultrasound) |
| follicle_count_r | int | optional | Right ovary follicle count (from ultrasound) |
| amh | float | optional | Anti-Mullerian Hormone level (ng/mL) |
| lh | float | optional | Luteinizing Hormone level (mIU/mL) |
| fsh | float | optional | Follicle Stimulating Hormone level (mIU/mL) |

**Response (200 OK):**
```json
{
  "disease_type": "pcos",
  "risk_score": 0.68,
  "risk_level": "high",
  "confidence": 0.79,
  "prediction": 1,
  "recommendations": [
    "Consult a gynecologist for proper PCOS evaluation",
    "Your elevated LH/FSH ratio is a common PCOS indicator",
    "Consider a low-glycemic diet to help manage symptoms",
    "Regular exercise can help improve insulin sensitivity",
    "Track your menstrual cycle for better pattern recognition"
  ],
  "model_version": "1.0.0",
  "disclaimer": "This is a screening tool based on statistical analysis. It is NOT a diagnosis. Please consult a gynecologist for proper evaluation."
}
```

---

## Chat API

### Send Chat Message (Authenticated)

Send a message to the AI health assistant with conversation history.

```http
POST /api/v1/chat/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "I've been feeling very anxious lately and having trouble sleeping"
}
```

**Response (200 OK):**
```json
{
  "response": "I hear you, and I want you to know that what you're experiencing is valid. Anxiety and sleep difficulties often go hand in hand, and many people struggle with this.\n\nCan you tell me a bit more about your situation? For instance:\n- How long have you been feeling this way?\n- Are there specific thoughts keeping you awake?\n- Have you noticed any triggers for your anxiety?\n\nIn the meantime, one technique that many find helpful is the 4-7-8 breathing method: breathe in for 4 seconds, hold for 7, and exhale slowly for 8. This can help calm your nervous system before bed.\n\nRemember, if these feelings persist, it might be worth speaking with a mental health professional who can provide personalized support."
}
```

### Send Chat Message (Public)

Send a message without authentication.

```http
POST /api/v1/chat/public
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What are some healthy breakfast options?"
}
```

**Response (200 OK):**
```json
{
  "response": "Great question! Here are some nutritious breakfast options:\n\n**Quick & Easy:**\n- Greek yogurt with berries and a handful of nuts\n- Overnight oats with chia seeds and banana\n- Whole grain toast with avocado and eggs\n\n**If You Have More Time:**\n- Vegetable omelette with spinach and tomatoes\n- Smoothie bowl with fruits, spinach, and protein powder\n- Poha or upma with vegetables (Indian options)\n\n**Key Principles:**\n- Include protein to stay full longer\n- Add fiber from whole grains or fruits\n- Limit added sugars\n\nWould you like more specific suggestions based on any dietary preferences or health goals?"
}
```

### Get Chat History

Retrieve conversation history for authenticated user.

```http
GET /api/v1/chat/history
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "role": "user",
    "content": "I've been having headaches frequently",
    "created_at": "2025-12-26T09:00:00Z"
  },
  {
    "role": "assistant",
    "content": "I'm sorry to hear you're experiencing frequent headaches...",
    "created_at": "2025-12-26T09:00:05Z"
  },
  {
    "role": "user",
    "content": "They usually happen in the afternoon",
    "created_at": "2025-12-26T09:01:00Z"
  },
  {
    "role": "assistant",
    "content": "Afternoon headaches can have several causes...",
    "created_at": "2025-12-26T09:01:03Z"
  }
]
```

---

## Habits API

### List User Habits

Get all habits for authenticated user.

```http
GET /api/v1/habits/
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "30-min Daily Exercise",
    "description": "Walking, jogging, or any cardio activity",
    "frequency": "daily",
    "target_condition": "diabetes",
    "is_active": true,
    "streak": 5,
    "last_logged": "2025-12-25T18:00:00Z",
    "created_at": "2025-12-20T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Blood Glucose Monitoring",
    "description": "Check blood sugar levels",
    "frequency": "daily",
    "target_condition": "diabetes",
    "is_active": true,
    "streak": 12,
    "last_logged": "2025-12-26T08:00:00Z",
    "created_at": "2025-12-14T10:00:00Z"
  }
]
```

### Create New Habit

Create a custom health habit.

```http
POST /api/v1/habits/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Meditation",
  "description": "10 minutes of mindful meditation",
  "frequency": "daily",
  "target_condition": "mental_health"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Meditation",
  "description": "10 minutes of mindful meditation",
  "frequency": "daily",
  "target_condition": "mental_health",
  "is_active": true,
  "streak": 0,
  "last_logged": null,
  "created_at": "2025-12-26T10:30:00Z"
}
```

### Log Habit Completion

Mark a habit as completed for today.

```http
POST /api/v1/habits/{habit_id}/log
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "notes": "Completed 30 minutes of jogging",
  "value": 30
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "habit_id": 1,
  "logged_at": "2025-12-26T18:00:00Z",
  "new_streak": 6,
  "message": "Great job! You've maintained a 6-day streak!"
}
```

### Update Habit

Update an existing habit.

```http
PUT /api/v1/habits/{habit_id}
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "45-min Daily Exercise",
  "description": "Increased exercise duration",
  "frequency": "daily"
}
```

### Delete Habit

Delete a habit.

```http
DELETE /api/v1/habits/{habit_id}
Authorization: Bearer <token>
```

**Response (204 No Content)**

---

## Dashboard API

### Get Dashboard Summary

Get aggregated health data for dashboard.

```http
GET /api/v1/dashboard/summary
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "user": {
    "name": "John Doe",
    "member_since": "2025-12-01"
  },
  "health_profile": {
    "age": 35,
    "gender": "male",
    "bmi": 25.5,
    "last_updated": "2025-12-25T10:00:00Z"
  },
  "recent_predictions": [
    {
      "disease_type": "diabetes",
      "risk_level": "medium",
      "risk_score": 0.45,
      "date": "2025-12-26"
    },
    {
      "disease_type": "heart_disease",
      "risk_level": "low",
      "risk_score": 0.22,
      "date": "2025-12-24"
    }
  ],
  "habits_summary": {
    "active_habits": 3,
    "completed_today": 2,
    "current_streaks": {
      "exercise": 6,
      "meditation": 3
    }
  },
  "insights": [
    "Your glucose levels have improved by 10% this month",
    "Great job maintaining your exercise streak!",
    "Consider adding more fiber to your diet"
  ]
}
```

### Get Health Trends

Get historical health data for charts.

```http
GET /api/v1/dashboard/trends?days=30
Authorization: Bearer <token>
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| days | int | 30 | Number of days of history |

**Response (200 OK):**
```json
{
  "predictions": {
    "diabetes": [
      {"date": "2025-12-01", "risk_score": 0.52},
      {"date": "2025-12-10", "risk_score": 0.48},
      {"date": "2025-12-20", "risk_score": 0.45},
      {"date": "2025-12-26", "risk_score": 0.42}
    ],
    "heart_disease": [
      {"date": "2025-12-05", "risk_score": 0.28},
      {"date": "2025-12-24", "risk_score": 0.22}
    ]
  },
  "habits": {
    "exercise": [
      {"date": "2025-12-20", "completed": true},
      {"date": "2025-12-21", "completed": true},
      {"date": "2025-12-22", "completed": false},
      {"date": "2025-12-23", "completed": true}
    ]
  },
  "summary": {
    "avg_diabetes_risk": 0.47,
    "risk_trend": "improving",
    "habit_completion_rate": 0.75
  }
}
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Or for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "glucose"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### HTTP Status Codes

| Code | Description | When Used |
|------|-------------|-----------|
| 200 | OK | Successful request |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Common Errors

**Authentication Errors:**
```json
// 401 - Missing token
{
  "detail": "Not authenticated"
}

// 401 - Invalid token
{
  "detail": "Could not validate credentials"
}

// 401 - Expired token
{
  "detail": "Token has expired"
}
```

**Validation Errors:**
```json
// 422 - Invalid field value
{
  "detail": [
    {
      "loc": ["body", "glucose"],
      "msg": "ensure this value is greater than or equal to 40",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 40}
    }
  ]
}
```

**Model Errors:**
```json
// 500 - Model not loaded
{
  "detail": "Diabetes model not found. Please ensure models are trained."
}
```

---

## Rate Limiting

To protect the service, rate limits may be applied:

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Authentication | 10 requests | per minute |
| Predictions | 30 requests | per minute |
| Chat | 60 requests | per minute |
| General | 100 requests | per minute |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1703593200
```

**Rate Limit Exceeded Response (429):**
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

## Code Examples

### Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "user@example.com",
        "password": "password123"
    }
)
token = response.json()["access_token"]

# Make prediction
headers = {"Authorization": f"Bearer {token}"}
prediction_data = {
    "pregnancies": 2,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 80,
    "bmi": 25.5,
    "diabetes_pedigree": 0.5,
    "age": 35
}

response = requests.post(
    f"{BASE_URL}/health/predict/diabetes",
    json=prediction_data,
    headers=headers
)

result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']:.1%}")
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Login
async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    return data.access_token;
}

// Make prediction
async function predictDiabetes(token, healthData) {
    const response = await fetch(`${BASE_URL}/health/predict/diabetes`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(healthData)
    });
    
    return response.json();
}

// Usage
const token = await login('user@example.com', 'password123');
const result = await predictDiabetes(token, {
    pregnancies: 2,
    glucose: 120,
    blood_pressure: 70,
    skin_thickness: 20,
    insulin: 80,
    bmi: 25.5,
    diabetes_pedigree: 0.5,
    age: 35
});

console.log(`Risk: ${result.risk_level} (${(result.risk_score * 100).toFixed(1)}%)`);
```

### cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Save token
TOKEN="your_token_here"

# Diabetes prediction
curl -X POST "http://localhost:8000/api/v1/health/predict/diabetes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 2,
    "glucose": 120,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 80,
    "bmi": 25.5,
    "diabetes_pedigree": 0.5,
    "age": 35
  }'

# Public chat (no auth)
curl -X POST "http://localhost:8000/api/v1/chat/public" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are symptoms of diabetes?"}'
```

---

## Postman Collection

Import this collection into Postman for easy API testing:

```json
{
  "info": {
    "name": "AI Health Platform API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8000/api/v1"
    },
    {
      "key": "token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/auth/login"
          }
        }
      ]
    },
    {
      "name": "Health",
      "item": [
        {
          "name": "Predict Diabetes",
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/health/predict/diabetes"
          }
        }
      ]
    }
  ]
}
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Dec 2025 | Initial API release |

---

*For questions or issues, please open a GitHub issue or contact the maintainers.*

*Last Updated: December 2025*
