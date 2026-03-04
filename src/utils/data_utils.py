"""
Utility functions for data loading and preprocessing.
"""

import pandas as pd
import numpy as np
import os


def load_data(file_path, **kwargs):
    """
    Load data from CSV or Excel file.
    
    Args:
        file_path: Path to the data file
        **kwargs: Additional arguments for pandas read function
    
    Returns:
        DataFrame
    """
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path, **kwargs)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def get_column_info(df):
    """
    Get detailed information about columns.
    
    Args:
        df: DataFrame
    
    Returns:
        DataFrame with column information
    """
    info = pd.DataFrame({
        'column': df.columns,
        'dtype': df.dtypes.values,
        'nunique': df.nunique().values,
        'null_count': df.isnull().sum().values,
        'null_pct': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    return info


def clean_salary_column(df, salary_col):
    """
    Clean salary column - handle currency symbols, commas, etc.
    
    Args:
        df: DataFrame
        salary_col: Name of salary column
    
    Returns:
        DataFrame with cleaned salary column
    """
    df = df.copy()
    if df[salary_col].dtype == 'object':
        df[salary_col] = df[salary_col].str.replace(r'[₹,Rs.]', '', regex=True)
        df[salary_col] = pd.to_numeric(df[salary_col], errors='coerce')
    return df


def handle_missing_values(df, strategy='drop', fill_value=None, columns=None):
    """
    Handle missing values in DataFrame.
    
    Args:
        df: DataFrame
        strategy: 'drop', 'fill', or 'none'
        fill_value: Value to fill if strategy is 'fill'
        columns: Specific columns to process (None = all)
    
    Returns:
        DataFrame with handled missing values
    """
    df = df.copy()
    cols = columns if columns else df.columns
    
    if strategy == 'drop':
        df = df.dropna(subset=cols)
    elif strategy == 'fill':
        df[cols] = df[cols].fillna(fill_value)
    
    return df


def remove_outliers(df, column, method='iqr', threshold=1.5):
    """
    Remove outliers from a column.
    
    Args:
        df: DataFrame
        column: Column to check for outliers
        method: 'iqr' or 'zscore'
        threshold: Threshold for outlier detection
    
    Returns:
        DataFrame without outliers
    """
    df = df.copy()
    
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        df = df[z_scores < threshold]
    
    return df


def save_to_csv(df, file_path, **kwargs):
    """
    Save DataFrame to CSV.
    
    Args:
        df: DataFrame
        file_path: Output file path
        **kwargs: Additional arguments for to_csv
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False, **kwargs)
