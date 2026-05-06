from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from src import data_cleaning,rfm,clustering
import pandas as pd
import logging

app=FastAPI()

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

class RequestsCheking(BaseModel):
    customer_col:str
    date_col:str
    amount_col:str
    data_path:str
    number_of_clusters:int | None = None
    vip_treshold:int | None = None

@app.post("/process_data")
async def process_data(requests: RequestsCheking):
    try:
        logger.info("Transaction started")
        if requests.data_path.endswith(".csv"):
            df=pd.read_csv(requests.data_path)
        else:
            df=pd.read_excel(requests.data_path)
        logger.info(f"Columns: {df.columns.tolist()}")
        df=data_cleaning.DataCleanerTransformer(
            requests.customer_col,
            requests.date_col,
            requests.amount_col
        ).fit_transform(df)
        df=rfm.RfmTransformer(
            requests.customer_col,
            requests.date_col,
            requests.amount_col,
            requests.vip_treshold
        ).fit_transform(df)
        df=clustering.ClusterTransformer(requests.number_of_clusters).fit_transform(df)
        logger.info("Transaction completed")
        return {"status":"succes","data":df.to_dict(orient="records")}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500,detail=str(e))