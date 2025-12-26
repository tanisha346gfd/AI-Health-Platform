"""
Train Heart Disease Risk Prediction Model (UCI Dataset)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime


class HeartDiseaseModelTrainer:
    """Complete training pipeline for heart disease risk prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.training_stats = {}
        
    def load_data(self, filepath='datasets/heart.csv'):
        """Load and preprocess UCI heart disease dataset"""
        print("📂 Loading UCI Heart Disease Dataset...")
        df = pd.read_csv(filepath)
        
        # Handle missing values (marked as NaN)
        df = df.replace('NaN', np.nan)
        
        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing values with median
        df = df.fillna(df.median())
        
        # Convert target to binary (0 = no disease, 1 = disease)
        df['target'] = (df['target'] > 0).astype(int)
        
        print(f"✅ Loaded {len(df)} samples")
        print(f"   Class distribution: {df['target'].value_counts().to_dict()}")
        
        return df
    
    def prepare_data(self, df):
        """Split features and target"""
        # Feature names with descriptions
        feature_descriptions = {
            'age': 'Age in years',
            'sex': 'Sex (1=male, 0=female)',
            'cp': 'Chest pain type (0-3)',
            'trestbps': 'Resting blood pressure',
            'chol': 'Serum cholesterol',
            'fbs': 'Fasting blood sugar > 120 mg/dl',
            'restecg': 'Resting ECG results',
            'thalach': 'Maximum heart rate achieved',
            'exang': 'Exercise induced angina',
            'oldpeak': 'ST depression',
            'slope': 'Slope of peak exercise ST',
            'ca': 'Number of major vessels (0-3)',
            'thal': 'Thalassemia (1=normal, 2=fixed defect, 3=reversible)'
        }
        
        X = df.drop('target', axis=1)
        y = df['target']
        
        self.feature_names = X.columns.tolist()
        self.training_stats = {
            col: {
                'mean': X[col].mean(), 
                'std': X[col].std(),
                'description': feature_descriptions.get(col, '')
            }
            for col in X.columns
        }
        
        return X, y
    
    def train(self, X, y):
        """Train Random Forest classifier"""
        print("🎯 Training Random Forest model...")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Hyperparameter tuning
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 15],
            'min_samples_split': [2, 5]
        }
        
        rf = RandomForestClassifier(random_state=42, class_weight='balanced')
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train_scaled, y_train)
        self.model = grid_search.best_estimator_
        
        print(f"✅ Best parameters: {grid_search.best_params_}")
        
        return X_test_scaled, y_test
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        print("\n📊 Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        print(classification_report(y_test, y_pred, target_names=['No Disease', 'Disease']))
        
        cm = confusion_matrix(y_test, y_pred)
        print("\n" + "="*60)
        print("CONFUSION MATRIX")
        print("="*60)
        print(cm)
        
        roc_auc = roc_auc_score(y_test, y_proba)
        print(f"\n🎯 ROC-AUC Score: {roc_auc:.4f}")
        
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n" + "="*60)
        print("TOP 10 IMPORTANT FEATURES")
        print("="*60)
        print(feature_importance.head(10).to_string(index=False))
        
        return {
            'y_test': y_test,
            'y_pred': y_pred,
            'y_proba': y_proba,
            'confusion_matrix': cm,
            'roc_auc': roc_auc,
            'feature_importance': feature_importance
        }
    
    def save_visualizations(self, results):
        """Generate evaluation plots"""
        print("\n📈 Generating visualizations...")
        os.makedirs('reports', exist_ok=True)
        
        # Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            results['confusion_matrix'], 
            annot=True, 
            fmt='d', 
            cmap='Reds',
            xticklabels=['No Disease', 'Disease'],
            yticklabels=['No Disease', 'Disease']
        )
        plt.title('Confusion Matrix - Heart Disease Prediction')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('reports/heart_confusion_matrix.png', dpi=300)
        plt.close()
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(results['y_test'], results['y_proba'])
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f"ROC-AUC = {results['roc_auc']:.4f}", linewidth=2, color='red')
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve - Heart Disease Prediction')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('reports/heart_roc_curve.png', dpi=300)
        plt.close()
        
        # Feature Importance
        top_features = results['feature_importance'].head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(top_features['feature'], top_features['importance'], color='crimson')
        plt.xlabel('Importance')
        plt.title('Top 10 Feature Importance - Heart Disease Prediction')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('reports/heart_feature_importance.png', dpi=300)
        plt.close()
        
        print("✅ Visualizations saved to reports/")
    
    def save_model(self):
        """Save model artifacts"""
        print("\n💾 Saving model...")
        os.makedirs('../models', exist_ok=True)
        
        model_artifacts = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'training_stats': self.training_stats,
            'version': '1.0.0',
            'trained_at': datetime.now().isoformat(),
            'dataset': 'UCI Heart Disease'
        }
        
        joblib.dump(model_artifacts, '../models/heart_model.pkl')
        print("✅ Model saved to models/heart_model.pkl")


def main():
    print("❤️  HEART DISEASE RISK PREDICTION MODEL TRAINING")
    print("="*60)
    
    trainer = HeartDiseaseModelTrainer()
    df = trainer.load_data()
    X, y = trainer.prepare_data(df)
    X_test, y_test = trainer.train(X, y)
    results = trainer.evaluate(X_test, y_test)
    trainer.save_visualizations(results)
    trainer.save_model()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
