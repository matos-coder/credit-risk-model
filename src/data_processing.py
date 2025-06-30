# ==============================================================================
# 10 Academy - Credit Risk Modeling - Week 5
# Task 3: Feature Engineering Script (src/data_processing.py)
#
# This script builds a robust, automated, and reproducible data processing
# pipeline that transforms raw data into a model-ready format.
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# --- Custom Transformers for Feature Engineering ---
# To integrate our custom feature engineering logic into a scikit-learn Pipeline,
# we create custom classes that inherit from BaseEstimator and TransformerMixin.
# This makes our code modular, reusable, and compatible with the scikit-learn ecosystem.

class AggregateFeatureCreator(BaseEstimator, TransformerMixin):
    """
    A custom transformer to create aggregate features for each customer.
    This transformer calculates statistics based on a customer's transaction history.
    """
    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything from the data,
        # so we just return self.
        return self

    def transform(self, X, y=None):
        # Ensure the input is a DataFrame
        X_copy = X.copy()

        # --- Create Aggregate Features ---
        # Group by 'CustomerId' to calculate metrics for each customer.
        # We use .agg() to compute multiple statistics at once.
        customer_agg_features = X_copy.groupby('CustomerId')['Amount'].agg([
            'sum',    # Total Transaction Amount
            'mean',   # Average Transaction Amount
            'count',  # Transaction Count
            'std'     # Standard Deviation of Transaction Amounts
        ]).reset_index()

        # Rename columns to be more descriptive.
        customer_agg_features.columns = [
            'CustomerId',
            'TotalTransactionAmount',
            'AverageTransactionAmount',
            'TransactionCount',
            'StdDevTransactionAmount'
        ]

        # Fill NaN values in StdDevTransactionAmount (which occur for customers
        # with only one transaction) with 0.
        customer_agg_features['StdDevTransactionAmount'] = customer_agg_features['StdDevTransactionAmount'].fillna(0)

        # Merge these new features back into the original DataFrame.
        X_copy = pd.merge(X_copy, customer_agg_features, on='CustomerId', how='left')
        
        return X_copy
    
class TimeFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    A custom transformer to extract time-based features from the 'TransactionStartTime' column.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_copy = X.copy()
        
        # --- Extract Features ---
        # Convert 'TransactionStartTime' to datetime objects.
        X_copy['TransactionStartTime'] = pd.to_datetime(X_copy['TransactionStartTime'])

        # Extract various time-based features.
        X_copy['TransactionHour'] = X_copy['TransactionStartTime'].dt.hour
        X_copy['TransactionDay'] = X_copy['TransactionStartTime'].dt.day
        X_copy['TransactionDayOfWeek'] = X_copy['TransactionStartTime'].dt.dayofweek # Monday=0, Sunday=6
        X_copy['TransactionMonth'] = X_copy['TransactionStartTime'].dt.month
        X_copy['TransactionYear'] = X_copy['TransactionStartTime'].dt.year

        # We can also create features that measure time elapsed.
        # For example, days since the first transaction for that customer.
        X_copy['DaysSinceFirstTransaction'] = (X_copy['TransactionStartTime'] - X_copy.groupby('CustomerId')['TransactionStartTime'].transform('min')).dt.days

        return X_copy