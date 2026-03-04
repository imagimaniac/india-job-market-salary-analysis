#!/usr/bin/env python3
"""
Script to download India Job Market & Salary Dataset from Kaggle.
"""

import os
import subprocess
import sys

def install_kaggle():
    """Install kaggle package if not already installed."""
    try:
        import kaggle
        return True
    except ImportError:
        print("Installing kaggle package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        return True

def download_dataset():
    """Download the dataset from Kaggle."""
    print("=" * 60)
    print("India Job Market & Salary Dataset Downloader")
    print("=" * 60)
    
    # Check for Kaggle credentials
    kaggle_json = os.path.expanduser("~/.kaggle/kaggle.json")
    
    if not os.path.exists(kaggle_json):
        print("\n⚠️  Kaggle credentials not found!")
        print("\nTo download the dataset:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Click 'Create New API Token'")
        print("3. Move kaggle.json to ~/.kaggle/kaggle.json")
        print("\nAlternatively, manually download from:")
        print("https://www.kaggle.com/datasets/kapoorprakhar/india-job-market-and-salary-dataset")
        print("\nAnd place the file in: data/raw/")
        return False
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        print("\n✅ Kaggle authenticated successfully!")
        print("\nDownloading dataset...")
        
        # Create data directory
        data_dir = os.path.join(os.path.dirname(__file__), 'data', 'raw')
        os.makedirs(data_dir, exist_ok=True)
        
        # Download dataset
        api.dataset_download_files(
            'kapoorprakhar/india-job-market-and-salary-dataset',
            path=data_dir,
            unzip=True
        )
        
        print(f"\n✅ Dataset downloaded to: {data_dir}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    install_kaggle()
    download_dataset()
