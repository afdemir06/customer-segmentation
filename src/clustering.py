from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pandas as pd

class ClusterTransformer(BaseEstimator,TransformerMixin):
    def __init__(self,number_of_clusters=None):
        self.number_of_clusters=number_of_clusters
    def fit(self,data):
        normal_customers_df=data[data["is_vip"]=="Normal"].drop(columns=["is_vip"])
        if self.number_of_clusters is None:
            inertians=[]
            k_range=range(2,11)

            for k in k_range:
                kmeans=KMeans(n_clusters=k,random_state=42)
                kmeans.fit(normal_customers_df)
                inertians.append(kmeans.inertia_)

            knee=KneeLocator(k_range,inertians,curve="convex",direction="decreasing")
            self.optimal_k=knee.knee
        else:
            self.optimal_k=self.number_of_clusters
        return self
    def transform(self,data):
        c_data=data.copy()

        normal_customers_df=c_data[c_data["is_vip"]=="Normal"].drop(columns=["is_vip"])
        vip_customers_df=c_data[c_data["is_vip"]=="VIP"].drop(columns=["is_vip"])
        kmeans=KMeans(n_clusters=self.optimal_k,random_state=42)
        kmeans.fit(normal_customers_df)
        normal_customers_df["cluster"]=kmeans.labels_
        vip_customers_df["cluster"]="VIP"

        concated_df=pd.concat([vip_customers_df,normal_customers_df],ignore_index=True)
        return concated_df