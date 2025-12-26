"""
PCOS Prediction Model Training
Uses real clinical data with proper ML pipeline and evaluation
"""
import pandas as pd
import numpy as np
import os
import sys
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns


class PCOSModelTrainer:
    """
    PCOS Prediction Model Trainer with proper ML pipeline
    
    This trainer:
    1. Loads real PCOS clinical dataset
    2. Performs EDA and preprocessing
    3. Trains multiple models (LogReg, RF, GradientBoosting)
    4. Evaluates with proper metrics (Accuracy, Precision, Recall, ROC-AUC)
    5. Saves the best model for production use
    """
    
    def __init__(self, dataset_path: str = None):
        self.dataset_path = dataset_path or os.path.join(
            os.path.dirname(__file__), 'datasets', 'pcos.csv'
        )
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.best_model_name = None
        self.metrics = {}
        
        # Key features for PCOS prediction based on clinical criteria
        self.important_features = [
            'Age', 'BMI', 'Weight', 'Cycle_length', 'Cycle_RI',
            'Weight_gain', 'Hair_growth', 'Skin_darkening', 'Pimples',
            'Fast_food', 'Regular_Exercise', 'Follicle_L', 'Follicle_R',
            'AMH', 'LH', 'FSH', 'FSH_LH', 'Waist_Hip_Ratio'
        ]
    
    def load_data(self):
        """Load and validate the PCOS dataset"""
        print("\n" + "="*60)
        print("📊 PCOS MODEL TRAINING PIPELINE")
        print("="*60)
        
        if not os.path.exists(self.dataset_path):
            print("⚠️ Dataset not found. Downloading...")
            from datasets.download_pcos import download_pcos_dataset
            download_pcos_dataset()
        
        self.df = pd.read_csv(self.dataset_path)
        print(f"\n✅ Loaded dataset: {len(self.df)} samples, {len(self.df.columns)} features")
        
        # Identify target column
        target_candidates = ['PCOS', 'PCOS (Y/N)', 'Target', 'target', 'pcos']
        self.target_col = None
        for col in target_candidates:
            if col in self.df.columns:
                self.target_col = col
                break
        
        if self.target_col is None:
            # Use last column as target
            self.target_col = self.df.columns[-1]
        
        print(f"   Target column: {self.target_col}")
        return self
    
    def eda(self):
        """Exploratory Data Analysis"""
        print("\n" + "-"*60)
        print("📈 EXPLORATORY DATA ANALYSIS")
        print("-"*60)
        
        # Dataset info
        print(f"\n📋 Dataset Shape: {self.df.shape}")
        print(f"\n📋 Target Distribution:")
        target_counts = self.df[self.target_col].value_counts()
        for val, count in target_counts.items():
            print(f"   {val}: {count} ({count/len(self.df)*100:.1f}%)")
        
        # Missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(f"\n⚠️ Missing Values:")
            for col, count in missing[missing > 0].items():
                print(f"   {col}: {count}")
        else:
            print(f"\n✅ No missing values")
        
        # Feature statistics
        print(f"\n📊 Numeric Features Summary:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:10]
        for col in numeric_cols:
            if col != self.target_col:
                print(f"   {col}: mean={self.df[col].mean():.2f}, std={self.df[col].std():.2f}")
        
        return self
    
    def preprocess(self):
        """Data preprocessing and feature engineering"""
        print("\n" + "-"*60)
        print("🔧 DATA PREPROCESSING")
        print("-"*60)
        
        df = self.df.copy()
        
        # Handle target variable
        if df[self.target_col].dtype == 'object':
            le = LabelEncoder()
            df[self.target_col] = le.fit_transform(df[self.target_col])
        
        # Remove non-informative columns
        drop_cols = ['Sl. No', 'Patient File No.', 'Unnamed: 0', 'Unnamed: 44']
        df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')
        
        # Fill missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Select features (use available important features)
        available_features = [f for f in self.important_features if f in df.columns]
        
        if len(available_features) < 5:
            # Use all numeric features except target
            available_features = [c for c in numeric_cols if c != self.target_col]
        
        self.feature_names = available_features
        print(f"   Using {len(available_features)} features: {available_features[:8]}...")
        
        # Prepare X and y
        self.X = df[available_features].values
        self.y = df[self.target_col].values
        
        # Handle class imbalance check
        class_ratio = self.y.sum() / len(self.y)
        print(f"   Class balance: {class_ratio*100:.1f}% positive")
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Apply SMOTE if imbalanced
        if class_ratio < 0.3 or class_ratio > 0.7:
            print("   Applying SMOTE for class balancing...")
            smote = SMOTE(random_state=42)
            self.X_train_scaled, self.y_train = smote.fit_resample(self.X_train_scaled, self.y_train)
            print(f"   After SMOTE: {len(self.y_train)} samples")
        
        print(f"   ✅ Training set: {len(self.y_train)} samples")
        print(f"   ✅ Test set: {len(self.y_test)} samples")
        
        return self
    
    def train_models(self):
        """Train multiple models and select the best"""
        print("\n" + "-"*60)
        print("🤖 MODEL TRAINING")
        print("-"*60)
        
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\n   Training {name}...")
            
            # Cross-validation
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
            cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, cv=cv, scoring='roc_auc')
            
            # Train on full training set
            model.fit(self.X_train_scaled, self.y_train)
            
            # Predict on test set
            y_pred = model.predict(self.X_test_scaled)
            y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            
            # Calculate metrics
            metrics = {
                'cv_roc_auc': cv_scores.mean(),
                'cv_roc_auc_std': cv_scores.std(),
                'accuracy': accuracy_score(self.y_test, y_pred),
                'precision': precision_score(self.y_test, y_pred),
                'recall': recall_score(self.y_test, y_pred),
                'f1': f1_score(self.y_test, y_pred),
                'roc_auc': roc_auc_score(self.y_test, y_pred_proba)
            }
            
            results[name] = {'model': model, 'metrics': metrics}
            
            print(f"      CV ROC-AUC: {metrics['cv_roc_auc']:.4f} (+/- {metrics['cv_roc_auc_std']:.4f})")
            print(f"      Test Accuracy: {metrics['accuracy']:.4f}")
            print(f"      Test ROC-AUC: {metrics['roc_auc']:.4f}")
        
        # Select best model by ROC-AUC
        best_name = max(results.keys(), key=lambda k: results[k]['metrics']['roc_auc'])
        self.model = results[best_name]['model']
        self.metrics = results[best_name]['metrics']
        self.best_model_name = best_name
        
        print(f"\n   🏆 Best Model: {best_name}")
        
        return self
    
    def evaluate(self):
        """Detailed evaluation of the best model"""
        print("\n" + "-"*60)
        print("📊 MODEL EVALUATION")
        print("-"*60)
        
        y_pred = self.model.predict(self.X_test_scaled)
        y_pred_proba = self.model.predict_proba(self.X_test_scaled)[:, 1]
        
        print(f"\n🎯 {self.best_model_name} Performance:")
        print(f"   Accuracy:  {self.metrics['accuracy']*100:.2f}%")
        print(f"   Precision: {self.metrics['precision']*100:.2f}%")
        print(f"   Recall:    {self.metrics['recall']*100:.2f}%")
        print(f"   F1-Score:  {self.metrics['f1']*100:.2f}%")
        print(f"   ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        
        print("\n📋 Classification Report:")
        print(classification_report(self.y_test, y_pred, target_names=['No PCOS', 'PCOS']))
        
        print("\n📊 Confusion Matrix:")
        cm = confusion_matrix(self.y_test, y_pred)
        print(f"   TN: {cm[0,0]}, FP: {cm[0,1]}")
        print(f"   FN: {cm[1,0]}, TP: {cm[1,1]}")
        
        # Feature importance (for tree-based models)
        if hasattr(self.model, 'feature_importances_'):
            print("\n📊 Top 10 Feature Importances:")
            importances = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            for _, row in importances.head(10).iterrows():
                print(f"   {row['feature']}: {row['importance']:.4f}")
        
        return self
    
    def save_model(self):
        """Save the trained model and scaler"""
        print("\n" + "-"*60)
        print("💾 SAVING MODEL")
        print("-"*60)
        
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, 'pcos_model.pkl')
        
        model_package = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_name': self.best_model_name,
            'metrics': self.metrics,
            'version': '1.0.0'
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_package, f)
        
        print(f"   ✅ Model saved to: {model_path}")
        print(f"   📊 Model: {self.best_model_name}")
        print(f"   📊 ROC-AUC: {self.metrics['roc_auc']:.4f}")
        print(f"   📊 Features: {len(self.feature_names)}")
        
        return model_path
    
    def generate_report(self):
        """Generate training report with visualizations"""
        print("\n" + "-"*60)
        print("📈 GENERATING REPORT")
        print("-"*60)
        
        reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. Confusion Matrix
        y_pred = self.model.predict(self.X_test_scaled)
        cm = confusion_matrix(self.y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0,0])
        axes[0,0].set_title('Confusion Matrix')
        axes[0,0].set_ylabel('Actual')
        axes[0,0].set_xlabel('Predicted')
        
        # 2. ROC Curve
        from sklearn.metrics import roc_curve
        y_pred_proba = self.model.predict_proba(self.X_test_scaled)[:, 1]
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        axes[0,1].plot(fpr, tpr, 'b-', label=f'ROC (AUC = {self.metrics["roc_auc"]:.3f})')
        axes[0,1].plot([0, 1], [0, 1], 'k--')
        axes[0,1].set_xlabel('False Positive Rate')
        axes[0,1].set_ylabel('True Positive Rate')
        axes[0,1].set_title('ROC Curve')
        axes[0,1].legend()
        
        # 3. Feature Importance
        if hasattr(self.model, 'feature_importances_'):
            importances = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=True).tail(10)
            
            axes[1,0].barh(importances['feature'], importances['importance'])
            axes[1,0].set_title('Top 10 Feature Importances')
        
        # 4. Metrics Summary
        metrics_text = f"""
PCOS PREDICTION MODEL
=====================
Model: {self.best_model_name}

Performance Metrics:
- Accuracy:  {self.metrics['accuracy']*100:.1f}%
- Precision: {self.metrics['precision']*100:.1f}%
- Recall:    {self.metrics['recall']*100:.1f}%
- F1-Score:  {self.metrics['f1']*100:.1f}%
- ROC-AUC:   {self.metrics['roc_auc']:.4f}

Training Info:
- Features: {len(self.feature_names)}
- Test Samples: {len(self.y_test)}
        """
        axes[1,1].text(0.1, 0.5, metrics_text, fontfamily='monospace', fontsize=10, verticalalignment='center')
        axes[1,1].axis('off')
        
        plt.tight_layout()
        report_path = os.path.join(reports_dir, 'pcos_model_report.png')
        plt.savefig(report_path, dpi=150)
        plt.close()
        
        print(f"   ✅ Report saved to: {report_path}")
        
        return self


def main():
    """Main training pipeline"""
    trainer = PCOSModelTrainer()
    
    trainer.load_data()
    trainer.eda()
    trainer.preprocess()
    trainer.train_models()
    trainer.evaluate()
    trainer.save_model()
    trainer.generate_report()
    
    print("\n" + "="*60)
    print("✅ PCOS MODEL TRAINING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
