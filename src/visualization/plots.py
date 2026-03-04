"""
Visualization utility functions.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


def setup_plotting(style='whitegrid', palette='husl'):
    """
    Setup plotting style.
    
    Args:
        style: Seaborn style
        palette: Color palette
    """
    plt.style.use(f'seaborn-v0_8-{style}')
    sns.set_palette(palette)
    sns.set_context('notebook')


def save_figure(fig, filename, results_dir, dpi=150):
    """
    Save figure to results directory.
    
    Args:
        fig: Matplotlib figure
        filename: Output filename
        results_dir: Results directory path
        dpi: Resolution
    """
    os.makedirs(results_dir, exist_ok=True)
    filepath = os.path.join(results_dir, 'figures', filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Saved: {filepath}")


def plot_distribution(df, column, bins=30, figsize=(10, 6)):
    """
    Plot distribution of a column.
    
    Args:
        df: DataFrame
        column: Column name
        bins: Number of bins
        figsize: Figure size
    
    Returns:
        Figure and axes
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram
    axes[0].hist(df[column].dropna(), bins=bins, edgecolor='black', alpha=0.7)
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'{column} Distribution')
    axes[0].axvline(df[column].mean(), color='red', linestyle='--', label='Mean')
    axes[0].axvline(df[column].median(), color='green', linestyle='--', label='Median')
    axes[0].legend()
    
    # Boxplot
    axes[1].boxplot(df[column].dropna())
    axes[1].set_ylabel(column)
    axes[1].set_title(f'{column} Boxplot')
    
    plt.tight_layout()
    return fig, axes


def plot_categorical(df, column, top_n=10, figsize=(10, 6)):
    """
    Plot top N categories.
    
    Args:
        df: DataFrame
        column: Column name
        top_n: Number of top categories
        figsize: Figure size
    
    Returns:
        Figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    top_cats = df[column].value_counts().head(top_n)
    sns.barplot(x=top_cats.values, y=top_cats.index, ax=ax, palette='viridis')
    
    ax.set_xlabel('Count')
    ax.set_ylabel(column)
    ax.set_title(f'Top {top_n} {column}')
    
    plt.tight_layout()
    return fig, ax


def plot_salary_by_category(df, category_col, salary_col, top_n=15, figsize=(12, 6)):
    """
    Plot median salary by category.
    
    Args:
        df: DataFrame
        category_col: Category column name
        salary_col: Salary column name
        top_n: Number of top categories
        figsize: Figure size
    
    Returns:
        Figure and axes
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    salary_by_cat = df.groupby(category_col)[salary_col].median().sort_values(ascending=False).head(top_n)
    sns.barplot(x=salary_by_cat.values, y=salary_by_cat.index, ax=ax, palette='coolwarm')
    
    ax.set_xlabel('Median Salary (INR)')
    ax.set_ylabel(category_col)
    ax.set_title(f'Median Salary by {category_col}')
    
    plt.tight_layout()
    return fig, ax


def plot_correlation_heatmap(df, numeric_cols=None, figsize=(10, 8)):
    """
    Plot correlation heatmap.
    
    Args:
        df: DataFrame
        numeric_cols: List of numeric columns (None = all numeric)
        figsize: Figure size
    
    Returns:
        Figure and axes
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                fmt='.2f', ax=ax, square=True)
    ax.set_title('Correlation Heatmap')
    
    plt.tight_layout()
    return fig, ax
