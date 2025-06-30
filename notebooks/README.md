
## Task 2: Exploratory Data Analysis (EDA)
### Objective

The primary goal of this Exploratory Data Analysis (EDA) is to explore the dataset to uncover patterns, identify data quality issues, and form actionable hypotheses that will guide the subsequent feature engineering and modeling phases. All exploratory work was conducted in the `notebooks/1.0-eda.ipynb` Jupyter Notebook, which is intended solely for exploration and not for production code.

---

### 1. Overview of the Data

- **Dimensions:** The dataset contains 95,662 rows (representing individual transactions) and 12 columns (features).
- **Data Types:** The columns include a mix of data types:
  - `object`: Categorical and identifier columns (e.g., TransactionId, AccountId, ProductCategory).
  - `int64`: Numerical columns (e.g., CountryCode, Value, PricingStrategy, FraudResult).
  - `float64`: The Amount column.
- **Initial Inspection:** A review of the first few rows confirmed the content and format of each column as described in the data dictionary.

---

### 2. Identifying Missing Values

- **Findings:** A thorough check revealed zero missing values across all columns in the dataset.
- **Implication:** This simplifies the data preprocessing pipeline, as no imputation or removal strategies for missing data are necessary. We can proceed directly to feature engineering.

---

### 3. Summary Statistics

- **Numerical Features (Amount, Value):**
  - The mean value for Amount is significantly different from the median (50th percentile), indicating a skewed distribution.
  - A large difference between the 75th percentile and the max value for both Amount and Value suggests the presence of outliers.
- **Categorical Features (ProductCategory, ChannelId, etc.):**
  - `ProductCategory`: 'airtime' is the most frequent category.
  - `ChannelId`: 'ChannelId_3' dominates the transactions.
  - `ProviderId`: 'ProviderId_4' and 'ProviderId_6' are the most common providers, showing a concentration of transactions with a few key providers.

---

### 4. Distribution Analysis

#### Distribution of Numerical Features

- **Observation:** Histograms for Amount and Value show both features are heavily right-skewed. Most transactions are of low value, with a long tail of very high-value transactions.
- **Implication:** This skewness can negatively impact certain machine learning models. A transformation (e.g., log transformation) will likely be necessary during feature engineering to normalize these distributions.

#### Distribution of Categorical Features

- **Observation:** There is a significant imbalance in several key categorical features:
  - `ProductCategory`: 'airtime' and 'financial_services' account for a large majority of transactions.
  - `ChannelId`: One channel is responsible for most of the transaction volume.
- **Implication:** The dominance of a few categories means these will be very influential in the model. Creating interaction features between these dominant categories could capture important predictive signals.

---

### 5. Outlier Detection

- **Observation:** Box plots for Amount and Value clearly illustrate the presence of numerous significant outliers, appearing as points far beyond the upper whisker of the plot.
- **Implication:** These outliers could represent legitimate, high-value transactions or potentially fraudulent activity. Their presence must be handled carefully, as they can disproportionately influence model training. Using robust scaling techniques (like RobustScaler) or transformations will be critical.

---

### 6. Correlation Analysis

- **Method:** A correlation matrix and heatmap were generated to understand the linear relationships between the main numerical features (Amount, Value, and the target FraudResult).
- **Observation:**
  - Amount and Value are highly correlated (0.81).
  - The linear correlation between Amount and FraudResult is extremely weak (-0.05).
- **Implication:** This lack of a strong linear relationship suggests that fraud cannot be predicted simply by the transaction amount. The underlying patterns of risk are likely more complex and non-linear, reinforcing the need for more sophisticated models (like tree-based ensembles) and detailed feature engineering.

---

### Summary of Top 5 EDA Insights & Actionable Hypotheses

1. **Insight:** The transaction Amount is heavily right-skewed with significant outliers.  
   **Hypothesis:** Normalizing the Amount feature using a log transformation will improve model performance and stability. The outliers may represent a distinct customer segment (e.g., businesses) that could be flagged with a separate binary feature.

2. **Insight:** Customer activity is highly concentrated in specific ProductCategory and ChannelId values.  
   **Hypothesis:** The specific combination of ProductCategory and ChannelId is a strong predictor of customer behavior and credit risk. Creating interaction features from these columns will capture valuable predictive patterns.

3. **Insight:** There is no direct, linear relationship between the transaction amount and the likelihood of fraud.  
   **Hypothesis:** To build an effective risk model, we must rely on non-linear models (e.g., Gradient Boosting, Random Forest) that can capture complex interactions between multiple features, rather than just simple trends.

4. **Insight:** The dataset is complete and has no missing values.  
   **Hypothesis:** The data preprocessing pipeline can be streamlined, as no time is needed for developing or implementing data imputation strategies. We can proceed directly to feature creation.

5. **Insight:** Time-based patterns may exist within the TransactionStartTime.  
   **Hypothesis:** The time of day, day of the week, or month of the transaction could be a critical predictor of risk. We must engineer features from the TransactionStartTime column to capture these potential temporal patterns.