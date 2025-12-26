# 🤝 Contributing to AI Health Platform

Thank you for your interest in contributing to the AI Health Platform! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Code Standards](#code-standards)
5. [Making Changes](#making-changes)
6. [Testing](#testing)
7. [Submitting Pull Requests](#submitting-pull-requests)
8. [ML Model Contributions](#ml-model-contributions)
9. [Documentation](#documentation)
10. [Community Guidelines](#community-guidelines)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.10+** installed
- **Git** for version control
- **pip** or **conda** for package management
- A **Groq API key** (for LLM features) - Get free at [console.groq.com](https://console.groq.com)
- Basic understanding of:
  - Python and FastAPI
  - Machine Learning concepts
  - REST API design

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/ai-health-platform.git
cd ai-health-platform
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/ai-health-platform.git
```

---

## Development Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required
SECRET_KEY=your-super-secret-key-change-in-production
GROQ_API_KEY=your-groq-api-key

# Optional
DATABASE_URL=sqlite:///./health_platform.db
DEBUG=true
GROQ_MODEL=llama-3.1-70b-versatile
```

### Train ML Models

```bash
# Download PCOS dataset (if not present)
python ml_training/datasets/download_pcos.py

# Train all models
python ml_training/train_diabetes.py
python ml_training/train_heart.py
python ml_training/train_pcos.py
```

### Run the Application

```bash
# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In a separate terminal, start frontend
cd frontend
python -m http.server 3000
```

### Verify Setup

- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

---

## Project Structure

```
ai-health-platform/
├── backend/
│   ├── app/                 # Main application code
│   │   ├── api/            # REST endpoints
│   │   ├── llm/            # LLM integration
│   │   ├── ml/             # ML inference
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── ml_training/        # Model training scripts
│   ├── models/             # Trained model files
│   └── tests/              # Test files
├── frontend/
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── *.html              # HTML pages
└── docs/                   # Documentation
```

### Key Files to Know

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app entry point |
| `app/config.py` | Configuration & settings |
| `app/llm/intent_router.py` | Intent detection system |
| `app/ml/*_model.py` | ML prediction modules |
| `ml_training/train_*.py` | Model training scripts |

---

## Code Standards

### Python Style Guide

We follow **PEP 8** with these additions:

```python
# File header docstring
"""
Module description
Brief explanation of what this module does
"""

# Import ordering
import standard_library  # 1. Standard library
import third_party       # 2. Third-party packages
from app import local    # 3. Local imports

# Class docstrings
class ExampleClass:
    """
    Brief class description.
    
    Longer description if needed.
    
    Attributes:
        attr_name: Description of attribute
    """

# Function docstrings
def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 10
        
    Returns:
        Dictionary containing result data
        
    Raises:
        ValueError: If param1 is empty
    """
```

### Type Hints

Always use type hints:

```python
# Good
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    return weight_kg / (height_m ** 2)

# Better (with Pydantic)
from pydantic import BaseModel

class BMIInput(BaseModel):
    weight_kg: float
    height_m: float

def calculate_bmi(data: BMIInput) -> float:
    return data.weight_kg / (data.height_m ** 2)
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | snake_case | `user_name` |
| Functions | snake_case | `get_user_profile()` |
| Classes | PascalCase | `UserProfile` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Files | snake_case | `user_service.py` |

### Error Handling

```python
# Use specific exceptions
from fastapi import HTTPException

# Good
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# Include context
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

---

## Making Changes

### Branch Naming

```
feature/short-description   # New features
bugfix/issue-description    # Bug fixes
docs/what-changed          # Documentation
refactor/what-changed      # Code refactoring
test/what-testing          # Test additions
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(ml): add XGBoost model for diabetes prediction
fix(api): handle missing glucose value in prediction
docs(readme): update installation instructions
test(auth): add JWT token expiration tests
```

### Keep Changes Small

- One feature/fix per PR
- Limit to ~300 lines of code changes
- Break large changes into smaller PRs

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/

# Run with verbose output
pytest -v
```

### Writing Tests

```python
# tests/test_diabetes_model.py
import pytest
from app.ml.diabetes_model import DiabetesPredictor

class TestDiabetesPredictor:
    """Tests for diabetes prediction model"""
    
    @pytest.fixture
    def predictor(self):
        """Create predictor instance"""
        return DiabetesPredictor()
    
    @pytest.fixture
    def valid_input(self):
        """Valid input data"""
        return {
            "Pregnancies": 2,
            "Glucose": 120,
            "BloodPressure": 70,
            "SkinThickness": 20,
            "Insulin": 80,
            "BMI": 25.5,
            "DiabetesPedigreeFunction": 0.5,
            "Age": 35
        }
    
    def test_prediction_returns_result(self, predictor, valid_input):
        """Test that prediction returns valid result"""
        result = predictor.predict(valid_input)
        
        assert result.risk_score >= 0
        assert result.risk_score <= 1
        assert result.risk_level in ["low", "medium", "high"]
    
    def test_high_glucose_increases_risk(self, predictor, valid_input):
        """Test that high glucose increases risk score"""
        normal_glucose = predictor.predict(valid_input)
        
        valid_input["Glucose"] = 200  # High glucose
        high_glucose = predictor.predict(valid_input)
        
        assert high_glucose.risk_score > normal_glucose.risk_score
    
    def test_invalid_input_raises_error(self, predictor):
        """Test that invalid input raises ValueError"""
        with pytest.raises(ValueError):
            predictor.predict({"Glucose": -100})  # Invalid
```

### Test Categories

| Category | Description | Location |
|----------|-------------|----------|
| Unit Tests | Test individual functions | `tests/unit/` |
| Integration Tests | Test API endpoints | `tests/integration/` |
| ML Tests | Test model predictions | `tests/ml/` |

---

## Submitting Pull Requests

### Before Submitting

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe how you tested these changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have added tests for new functionality
- [ ] All tests pass locally
- [ ] Documentation has been updated
```

### Review Process

1. Create PR against `main` branch
2. Automated tests run via CI
3. Maintainer reviews code
4. Address feedback
5. Merge when approved

---

## ML Model Contributions

### Adding a New Model

1. **Create training script** in `ml_training/`:
```python
# ml_training/train_new_condition.py
"""
Training script for New Condition prediction model
"""

def load_data():
    """Load and preprocess dataset"""
    pass

def train_model(X, y):
    """Train and validate model"""
    pass

def save_model(model, scaler, metrics):
    """Save model artifacts"""
    pass

if __name__ == "__main__":
    # Training pipeline
    X, y = load_data()
    model = train_model(X, y)
    save_model(model)
```

2. **Create inference module** in `app/ml/`:
```python
# app/ml/new_condition_model.py
"""
New Condition Prediction - Inference Module
"""
from app.ml.base_predictor import BaseHealthPredictor

class NewConditionPredictor(BaseHealthPredictor):
    def __init__(self):
        super().__init__("models/new_condition_model.pkl")
    
    def validate_input(self, features):
        # Validate input features
        pass
    
    def predict(self, features):
        # Make prediction
        pass
```

3. **Add API endpoint** in `app/api/health.py`:
```python
@router.post("/predict/new-condition")
async def predict_new_condition(data: NewConditionRequest):
    predictor = get_new_condition_predictor()
    return predictor.predict(data.dict())
```

### Model Requirements

- [ ] Training script with clear documentation
- [ ] Model performance metrics (AUC-ROC, accuracy, etc.)
- [ ] Feature importance analysis
- [ ] Bias evaluation across demographics
- [ ] Unit tests for inference
- [ ] Update README with model details

### Dataset Guidelines

- Use publicly available medical datasets
- Document data source and license
- Include data preprocessing steps
- Note any known biases

---

## Documentation

### What to Document

1. **Code Comments**: Explain *why*, not *what*
2. **Docstrings**: All public functions and classes
3. **README**: User-facing instructions
4. **Architecture**: System design decisions
5. **API Docs**: Endpoint usage (auto-generated)

### Documentation Style

```python
def calculate_risk_score(
    features: Dict[str, float],
    model_version: str = "1.0.0"
) -> RiskResult:
    """
    Calculate disease risk score from health features.
    
    This function takes health metrics and returns a risk assessment
    using the specified model version. Handles feature scaling and
    out-of-distribution detection internally.
    
    Args:
        features: Dictionary of health metrics including:
            - glucose: Blood glucose level (mg/dL)
            - bmi: Body Mass Index
            - age: Age in years
        model_version: Model version to use (default: latest)
    
    Returns:
        RiskResult containing:
            - risk_score: Float between 0-1
            - risk_level: "low", "medium", or "high"
            - confidence: Model confidence score
    
    Raises:
        ValueError: If required features are missing
        ModelNotFoundError: If specified model version doesn't exist
    
    Example:
        >>> features = {"glucose": 120, "bmi": 25.5, "age": 35}
        >>> result = calculate_risk_score(features)
        >>> print(f"Risk: {result.risk_level}")
        Risk: medium
    
    Note:
        Risk scores should be interpreted as statistical risk,
        not clinical diagnosis. Always recommend professional
        consultation for concerning results.
    """
```

---

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person
- No harassment or discrimination

### Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue
- **Security**: Email maintainers directly

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked in documentation

---

## Quick Reference

### Useful Commands

```bash
# Backend
uvicorn app.main:app --reload          # Start dev server
pytest                                   # Run tests
pip freeze > requirements.txt           # Update dependencies

# ML
python ml_training/train_diabetes.py    # Train diabetes model
python ml_training/evaluate.py          # Evaluate all models

# Git
git fetch upstream                      # Sync with upstream
git rebase upstream/main               # Rebase on main
```

### File Templates

New API endpoint:
```python
# app/api/new_endpoint.py
from fastapi import APIRouter, Depends
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_items(current_user = Depends(get_current_user)):
    """Get all items for current user"""
    return {"items": []}
```

---

Thank you for contributing to making health AI more accessible and responsible! 🙏

---

*Last Updated: December 2025*
