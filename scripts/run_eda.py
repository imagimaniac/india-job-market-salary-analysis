#!/usr/bin/env python3
"""
Complete EDA and Visualization Script for India Job Market Salary Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import warnings
import json
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

# Paths
ROOT_DIR = '/Users/impro/Projects/india-job-market-salary-analysis'
DATA_DIR = os.path.join(ROOT_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(ROOT_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')

# Create directories
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(os.path.join(RESULTS_DIR, 'figures'), exist_ok=True)
os.makedirs(os.path.join(RESULTS_DIR, 'tables'), exist_ok=True)

print("="*60)
print("INDIA JOB MARKET SALARY ANALYSIS - EDA")
print("="*60)

# Load data
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
file_path = os.path.join(DATA_DIR, csv_files[0])
df = pd.read_csv(file_path)

print(f"\n✅ Dataset loaded: {csv_files[0]}")
print(f"   Shape: {df.shape[0]} rows, {df.shape[1]} columns")

# Parse salary - handle multiple formats
def parse_salary(salary_str):
    """Parse salary string and return annual salary in INR"""
    if pd.isna(salary_str) or salary_str == 'Not specified':
        return np.nan
    
    salary_str = str(salary_str)
    
    # Check if it's monthly or yearly
    is_monthly = 'month' in salary_str.lower()
    
    # Extract all numbers (remove ₹, commas, spaces)
    numbers = re.findall(r'[\d,]+\.?\d*', salary_str.replace('₹', '').replace(',', ''))
    numbers = [float(n.replace(',', '')) for n in numbers if n]
    
    if not numbers:
        return np.nan
    
    # Use average of range or single value
    avg_salary = sum(numbers) / len(numbers)
    
    # Convert to annual (monthly * 12)
    if is_monthly:
        avg_salary = avg_salary * 12
    
    return avg_salary

# Apply salary parsing
df['Annual_Salary'] = df['Salary'].apply(parse_salary)

# Also use Monthly Salary * 12 where Annual_Salary is NaN
df['Monthly_Salary_Annual'] = df['Monthly Salary'] * 12
df['Final_Salary'] = df['Annual_Salary'].fillna(df['Monthly_Salary_Annual'])

# Filter out NaN salaries
df_with_salary = df[df['Final_Salary'].notna()].copy()

print(f"   Jobs with valid salary: {len(df_with_salary)} / {len(df)}")

# Save cleaned data
df.to_csv(os.path.join(PROCESSED_DIR, 'cleaned_data.csv'), index=False)
df_with_salary.to_csv(os.path.join(PROCESSED_DIR, 'data_with_salary.csv'), index=False)
print("✅ Cleaned data saved")

# Column mapping for this dataset
COLUMN_MAPPING = {
    'salary': 'Final_Salary',
    'job_title': 'Job Title',
    'company': None,
    'location': 'Location',
    'experience': None,
    'state': 'State',
    'locality': 'Locality'
}

# Save mapping
with open(os.path.join(PROCESSED_DIR, 'column_mapping.json'), 'w') as f:
    json.dump(COLUMN_MAPPING, f, indent=2)

print("\n" + "="*60)
print("1. DATASET OVERVIEW")
print("="*60)

print("\n📊 Column Information:")
for col in df.columns:
    print(f"   {col}: {df[col].dtype} | unique: {df[col].nunique()}")

print("\n📈 Summary Statistics (Annual Salary):")
print(df_with_salary['Final_Salary'].describe())

print("\n❌ Missing Values:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "   No missing values")

# =============================================================================
# UNIVARIATE ANALYSIS
# =============================================================================
print("\n" + "="*60)
print("2. UNIVARIATE ANALYSIS - SALARY DISTRIBUTION")
print("="*60)

# Salary Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df_with_salary['Final_Salary'].dropna(), bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Annual Salary (INR)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Salary Distribution - Histogram')
axes[0].axvline(df_with_salary['Final_Salary'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: ₹{df_with_salary['Final_Salary'].mean():,.0f}")
axes[0].axvline(df_with_salary['Final_Salary'].median(), color='green', linestyle='--', linewidth=2, label=f"Median: ₹{df_with_salary['Final_Salary'].median():,.0f}")
axes[0].legend()

# Boxplot
bp = axes[1].boxplot(df_with_salary['Final_Salary'].dropna(), vert=True, patch_artist=True)
bp['boxes'][0].set_facecolor('steelblue')
axes[1].set_ylabel('Annual Salary (INR)')
axes[1].set_title('Salary Distribution - Boxplot')

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '01_salary_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 01_salary_distribution.png")

# Job Title Distribution
fig, ax = plt.subplots(figsize=(12, 8))
top_jobs = df['Job Title'].value_counts().head(15)
sns.barplot(x=top_jobs.values, y=top_jobs.index, palette='viridis', ax=ax)
ax.set_xlabel('Count')
ax.set_ylabel('Job Title')
ax.set_title('Top 15 Job Titles by Frequency')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '02_job_title_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 02_job_title_distribution.png")

# Location Distribution
fig, ax = plt.subplots(figsize=(12, 8))
top_locations = df['Location'].value_counts().head(15)
sns.barplot(x=top_locations.values, y=top_locations.index, palette='magma', ax=ax)
ax.set_xlabel('Count')
ax.set_ylabel('Location')
ax.set_title('Top 15 Locations by Job Count')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '03_location_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 03_location_distribution.png")

# State Distribution
fig, ax = plt.subplots(figsize=(12, 8))
top_states = df['State'].value_counts().head(15)
sns.barplot(x=top_states.values, y=top_states.index, palette='coolwarm', ax=ax)
ax.set_xlabel('Count')
ax.set_ylabel('State')
ax.set_title('Top 15 States by Job Count')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '04_state_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 04_state_distribution.png")

# =============================================================================
# BIVARIATE ANALYSIS
# =============================================================================
print("\n" + "="*60)
print("3. BIVARIATE ANALYSIS - SALARY BY CATEGORIES")
print("="*60)

# Salary by Job Title (Top 15)
fig, ax = plt.subplots(figsize=(12, 8))
salary_by_job = df_with_salary.groupby('Job Title')['Final_Salary'].median().sort_values(ascending=False).head(15)
sns.barplot(x=salary_by_job.values, y=salary_by_job.index, palette='coolwarm', ax=ax)
ax.set_xlabel('Median Annual Salary (INR)')
ax.set_ylabel('Job Title')
ax.set_title('Top 15 Highest Paying Job Titles (by Median Salary)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '05_salary_by_job_title.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 05_salary_by_job_title.png")

# Salary by Location (Top 15)
fig, ax = plt.subplots(figsize=(12, 8))
salary_by_location = df_with_salary.groupby('Location')['Final_Salary'].median().sort_values(ascending=False).head(15)
sns.barplot(x=salary_by_location.values, y=salary_by_location.index, palette='viridis', ax=ax)
ax.set_xlabel('Median Annual Salary (INR)')
ax.set_ylabel('Location')
ax.set_title('Top 15 Highest Paying Locations (by Median Salary)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '06_salary_by_location.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 06_salary_by_location.png")

# Salary by State (Top 15)
fig, ax = plt.subplots(figsize=(12, 8))
salary_by_state = df_with_salary.groupby('State')['Final_Salary'].median().sort_values(ascending=False).head(15)
sns.barplot(x=salary_by_state.values, y=salary_by_state.index, palette='magma', ax=ax)
ax.set_xlabel('Median Annual Salary (INR)')
ax.set_ylabel('State')
ax.set_title('Top 15 Highest Paying States (by Median Salary)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '07_salary_by_state.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 07_salary_by_state.png")

# Salary Distribution by Top Job Titles (Boxplot) - using only jobs with enough data
fig, ax = plt.subplots(figsize=(14, 8))
job_counts = df_with_salary['Job Title'].value_counts()
top_10_jobs = job_counts[job_counts >= 5].head(10).index.tolist()  # Jobs with 5+ entries
if top_10_jobs:
    df_top_jobs = df_with_salary[df_with_salary['Job Title'].isin(top_10_jobs)]
    order = df_top_jobs.groupby('Job Title')['Final_Salary'].median().sort_values(ascending=False).index
    sns.boxplot(data=df_top_jobs, x='Job Title', y='Final_Salary', order=order, palette='Set2', ax=ax)
    ax.set_xlabel('Job Title')
    ax.set_ylabel('Annual Salary (INR)')
    ax.set_title('Salary Distribution by Top 10 Job Titles (5+ entries)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'figures', '08_salary_boxplot_by_job.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 08_salary_boxplot_by_job.png")
else:
    print("⚠️  Skipped: 08_salary_boxplot_by_job.png (insufficient data)")

# Salary Distribution by Top Locations (Boxplot)
fig, ax = plt.subplots(figsize=(14, 8))
loc_counts = df_with_salary['Location'].value_counts()
top_10_locations = loc_counts[loc_counts >= 5].head(10).index.tolist()
if top_10_locations:
    df_top_locations = df_with_salary[df_with_salary['Location'].isin(top_10_locations)]
    order = df_top_locations.groupby('Location')['Final_Salary'].median().sort_values(ascending=False).index
    sns.boxplot(data=df_top_locations, x='Location', y='Final_Salary', order=order, palette='Set3', ax=ax)
    ax.set_xlabel('Location')
    ax.set_ylabel('Annual Salary (INR)')
    ax.set_title('Salary Distribution by Top 10 Locations (5+ entries)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'figures', '09_salary_boxplot_by_location.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 09_salary_boxplot_by_location.png")
else:
    print("⚠️  Skipped: 09_salary_boxplot_by_location.png (insufficient data)")

# =============================================================================
# ADDITIONAL VISUALIZATIONS
# =============================================================================
print("\n" + "="*60)
print("4. ADDITIONAL ANALYSIS")
print("="*60)

# Monthly vs Annual Salary Scatter
fig, ax = plt.subplots(figsize=(10, 6))
mask = df_with_salary['Monthly Salary'].notna() & df_with_salary['Final_Salary'].notna()
ax.scatter(df_with_salary.loc[mask, 'Monthly Salary']*12, df_with_salary.loc[mask, 'Final_Salary'], alpha=0.5, c='steelblue')
ax.set_xlabel('Monthly Salary × 12 (INR)')
ax.set_ylabel('Parsed Annual Salary (INR)')
ax.set_title('Monthly Salary (annualized) vs Parsed Annual Salary')
# Add perfect correlation line
max_val = max(df_with_salary.loc[mask, 'Final_Salary'].max(), (df_with_salary.loc[mask, 'Monthly Salary']*12).max())
ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.8, label='Perfect match')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '10_monthly_vs_annual_salary.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 10_monthly_vs_annual_salary.png")

# Top Localities
fig, ax = plt.subplots(figsize=(12, 8))
locality_counts = df['Locality'].dropna().value_counts().head(15)
if len(locality_counts) > 0:
    sns.barplot(x=locality_counts.values, y=locality_counts.index, palette='plasma', ax=ax)
    ax.set_xlabel('Count')
    ax.set_ylabel('Locality')
    ax.set_title('Top 15 Localities by Job Count')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'figures', '11_top_localities.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 11_top_localities.png")
else:
    print("⚠️  Skipped: 11_top_localities.png (no data)")

# Salary by State - All states
fig, ax = plt.subplots(figsize=(14, 10))
salary_by_state_all = df_with_salary.groupby('State')['Final_Salary'].agg(['median', 'count']).sort_values('median', ascending=False)
salary_by_state_all = salary_by_state_all[salary_by_state_all['count'] >= 3]  # States with 3+ jobs
sns.barplot(x=salary_by_state_all['median'], y=salary_by_state_all.index, palette='RdYlGn', ax=ax)
ax.set_xlabel('Median Annual Salary (INR)')
ax.set_ylabel('State')
ax.set_title('Median Salary by State (States with 3+ jobs)')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '12_salary_by_all_states.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 12_salary_by_all_states.png")

# Job Count by Location (Pie chart - top 10)
fig, ax = plt.subplots(figsize=(10, 10))
location_counts = df['Location'].value_counts().head(10)
other_count = df['Location'].value_counts().sum() - location_counts.sum()
pie_data = list(location_counts.values) + [other_count]
pie_labels = list(location_counts.index) + ['Others']
colors = sns.color_palette('husl', len(pie_data))
ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('Job Distribution by Location (Top 10 + Others)')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '13_location_pie_chart.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 13_location_pie_chart.png")

# Salary histogram by top job titles
fig, ax = plt.subplots(figsize=(14, 6))
job_salary_counts = df_with_salary['Job Title'].value_counts()
top_5_jobs = job_salary_counts[job_salary_counts >= 5].head(5).index.tolist()
for job in top_5_jobs:
    job_salaries = df_with_salary[df_with_salary['Job Title'] == job]['Final_Salary'].dropna()
    ax.hist(job_salaries, bins=15, alpha=0.5, label=f'{job} (n={len(job_salaries)})')
ax.set_xlabel('Annual Salary (INR)')
ax.set_ylabel('Frequency')
ax.set_title('Salary Distribution for Top 5 Job Titles (5+ entries)')
ax.legend()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '14_salary_hist_top_jobs.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 14_salary_hist_top_jobs.png")

# Salary violin plot by top states
fig, ax = plt.subplots(figsize=(14, 8))
state_salary_counts = df_with_salary['State'].value_counts()
top_states = state_salary_counts[state_salary_counts >= 5].head(8).index.tolist()
if top_states:
    df_top_states = df_with_salary[df_with_salary['State'].isin(top_states)]
    order = df_top_states.groupby('State')['Final_Salary'].median().sort_values(ascending=False).index
    sns.violinplot(data=df_top_states, x='State', y='Final_Salary', order=order, palette='muted', ax=ax)
    ax.set_xlabel('State')
    ax.set_ylabel('Annual Salary (INR)')
    ax.set_title('Salary Distribution by Top States (Violin Plot)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'figures', '15_salary_violin_by_state.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Saved: 15_salary_violin_by_state.png")

# Salary comparison - Monthly vs Yearly jobs
fig, ax = plt.subplots(figsize=(10, 6))
df_with_salary['Salary_Type'] = df_with_salary['Salary'].apply(
    lambda x: 'Monthly' if 'month' in str(x).lower() else ('Yearly' if 'year' in str(x).lower() else 'Unknown')
)
salary_type_counts = df_with_salary['Salary_Type'].value_counts()
sns.barplot(x=salary_type_counts.index, y=salary_type_counts.values, palette='pastel', ax=ax)
ax.set_xlabel('Salary Type')
ax.set_ylabel('Count')
ax.set_title('Jobs by Salary Type (Monthly vs Yearly)')
for i, v in enumerate(salary_type_counts.values):
    ax.text(i, v + 5, str(v), ha='center')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'figures', '16_salary_type_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ Saved: 16_salary_type_distribution.png")

# =============================================================================
# SAVE SUMMARY TABLES
# =============================================================================
print("\n" + "="*60)
print("5. SAVING SUMMARY TABLES")
print("="*60)

# Salary by Job Title
salary_by_job_df = df_with_salary.groupby('Job Title').agg({
    'Final_Salary': ['mean', 'median', 'min', 'max', 'count']
}).round(0)
salary_by_job_df.columns = ['Mean', 'Median', 'Min', 'Max', 'Count']
salary_by_job_df = salary_by_job_df.sort_values('Median', ascending=False)
salary_by_job_df.to_csv(os.path.join(RESULTS_DIR, 'tables', 'salary_by_job_title.csv'))
print("✅ Saved: tables/salary_by_job_title.csv")

# Salary by Location
salary_by_location_df = df_with_salary.groupby('Location').agg({
    'Final_Salary': ['mean', 'median', 'min', 'max', 'count']
}).round(0)
salary_by_location_df.columns = ['Mean', 'Median', 'Min', 'Max', 'Count']
salary_by_location_df = salary_by_location_df.sort_values('Median', ascending=False)
salary_by_location_df.to_csv(os.path.join(RESULTS_DIR, 'tables', 'salary_by_location.csv'))
print("✅ Saved: tables/salary_by_location.csv")

# Salary by State
salary_by_state_df = df_with_salary.groupby('State').agg({
    'Final_Salary': ['mean', 'median', 'min', 'max', 'count']
}).round(0)
salary_by_state_df.columns = ['Mean', 'Median', 'Min', 'Max', 'Count']
salary_by_state_df = salary_by_state_df.sort_values('Median', ascending=False)
salary_by_state_df.to_csv(os.path.join(RESULTS_DIR, 'tables', 'salary_by_state.csv'))
print("✅ Saved: tables/salary_by_state.csv")

# Overall summary
summary_stats = pd.DataFrame({
    'Metric': ['Total Jobs', 'Jobs with Salary', 'Unique Job Titles', 'Unique Locations', 'Unique States',
               'Mean Salary (INR)', 'Median Salary (INR)', 'Min Salary (INR)', 'Max Salary (INR)', 'Std Dev (INR)'],
    'Value': [len(df), len(df_with_salary), df['Job Title'].nunique(), df['Location'].nunique(), df['State'].nunique(),
              df_with_salary['Final_Salary'].mean(), df_with_salary['Final_Salary'].median(), 
              df_with_salary['Final_Salary'].min(), df_with_salary['Final_Salary'].max(), df_with_salary['Final_Salary'].std()]
})
summary_stats.to_csv(os.path.join(RESULTS_DIR, 'tables', 'overall_summary.csv'), index=False)
print("✅ Saved: tables/overall_summary.csv")

print("\n" + "="*60)
print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("="*60)
print(f"\n📁 Output location: {RESULTS_DIR}")
print(f"   - figures/: {len(os.listdir(os.path.join(RESULTS_DIR, 'figures')))} PNG files")
print(f"   - tables/: {len(os.listdir(os.path.join(RESULTS_DIR, 'tables')))} CSV files")
