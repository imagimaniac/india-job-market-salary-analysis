# India Job Market & Salary Analysis

Exploratory Data Analysis (EDA) and visualization of the India Job Market & Salary Dataset from Kaggle.

## 📊 Project Overview

This project performs a comprehensive exploratory data analysis on the India Job Market & Salary Dataset to uncover insights about:
- Salary distributions across different job roles
- Top-paying companies and cities
- Job market trends and demand
- Skills and experience correlation with salaries

## 📁 Project Structure

```
india-job-market-salary-analysis/
├── data/
│   ├── raw/                  # Original downloaded data
│   └── processed/            # Cleaned and transformed data
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_eda_univariate.ipynb
│   ├── 03_eda_bivariate.ipynb
│   └── 04_visualizations.ipynb
├── src/
│   ├── utils/                # Utility functions
│   └── visualization/       # Plotting functions
├── models/                   # Saved models (if any)
├── results/
│   ├── figures/              # Generated visualizations
│   └── tables/               # Generated summary tables
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── setup.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/india-job-market-salary-analysis.git
cd india-job-market-salary-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the dataset:
   - Go to [Kaggle - India Job Market & Salary Dataset](https://www.kaggle.com/datasets/kapoorprakhar/india-job-market-and-salary-dataset)
   - Download the dataset
   - Place it in `data/raw/`

5. Run Jupyter Notebook:
```bash
jupyter notebook
```

## 📈 Analysis Highlights

### Univariate Analysis
- Salary distribution analysis
- Job title frequency
- Company distribution
- Location analysis

### Bivariate Analysis
- Salary by job title
- Salary by location
- Salary by company size
- Experience vs Salary

### Visualizations
- Histograms and box plots
- Bar charts for categorical comparisons
- Heatmaps for correlations
- Interactive plots with Plotly

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## 👤 Author

Your Name - [Your GitHub Profile]

## 🙏 Acknowledgments

- Dataset: [Kaggle - India Job Market & Salary Dataset](https://www.kaggle.com/datasets/kapoorprakhar/india-job-market-and-salary-dataset)
