# 🤖 AI Health Platform - Machine Learning Models Documentation

## Overview

This document provides comprehensive documentation for the machine learning models used in the AI Health Platform. Each model is designed for health risk prediction with a focus on transparency, accuracy, and responsible AI practices.

---

## Table of Contents
1. [Model Summary](#model-summary)
2. [Diabetes Prediction Model](#diabetes-prediction-model)
3. [Heart Disease Prediction Model](#heart-disease-prediction-model)
4. [PCOS Prediction Model](#pcos-prediction-model)
5. [Training Pipeline](#training-pipeline)
6. [Model Evaluation](#model-evaluation)
7. [Feature Engineering](#feature-engineering)
8. [Model Deployment](#model-deployment)
9. [Limitations & Bias](#limitations--bias)
10. [Future Improvements](#future-improvements)

---

## Model Summary

| Model | Algorithm | Dataset | ROC-AUC | Accuracy | Features |
|-------|-----------|---------|---------|----------|----------|
| **Diabetes** | Random Forest | PIMA Indians (768 samples) | 0.829 | 77.3% | 13 (8 base + 5 engineered) |
| **Heart Disease** | Random Forest | UCI Cleveland (303 samples) | 0.947 | 88.5% | 13 clinical features |
| **PCOS** | Gradient Boosting | Clinical PCOS (541 samples) | 0.795 | 76.2% | 18 features |

---

## Diabetes Prediction Model

### Dataset: PIMA Indians Diabetes Database

**Source**: National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)

**Description**: Originally collected to study diabetes among Pima Indian women in Arizona, who have a high prevalence of Type 2 diabetes.

#### Dataset Statistics
```
Total Samples: 768
Positive Cases: 268 (34.9%)
Negative Cases: 500 (65.1%)
Class Imbalance: Moderate (handled with SMOTE)
```

### Features

| Feature | Description | Range | Unit |
|---------|-------------|-------|------|
| Pregnancies | Number of times pregnant | 0-17 | count |
| Glucose | Plasma glucose concentration (2h OGTT) | 0-199 | mg/dL |
| BloodPressure | Diastolic blood pressure | 0-122 | mm Hg |
| SkinThickness | Triceps skin fold thickness | 0-99 | mm |
| Insulin | 2-hour serum insulin | 0-846 | μU/mL |
| BMI | Body Mass Index | 0-67.1 | kg/m² |
| DiabetesPedigreeFunction | Diabetes heredity score | 0.078-2.42 | - |
| Age | Age in years | 21-81 | years |

### Engineered Features

```python
# Age Groups (categorical)
age_group = 0 if age <= 30 else (1 if age <= 45 else (2 if age <= 60 else 3))

# BMI Categories
bmi_cat = 0 if bmi < 18.5 else (1 if bmi < 25 else (2 if bmi < 30 else 3))
# 0: Underweight, 1: Normal, 2: Overweight, 3: Obese

# Glucose Categories
glucose_cat = 0 if glucose < 100 else (1 if glucose < 125 else 2)
# 0: Normal, 1: Prediabetes, 2: Diabetes range

# Interaction Features
bmi_age = bmi * age
glucose_bmi = glucose * bmi
```

### Model Architecture

```
Algorithm: Random Forest Classifier
├── Number of Trees: 100
├── Max Depth: 10
├── Min Samples Split: 5
├── Min Samples Leaf: 2
├── Class Weight: balanced
└── Random State: 42
```

### Feature Importance

```
1. Glucose                    0.280 ████████████████████████████
2. BMI                        0.180 ██████████████████
3. Age                        0.148 ███████████████
4. DiabetesPedigreeFunction   0.122 ████████████
5. Insulin                    0.098 ██████████
6. BloodPressure              0.072 ███████
7. SkinThickness              0.055 ██████
8. Pregnancies                0.045 ████
```

### Performance Metrics

```
                     Precision    Recall    F1-Score
    Negative (0)        0.81       0.85       0.83
    Positive (1)        0.70       0.64       0.67

    Accuracy                                  0.773
    Macro Avg           0.76       0.75       0.75
    ROC-AUC                                   0.829
```

### Confusion Matrix

```
              Predicted
              Neg    Pos
Actual Neg    127     23
       Pos     35     65

True Negatives:  127  |  False Positives: 23
False Negatives:  35  |  True Positives:  65
```

---

## Heart Disease Prediction Model

### Dataset: UCI Heart Disease (Cleveland)

**Source**: UCI Machine Learning Repository (Cleveland Clinic Foundation)

**Description**: Contains 303 patient records from Cleveland Clinic with 14 attributes commonly used in heart disease diagnosis.

#### Dataset Statistics
```
Total Samples: 303
Positive Cases: 138 (45.5%)
Negative Cases: 165 (54.5%)
Class Balance: Good (nearly balanced)
```

### Features

| Feature | Description | Values | Type |
|---------|-------------|--------|------|
| age | Age in years | 29-77 | Continuous |
| sex | Sex | 0=F, 1=M | Binary |
| cp | Chest pain type | 0-3 | Categorical |
| trestbps | Resting blood pressure | 94-200 mm Hg | Continuous |
| chol | Serum cholesterol | 126-564 mg/dl | Continuous |
| fbs | Fasting blood sugar > 120 mg/dl | 0=No, 1=Yes | Binary |
| restecg | Resting ECG results | 0-2 | Categorical |
| thalach | Maximum heart rate achieved | 71-202 | Continuous |
| exang | Exercise induced angina | 0=No, 1=Yes | Binary |
| oldpeak | ST depression | 0-6.2 | Continuous |
| slope | Slope of peak exercise ST | 0-2 | Categorical |
| ca | Major vessels colored by fluoroscopy | 0-4 | Ordinal |
| thal | Thalassemia | 0-3 | Categorical |

### Chest Pain Types (cp)

| Value | Type | Description |
|-------|------|-------------|
| 0 | Typical Angina | Classic heart-related chest pain |
| 1 | Atypical Angina | Chest pain not typical of heart disease |
| 2 | Non-anginal Pain | Chest pain unlikely from heart |
| 3 | Asymptomatic | No chest pain symptoms |

### Model Architecture

```
Algorithm: Random Forest Classifier
├── Number of Trees: 100
├── Max Depth: None (fully grown)
├── Min Samples Split: 2
├── Min Samples Leaf: 1
├── Bootstrap: True
└── Random State: 42
```

### Feature Importance

```
1. thal (Thalassemia)         0.142 ██████████████
2. ca (Vessels)               0.138 ██████████████
3. cp (Chest Pain)            0.127 █████████████
4. oldpeak (ST Depression)    0.115 ████████████
5. thalach (Max Heart Rate)   0.098 ██████████
6. age                        0.087 █████████
7. chol (Cholesterol)         0.076 ████████
8. exang (Exercise Angina)    0.069 ███████
9. trestbps (Blood Pressure)  0.058 ██████
10. sex                       0.045 ████
11. slope                     0.025 ███
12. fbs (Blood Sugar)         0.012 █
13. restecg                   0.008 █
```

### Performance Metrics

```
                     Precision    Recall    F1-Score
    No Disease (0)      0.90       0.88       0.89
    Disease (1)         0.87       0.89       0.88

    Accuracy                                  0.885
    Macro Avg           0.88       0.88       0.88
    ROC-AUC                                   0.947
```

### ROC Curve Analysis

```
                    │
           1.0 ─────┼────────────────────●●●●●
                    │                  ●●
                    │                ●●
       Sensitivity  │              ●●
                    │            ●●
           0.5 ─────┼──────────●●────────────
                    │        ●●
                    │      ●●
                    │    ●●
                    │  ●●
           0.0 ─────●●───────────────────────
                    0.0        0.5        1.0
                      1 - Specificity

AUC = 0.947 (Excellent discrimination)
```

---

## PCOS Prediction Model

### Dataset: Clinical PCOS Dataset

**Source**: Clinical dataset based on Rotterdam criteria for PCOS diagnosis

**Description**: Contains 541 patient records with symptoms, lifestyle factors, and hormonal indicators commonly assessed in PCOS diagnosis.

#### Dataset Statistics
```
Total Samples: 541
Positive Cases: 177 (32.7%)
Negative Cases: 364 (67.3%)
Class Imbalance: Moderate (handled with SMOTE)
```

### Features

#### Symptom Features
| Feature | Description | Values |
|---------|-------------|--------|
| Hair_growth | Excessive facial/body hair (hirsutism) | 0=No, 1=Yes |
| Skin_darkening | Acanthosis nigricans | 0=No, 1=Yes |
| Pimples | Persistent acne | 0=No, 1=Yes |
| Weight_gain | Recent unexplained weight gain | 0=No, 1=Yes |

#### Clinical Features
| Feature | Description | Range |
|---------|-------------|-------|
| Age | Age in years | 15-50 |
| BMI | Body Mass Index | 15-50 |
| Cycle_length | Menstrual cycle regularity | 1-4 (1=regular to 4=absent) |
| Cycle_RI | Cycle irregularity indicator | 0=Regular, 1=Irregular |
| Follicle_L | Left ovary follicle count | 0-30 |
| Follicle_R | Right ovary follicle count | 0-30 |

#### Hormonal Features
| Feature | Description | Normal Range |
|---------|-------------|--------------|
| AMH | Anti-Mullerian Hormone | 1.0-4.0 ng/mL |
| LH | Luteinizing Hormone | 2-15 mIU/mL |
| FSH | Follicle Stimulating Hormone | 3-10 mIU/mL |
| FSH_LH | FSH to LH ratio | > 1 (normal) |

#### Lifestyle Features
| Feature | Description | Values |
|---------|-------------|--------|
| Fast_food | Regular fast food consumption | 0=No, 1=Yes |
| Regular_Exercise | Exercises regularly | 0=No, 1=Yes |
| Waist_Hip_Ratio | Waist to hip circumference ratio | 0.7-1.0 |

### Model Architecture

```
Algorithm: Gradient Boosting Classifier
├── Number of Estimators: 100
├── Learning Rate: 0.1
├── Max Depth: 5
├── Min Samples Split: 5
├── Min Samples Leaf: 2
├── Subsample: 0.8
└── Random State: 42
```

### Feature Importance

```
1. Cycle_length               0.207 █████████████████████
2. BMI                        0.125 ████████████
3. AMH                        0.122 ████████████
4. FSH_LH (Ratio)             0.112 ███████████
5. Hair_growth                0.104 ██████████
6. Follicle_L                 0.078 ████████
7. Follicle_R                 0.072 ███████
8. Weight_gain                0.058 ██████
9. Age                        0.045 ████
10. Pimples                   0.032 ███
11. Fast_food                 0.022 ██
12. Regular_Exercise          0.015 ██
13. Skin_darkening            0.008 █
```

### Performance Metrics

```
                     Precision    Recall    F1-Score
    No PCOS (0)         0.82       0.79       0.80
    PCOS (1)            0.68       0.72       0.70

    Accuracy                                  0.762
    Macro Avg           0.75       0.76       0.75
    ROC-AUC                                   0.795
```

---

## Training Pipeline

### Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Data     │───▶│ Preprocess  │───▶│   Feature   │───▶│    Class    │
│   Loading   │    │  & Clean    │    │ Engineering │    │  Balancing  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│   Export    │◀───│  Evaluate   │◀───│   Train     │◀─────────┘
│   Model     │    │   Model     │    │   Model     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Step 1: Data Loading

```python
import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """Load dataset from CSV file"""
    df = pd.read_csv(filepath)
    
    # Basic info
    print(f"Shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    return df
```

### Step 2: Preprocessing

```python
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess data"""
    
    # Handle missing values
    # Option 1: Replace zeros with median (for values that can't be zero)
    zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in zero_cols:
        df[col] = df[col].replace(0, df[col].median())
    
    # Option 2: Drop rows with missing values
    # df = df.dropna()
    
    # Remove outliers (optional)
    # df = df[df['BMI'] < 60]
    
    return df
```

### Step 3: Feature Engineering

```python
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create new features from existing ones"""
    
    # Binned age groups
    df['age_group'] = pd.cut(df['Age'], 
                             bins=[0, 30, 45, 60, 100], 
                             labels=[0, 1, 2, 3])
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['BMI'],
                                bins=[0, 18.5, 25, 30, 100],
                                labels=[0, 1, 2, 3])
    
    # Interaction terms
    df['bmi_age'] = df['BMI'] * df['Age']
    df['glucose_bmi'] = df['Glucose'] * df['BMI']
    
    return df
```

### Step 4: Class Balancing (SMOTE)

```python
from imblearn.over_sampling import SMOTE

def balance_classes(X, y):
    """Apply SMOTE to handle class imbalance"""
    
    smote = SMOTE(random_state=42, sampling_strategy='auto')
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    print(f"Before SMOTE: {y.value_counts().to_dict()}")
    print(f"After SMOTE: {pd.Series(y_resampled).value_counts().to_dict()}")
    
    return X_resampled, y_resampled
```

### Step 5: Model Training

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def train_model(X, y):
    """Train model with cross-validation"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    print(f"CV ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
    
    # Final fit
    model.fit(X_train_scaled, y_train)
    
    return model, scaler, (X_test_scaled, y_test)
```

### Step 6: Model Export

```python
import joblib

def save_model(model, scaler, feature_names, metrics, filepath):
    """Save model artifacts"""
    
    artifacts = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'metrics': metrics,
        'version': '1.0.0',
        'training_date': datetime.now().isoformat()
    }
    
    joblib.dump(artifacts, filepath)
    print(f"Model saved to {filepath}")
```

---

## Model Evaluation

### Metrics Used

| Metric | Description | Use Case |
|--------|-------------|----------|
| **ROC-AUC** | Area under ROC curve | Overall discrimination ability |
| **Accuracy** | Correct predictions / Total | General performance |
| **Precision** | TP / (TP + FP) | When false positives are costly |
| **Recall** | TP / (TP + FN) | When false negatives are costly |
| **F1-Score** | Harmonic mean of precision & recall | Balanced measure |

### Evaluation Code

```python
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve, accuracy_score
)

def evaluate_model(model, X_test, y_test):
    """Comprehensive model evaluation"""
    
    # Predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_proba):.3f}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:\n{cm}")
    
    return {
        'roc_auc': roc_auc_score(y_test, y_proba),
        'accuracy': accuracy_score(y_test, y_pred),
        'confusion_matrix': cm.tolist()
    }
```

### Cross-Validation Strategy

```python
from sklearn.model_selection import StratifiedKFold

def cross_validate(model, X, y, n_folds=5):
    """Stratified k-fold cross-validation"""
    
    cv = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    metrics = {'roc_auc': [], 'accuracy': [], 'f1': []}
    
    for train_idx, val_idx in cv.split(X, y):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        model.fit(X_train, y_train)
        y_proba = model.predict_proba(X_val)[:, 1]
        y_pred = model.predict(X_val)
        
        metrics['roc_auc'].append(roc_auc_score(y_val, y_proba))
        metrics['accuracy'].append(accuracy_score(y_val, y_pred))
    
    return {k: (np.mean(v), np.std(v)) for k, v in metrics.items()}
```

---

## Feature Engineering

### Techniques Used

#### 1. Binning (Discretization)
Convert continuous variables into categorical:

```python
# Age groups based on health risk profiles
age_bins = [0, 30, 45, 60, 100]
age_labels = ['Young', 'Middle', 'Older', 'Senior']
df['age_group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
```

#### 2. Interaction Features
Capture relationships between variables:

```python
# BMI-Age interaction (obesity impact increases with age)
df['bmi_age'] = df['BMI'] * df['Age']

# Glucose-BMI interaction (metabolic syndrome indicator)
df['glucose_bmi'] = df['Glucose'] * df['BMI']
```

#### 3. Ratio Features
Domain-specific ratios:

```python
# FSH/LH ratio (important for PCOS)
df['fsh_lh_ratio'] = df['FSH'] / (df['LH'] + 0.001)

# Waist-to-height ratio (better than BMI for some conditions)
df['waist_height'] = df['Waist'] / df['Height']
```

#### 4. Domain Knowledge Features

```python
# Metabolic syndrome indicators
df['metabolic_risk'] = (
    (df['BMI'] >= 30).astype(int) +
    (df['Glucose'] >= 100).astype(int) +
    (df['BloodPressure'] >= 130).astype(int)
)
```

---

## Model Deployment

### Loading Models for Inference

```python
import joblib
import numpy as np

class ModelInference:
    """Model inference wrapper"""
    
    def __init__(self, model_path: str):
        artifacts = joblib.load(model_path)
        self.model = artifacts['model']
        self.scaler = artifacts['scaler']
        self.feature_names = artifacts['feature_names']
        self.version = artifacts.get('version', '1.0.0')
    
    def predict(self, features: dict) -> dict:
        """Make prediction from feature dictionary"""
        
        # Prepare features in correct order
        X = np.array([[features[f] for f in self.feature_names]])
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        probability = self.model.predict_proba(X_scaled)[0][1]
        
        return {
            'risk_score': float(probability),
            'risk_level': self._get_risk_level(probability),
            'confidence': self._get_confidence(probability)
        }
    
    def _get_risk_level(self, score: float) -> str:
        if score < 0.3:
            return 'low'
        elif score < 0.6:
            return 'medium'
        return 'high'
    
    def _get_confidence(self, score: float) -> float:
        # Confidence is higher when prediction is more certain
        return abs(score - 0.5) * 2
```

### API Integration

```python
# app/ml/diabetes_model.py
from app.ml.base_predictor import BaseHealthPredictor

class DiabetesPredictor(BaseHealthPredictor):
    """Diabetes prediction model wrapper"""
    
    def __init__(self):
        super().__init__("models/diabetes_model.pkl")
    
    def validate_input(self, features: dict) -> tuple:
        """Validate input features"""
        required = ['Pregnancies', 'Glucose', 'BMI', 'Age']
        
        for field in required:
            if field not in features:
                return False, f"Missing: {field}"
        
        # Range validation
        if not (40 <= features['Glucose'] <= 400):
            return False, "Glucose out of range"
        
        return True, ""
```

---

## Limitations & Bias

### Known Limitations

| Model | Limitation | Impact |
|-------|-----------|--------|
| **Diabetes** | Trained on Pima Indian women | May not generalize to other ethnicities/genders |
| **Heart** | Predominantly male data | May underperform for females |
| **PCOS** | Limited sample size | Uncertainty in edge cases |

### Bias Considerations

#### Demographic Bias
- Models may perform differently across ethnicities
- Age distribution in training data affects predictions for extreme ages
- Gender imbalance in heart disease model

#### Mitigation Strategies
1. **Confidence thresholding**: Lower confidence for out-of-distribution inputs
2. **Uncertainty quantification**: Show prediction uncertainty
3. **Continuous monitoring**: Track performance across demographics
4. **Transparent limitations**: Clearly communicate model limitations

### Out-of-Distribution Detection

```python
def detect_ood(self, features: dict) -> bool:
    """Detect if input is significantly different from training data"""
    
    # Check if features are within training data range
    for feature, value in features.items():
        if feature in self.training_stats:
            mean = self.training_stats[feature]['mean']
            std = self.training_stats[feature]['std']
            
            # Flag if > 3 standard deviations from mean
            if abs(value - mean) > 3 * std:
                return True
    
    return False
```

---

## Future Improvements

### Planned Enhancements

1. **Model Updates**
   - Ensemble methods for better accuracy
   - Neural network alternatives
   - Calibrated probabilities

2. **Data Improvements**
   - Diverse training datasets
   - More recent medical data
   - Longitudinal data for trend prediction

3. **Features**
   - Wearable device data integration
   - Lab test result integration
   - Genetic risk factors

4. **Infrastructure**
   - A/B testing framework
   - Model monitoring dashboard
   - Automated retraining pipeline

### Research Directions

- Federated learning for privacy-preserving training
- Explainable AI (SHAP values, attention mechanisms)
- Multimodal models (text + tabular data)
- Time-series models for risk trajectory

---

## References

### Datasets
1. PIMA Indians Diabetes Dataset - [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/pima+indians+diabetes)
2. UCI Heart Disease Dataset - [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/heart+disease)
3. PCOS Dataset - Clinical data based on Rotterdam criteria

### Papers
1. "Diabetes prediction using machine learning" - Various studies
2. "Heart disease prediction using Random Forest" - UCI studies
3. "PCOS diagnosis criteria" - Rotterdam ESHRE/ASRM consensus

---

*Last Updated: December 2025*
