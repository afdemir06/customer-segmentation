from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd
import numpy as np

class RfmTransformer(BaseEstimator,TransformerMixin):
    def __init__(self,customer_col,date_col,amount_col,vip_treshold=3):
        self.customer_column=customer_col
        self.date_column=date_col
        self.amount_column=amount_col
        self.vip_treshold=vip_treshold
    def fit(self,data):
        return self
    def transform(self,data):
        c_data=data.copy()
        c_data=c_data[[self.customer_column,self.date_column,self.amount_column]]
        rfm_df=c_data.groupby(self.customer_column).agg(
            frequency=(self.date_column,"count"),
            monetary=(self.amount_column,"sum"),
            last_date=(self.date_column,"max")
        )
        monetory_median=rfm_df["monetary"].median()
        rfm_df["recency"]=(pd.Timestamp.now()-rfm_df["last_date"]).dt.days
        rfm_df=rfm_df.drop(columns=["last_date"])
        rfm_df["is_vip"]=np.where(rfm_df["monetary"]>monetory_median*self.vip_treshold,"VIP","Normal")

        return rfm_df