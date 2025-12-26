"""
Download real medical datasets for training
"""
import pandas as pd
import requests
import os

def download_pima_diabetes():
    """Download PIMA Indians Diabetes Dataset"""
    print("📥 Downloading PIMA Indians Diabetes Dataset...")
    
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Column names for PIMA dataset
        columns = [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
        ]
        
        # Save to CSV
        with open('diabetes.csv', 'w') as f:
            f.write(','.join(columns) + '\n')
            f.write(response.text)
        
        # Verify
        df = pd.read_csv('diabetes.csv')
        print(f"✅ PIMA dataset downloaded: {len(df)} samples, {len(df.columns)} features")
        print(f"   Positive cases: {df['Outcome'].sum()} ({df['Outcome'].sum()/len(df)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error downloading PIMA dataset: {e}")


def download_heart_disease():
    """Download UCI Heart Disease Dataset"""
    print("\n📥 Downloading UCI Heart Disease Dataset...")
    
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Column names for UCI Heart Disease
        columns = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
        ]
        
        # Save and clean
        lines = response.text.strip().split('\n')
        clean_lines = []
        
        for line in lines:
            # Replace '?' with NaN
            clean_line = line.replace('?', 'NaN')
            clean_lines.append(clean_line)
        
        with open('heart.csv', 'w') as f:
            f.write(','.join(columns) + '\n')
            for line in clean_lines:
                f.write(line + '\n')
        
        # Verify
        df = pd.read_csv('heart.csv')
        print(f"✅ Heart disease dataset downloaded: {len(df)} samples, {len(df.columns)} features")
        print(f"   Disease cases: {(df['target'] > 0).sum()} ({(df['target'] > 0).sum()/len(df)*100:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error downloading heart disease dataset: {e}")


def create_synthetic_health_data():
    """Create a small synthetic dataset for testing (not for training)"""
    print("\n📝 Creating synthetic test data...")
    
    test_data = {
        'diabetes_test': {
            'Pregnancies': 2,
            'Glucose': 148,
            'BloodPressure': 72,
            'SkinThickness': 35,
            'Insulin': 0,
            'BMI': 33.6,
            'DiabetesPedigreeFunction': 0.627,
            'Age': 50
        },
        'heart_test': {
            'age': 63,
            'sex': 1,
            'cp': 3,
            'trestbps': 145,
            'chol': 233,
            'fbs': 1,
            'restecg': 0,
            'thalach': 150,
            'exang': 0,
            'oldpeak': 2.3,
            'slope': 0,
            'ca': 0,
            'thal': 1
        }
    }
    
    import json
    with open('test_samples.json', 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print("✅ Test samples created")


if __name__ == "__main__":
    print("🏥 AI Health Platform - Dataset Downloader\n")
    print("=" * 60)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Download datasets (saves to current directory)
    download_pima_diabetes()
    download_heart_disease()
    create_synthetic_health_data()
    
    print("\n" + "=" * 60)
    print("✅ All datasets downloaded successfully!")
    print("\nNext steps:")
    print("1. Run: python train_diabetes.py")
    print("2. Run: python train_heart.py")
    print("3. Check the 'reports/' folder for evaluation results")
