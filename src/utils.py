def download_results(data):
    df=data.to_csv(index=False).encode("utf-8")
    return df