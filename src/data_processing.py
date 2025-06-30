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

