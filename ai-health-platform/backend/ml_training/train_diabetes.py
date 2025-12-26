"""
Train Diabetes Risk Prediction Model (PIMA Indians Dataset)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, precision_recall_curve
)
from imblearn.over_sampling import SMOTE
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime


class DiabetesModelTrainer:
    """Complete training pipeline for diabetes risk prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.training_stats = {}
        
    def load_data(self, filepath='datasets/diabetes.csv'):
        """Load and preprocess PIMA diabetes dataset"""
        print("📂 Loading PIMA Indians Diabetes Dataset...")
        df = pd.read_csv(filepath)
        
        # Handle zeros (medical impossibility)
        # In this dataset, 0 means missing value
        zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        
        for col in zero_cols:
            df[col] = df[col].replace(0, np.nan)
            df[col].fillna(df[col].median(), inplace=True)
        
        print(f"✅ Loaded {len(df)} samples")
        print(f"   Class distribution: {df['Outcome'].value_counts().to_dict()}")
        
        return df
    
    def engineer_features(self, df):
        """Create additional features"""
        print("🔧 Engineering features...")
        
        # Age groups (as numeric, not categorical)
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 30, 45, 60, 100], labels=[0, 1, 2, 3]).astype(float)
        
        # BMI categories (as numeric)
        df['BMI_Category'] = pd.cut(
            df['BMI'], 
            bins=[0, 18.5, 25, 30, 100], 
            labels=[0, 1, 2, 3]
        ).astype(float)
        
        # Glucose categories (as numeric)
        df['Glucose_Category'] = pd.cut(
            df['Glucose'],
            bins=[0, 100, 125, 200],
            labels=[0, 1, 2]
        ).astype(float)
        
        # Interaction features
        df['BMI_Age'] = df['BMI'] * df['Age']
        df['Glucose_BMI'] = df['Glucose'] * df['BMI']
        
        return df
    
    def prepare_data(self, df):
        """Split features and target"""
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']
        
        # Store feature names and stats for validation
        self.feature_names = X.columns.tolist()
        self.training_stats = {
            col: {'mean': X[col].mean(), 'std': X[col].std()}
            for col in X.columns
        }
        
        return X, y
    
    def train(self, X, y):
        """Train Random Forest with hyperparameter tuning"""
        print("🎯 Training Random Forest model...")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Handle class imbalance with SMOTE
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
        
        print(f"   After SMOTE: {len(X_train_balanced)} samples")
        
        # Hyperparameter tuning
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 15, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        
        rf = RandomForestClassifier(random_state=42, class_weight='balanced')
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train_balanced, y_train_balanced)
        
        self.model = grid_search.best_estimator_
        print(f"✅ Best parameters: {grid_search.best_params_}")
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.model, X_train_balanced, y_train_balanced, cv=5, scoring='roc_auc'
        )
        print(f"   Cross-validation ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return X_test_scaled, y_test
    
    def evaluate(self, X_test, y_test):
        """Comprehensive model evaluation"""
        print("\n📊 Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Metrics
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        print(classification_report(y_test, y_pred, target_names=['No Diabetes', 'Diabetes']))
        
        print("\n" + "="*60)
        print("CONFUSION MATRIX")
        print("="*60)
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        roc_auc = roc_auc_score(y_test, y_proba)
        print(f"\n🎯 ROC-AUC Score: {roc_auc:.4f}")
        
        # Feature importance
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
        """Generate and save evaluation plots"""
        print("\n📈 Generating visualizations...")
        
        os.makedirs('reports', exist_ok=True)
        
        # 1. Confusion Matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            results['confusion_matrix'], 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=['No Diabetes', 'Diabetes'],
            yticklabels=['No Diabetes', 'Diabetes']
        )
        plt.title('Confusion Matrix - Diabetes Prediction')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('reports/diabetes_confusion_matrix.png', dpi=300)
        plt.close()
        
        # 2. ROC Curve
        fpr, tpr, _ = roc_curve(results['y_test'], results['y_proba'])
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f"ROC-AUC = {results['roc_auc']:.4f}", linewidth=2)
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve - Diabetes Prediction')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('reports/diabetes_roc_curve.png', dpi=300)
        plt.close()
        
        # 3. Feature Importance
        top_features = results['feature_importance'].head(10)
        plt.figure(figsize=(10, 6))
        plt.barh(top_features['feature'], top_features['importance'])
        plt.xlabel('Importance')
        plt.title('Top 10 Feature Importance - Diabetes Prediction')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('reports/diabetes_feature_importance.png', dpi=300)
        plt.close()
        
        print("✅ Visualizations saved to reports/")
    
    def save_model(self):
        """Save model, scaler, and metadata"""
        print("\n💾 Saving model...")
        
        os.makedirs('../models', exist_ok=True)
        
        model_artifacts = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'training_stats': self.training_stats,
            'version': '1.0.0',
            'trained_at': datetime.now().isoformat(),
            'dataset': 'PIMA Indians Diabetes'
        }
        
        joblib.dump(model_artifacts, '../models/diabetes_model.pkl')
        print("✅ Model saved to models/diabetes_model.pkl")


def main():
    print("🏥 DIABETES RISK PREDICTION MODEL TRAINING")
    print("="*60)
    
    trainer = DiabetesModelTrainer()
    
    # Load data
    df = trainer.load_data()
    
    # Engineer features
    df = trainer.engineer_features(df)
    
    # Prepare data
    X, y = trainer.prepare_data(df)
    
    # Train
    X_test, y_test = trainer.train(X, y)
    
    # Evaluate
    results = trainer.evaluate(X_test, y_test)
    
    # Save visualizations
    trainer.save_visualizations(results)
    
    # Save model
    trainer.save_model()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check reports/ for evaluation results")
    print("2. Run: python train_heart.py")
    print("3. Test model in your application")


if __name__ == "__main__":
    main()
