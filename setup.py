# India Job Market Salary Analysis

from setuptools import setup, find_packages

setup(
    name="india-job-market-salary-analysis",
    version="1.0.0",
    description="EDA and visualization of India Job Market & Salary Dataset",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.18.0",
    ],
    python_requires=">=3.8",
)
