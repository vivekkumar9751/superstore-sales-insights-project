# Superstore Sales Insights Project

This project provides a comprehensive analysis of a superstore's sales data. The workflow is broken down into distinct steps, from initial data cleaning and exploratory analysis to in-depth customer segmentation, feature engineering, and finally, exporting the results to a database.

## Project Workflow

The project is structured as a sequential pipeline. Each script performs a specific task and prepares data for the next step.

### Step 1: Data Cleaning & Initial EDA (`main.py`)

*   **Purpose**: To perform initial cleaning on the raw dataset and conduct a preliminary exploratory data analysis (EDA).
*   **Input**: Reads the raw `Superstore.csv` file.
*   **Actions**:
    *   Converts date columns to the correct format.
    *   Creates `Order Month` and `Order Year` for time-series analysis.
    *   Calculates and prints high-level KPIs (Total Sales, Profit, Orders).
    *   Generates bar charts for sales by category, sub-category, and region.
*   **Output**:
    *   `cleaned_Superstore.csv`: A processed version of the raw data, saved in the project root.
    *   **Note**: This script identifies but *does not remove* duplicate rows from the output file.

### Step 2: Customer Segmentation - RFM Analysis (`Day2.py`)

*   **Purpose**: To segment customers based on their purchasing behavior using RFM (Recency, Frequency, Monetary) analysis.
*   **Input**: Reads the raw `Superstore.csv` file.
*   **Actions**:
    *   Calculates Recency, Frequency, and Monetary values for each customer.
    *   Assigns scores and groups customers into descriptive segments like `Champions`, `Loyal Customers`, and `At Risk`.
    *   Generates a pie chart of customer segments and a heatmap of Recency vs. Frequency.
*   **Output**:
    *   `Recency_Frequency_Monetary.csv`: A file containing the detailed RFM data for each customer.
    *   **Note**: The generated plots are displayed on-screen but are not saved to the `images` directory.

### Step 3: In-Depth Analysis & Feature Engineering (`day3.py`)

*   **Purpose**: To perform a deep-dive analysis on the cleaned data, generating advanced metrics and features.
*   **Input**: Reads `Data/cleaned_Superstore.csv`.
*   **Actions**:
    *   **Data Preparation**: Handles outliers and normalizes numerical features.
    *   **Customer Analysis**: Calculates Customer Lifetime Value (CLV) and engineers features for churn prediction.
    *   **Product Analysis**: Identifies best-selling products, analyzes profitability, and performs market basket analysis to find associated products.
    *   **Trend & Regional Analysis**: Analyzes monthly sales trends, seasonality, and region-wise performance.
*   **Output**:
    *   Exports over 10 detailed CSV reports into the `/Reports` directory, including `customer_lifetime_value.csv`, `association_rules.csv`, and more.

### Step 4: Database Export (`day4.py`)

*   **Purpose**: To load the processed CSV files into a central MySQL database for persistent storage and easier access by other applications (e.g., dashboards).
*   **Input**: Reads `Data/cleaned_Superstore.csv` and `Data/Recency_Frequency_Monetary.csv`.
*   **Actions**:
    *   Connects to a local MySQL database.
    *   Exports the DataFrames to two tables: `cleaned_Superstore` and `Recency_Frequency_Monetary`.
*   **Output**:
    *   Two tables created or replaced in the `superstore_data` MySQL database.
    *   **Security Note**: The database credentials are hardcoded in the script. This is a security risk and should be avoided in a production environment.

## How to Run the Pipeline

1.  **Prerequisites**: Ensure you have the required Python libraries installed:
    ```bash
    pip install pandas numpy scikit-learn mlxtend matplotlib seaborn sqlalchemy mysql-connector-python
    ```

2.  **Run the scripts in order**: Execute the scripts from the project's root directory.
    ```bash
    # Step 1: Clean the data
    python3 Main/main.py

    # Step 2: Perform RFM Analysis
    python3 Main/Day2.py

    # Before proceeding, move the generated CSVs to the Data directory
    mv cleaned_Superstore.csv Data/
    mv Recency_Frequency_Monetary.csv Data/

    # Step 3: Run the in-depth analysis
    python3 Main/day3.py

    # Step 4 (Optional): Export to MySQL
    python3 Main/day4.py
    ```