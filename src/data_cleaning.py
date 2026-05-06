from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd

class DataCleanerTransformer(BaseEstimator,TransformerMixin):
    def __init__(self,customer_col,date_col,amount_col):
        self.customer_column=customer_col
        self.date_column=date_col
        self.amount_column=amount_col
    def fit(self,data):
        data_=data[[self.customer_column,self.date_column,self.amount_column]]
        self.numeric_columns=data_.select_dtypes(include=["number"]).columns
        self.medians=data_[self.numeric_columns].median()
        return self
    def transform(self,data):
        c_data=data.copy()
        c_data=c_data[[self.customer_column,self.date_column,self.amount_column]]
        c_data=c_data.fillna(self.medians)
        c_data[self.date_column]=pd.to_datetime(c_data[self.date_column],errors="coerce")
        return c_data