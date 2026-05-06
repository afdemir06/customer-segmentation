import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
from src.utils import download_results

st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #080C10;
    color: #C8D6E5;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1200px; }

/* Hero header */
.hero {
    border-left: 3px solid #00E5B4;
    padding: 1.2rem 0 1.2rem 1.6rem;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #F0F6FF;
    letter-spacing: -0.03em;
    margin: 0 0 0.3rem 0;
}
.hero p {
    font-size: 0.82rem;
    color: #4A6080;
    margin: 0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00E5B4;
    margin-bottom: 0.8rem;
    margin-top: 2rem;
}

/* Card wrapper */
.card {
    background: #0D1117;
    border: 1px solid #1A2535;
    border-radius: 4px;
    padding: 1.6rem;
    margin-bottom: 1rem;
}

/* Metric cards */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-card {
    flex: 1;
    background: #0D1117;
    border: 1px solid #1A2535;
    border-top: 2px solid #00E5B4;
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
}
.metric-card.vip { border-top-color: #F0A500; }
.metric-card.clusters { border-top-color: #4D9EFF; }
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #F0F6FF;
    line-height: 1;
}
.metric-label {
    font-size: 0.72rem;
    color: #4A6080;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, #00E5B4 0%, #1A2535 60%);
    margin: 2rem 0;
    border: none;
}

/* Streamlit widget overrides */
div[data-testid="stFileUploader"] {
    background: #0D1117 !important;
    border: 1px dashed #1A2535 !important;
    border-radius: 4px !important;
    padding: 1rem !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #00E5B4 !important;
}
label[data-testid="stWidgetLabel"] p {
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #4A6080 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #0D1117 !important;
    border-color: #1A2535 !important;
    color: #C8D6E5 !important;
    border-radius: 4px !important;
}
div[data-testid="stSlider"] { padding: 0.4rem 0; }

/* Button */
div[data-testid="stButton"] > button {
    background: #00E5B4 !important;
    color: #080C10 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.7rem 2.2rem !important;
    margin-top: 1rem !important;
    transition: opacity 0.2s !important;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

/* Download buttons */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #00E5B4 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    border: 1px solid #00E5B4 !important;
    border-radius: 2px !important;
    padding: 0.5rem 1.4rem !important;
    width: 100% !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #00E5B4 !important;
    color: #080C10 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #1A2535 !important;
    border-radius: 4px !important;
}

/* Error / success */
div[data-testid="stAlert"] {
    background: #0D1117 !important;
    border-radius: 4px !important;
    font-size: 0.8rem !important;
}

/* Checkbox */
div[data-testid="stCheckbox"] label p {
    font-size: 0.78rem !important;
    color: #C8D6E5 !important;
    text-transform: none !important;
    letter-spacing: 0.04em !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>Customer Segmentation</h1>
    <p>RFM · K-Means Clustering · VIP Detection</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">01 — Data Source</div>', unsafe_allow_html=True)
raw_file = st.file_uploader("Upload transaction file", type=["csv", "xlsx"], label_visibility="collapsed")

if raw_file is None:
    st.markdown("""
    <div style="background:#0D1117;border:1px dashed #1A2535;border-radius:4px;padding:2.5rem;text-align:center;margin-top:0.5rem;">
        <span style="font-size:0.78rem;color:#4A6080;letter-spacing:0.08em;">
            Drop a CSV or XLSX file to begin · Needs customer ID, date and amount columns
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    df = pd.read_csv(raw_file) if raw_file.name.endswith(".csv") else pd.read_excel(raw_file)

    def check_columns(df, amount_column, date_column):
        original_amount_nulls = df[amount_column].isnull().sum()
        converted_amount_nulls = pd.to_numeric(df[amount_column], errors="coerce").isnull().sum()
        amount_invalid = converted_amount_nulls > original_amount_nulls

        original_date_nulls = df[date_column].isnull().sum()
        converted_date_nulls = pd.to_datetime(df[date_column], errors="coerce").isnull().sum()
        datetime_invalid = converted_date_nulls > original_date_nulls

        if amount_invalid or datetime_invalid:
            return False
        return True

    st.markdown(f"""
    <div style="display:flex;gap:0.6rem;align-items:center;margin:0.8rem 0 1.6rem 0;">
        <span style="background:#0D1117;border:1px solid #1A2535;border-radius:2px;
                     padding:0.3rem 0.8rem;font-size:0.72rem;color:#00E5B4;">
            {raw_file.name}
        </span>
        <span style="font-size:0.72rem;color:#4A6080;">
            {len(df):,} rows · {len(df.columns)} columns
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">02 — Column Mapping</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        customer_col = st.selectbox("Customer ID column", options=df.columns)
    with col2:
        date_col = st.selectbox("Transaction date column", options=df.columns)
    with col3:
        amount_col = st.selectbox("Amount column", options=df.columns)

    st.markdown('<div class="section-label">03 — Parameters</div>', unsafe_allow_html=True)
    pcol1, pcol2 = st.columns([1, 1])
    with pcol1:
        vip_treshold = st.slider("VIP threshold (× monetary median)", min_value=2, max_value=5, value=3)
    with pcol2:
        checkbox = st.checkbox("Set number of clusters manually")
        number_of_clusters = st.number_input("Cluster count", min_value=2, step=1) if checkbox else None

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not check_columns(df, amount_col, date_col):
        st.error("⚠  Column type mismatch — verify the amount and date columns are correct.")
    else:
        os.makedirs("data", exist_ok=True)
        DATA_PATH = f"data/raw_data.{raw_file.name.split('.')[-1]}"
        with open(DATA_PATH, "wb") as f:
            f.write(raw_file.getbuffer())
        if not "data" in st.session_state:
            st.session_state["data"]=None
        if st.session_state["data"] is None:
            if st.button("Run Segmentation →"):
                with st.spinner("Processing — computing RFM scores and clustering..."):
                    response = requests.post(
                    url="http://api:8000/process_data",
                        json={
                            "customer_col": customer_col,
                            "date_col": date_col,
                            "amount_col": amount_col,
                            "data_path": DATA_PATH,
                            "number_of_clusters": number_of_clusters,
                            "vip_treshold": vip_treshold,
                            },
                        )
                if response.status_code != 200:
                    st.error(f"API error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
                else:
                    st.session_state["data"]=response.json()["data"]
                    st.rerun()
        else:
                data=st.session_state["data"]
                df = pd.DataFrame(data)
                vip_df = df[df["cluster"] == "VIP"]
                rest_df = df[df["cluster"] != "VIP"]
                grouped_df = rest_df.groupby("cluster").agg(
                    frequency_mean=("frequency", "mean"),
                    monetary_mean=("monetary", "mean"),
                    recency_mean=("recency", "mean"),
                )
                n_clusters = rest_df["cluster"].nunique()

                st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-card">
                        <div class="metric-value">{len(df):,}</div>
                        <div class="metric-label">Total customers</div>
                    </div>
                    <div class="metric-card vip">
                        <div class="metric-value">{len(vip_df):,}</div>
                        <div class="metric-label">VIP customers</div>
                    </div>
                    <div class="metric-card clusters">
                        <div class="metric-value">{n_clusters}</div>
                        <div class="metric-label">Segments found</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-label">VIP Customers</div>', unsafe_allow_html=True)
                st.dataframe(vip_df, use_container_width=True, hide_index=True)

                st.markdown('<div class="section-label">Segment Overview</div>', unsafe_allow_html=True)
                st.dataframe(grouped_df, use_container_width=True)

                st.markdown('<div class="section-label">Scatter Plot</div>', unsafe_allow_html=True)
                scatter_plot_dict = {
                    "Recency — Frequency": ("recency", "frequency"),
                    "Recency — Monetary": ("recency", "monetary"),
                    "Frequency — Monetary": ("frequency", "monetary"),
                }
                selected_pair = st.selectbox("Axis pair", options=list(scatter_plot_dict.keys()))
                x, y = scatter_plot_dict[selected_pair]
                fig = px.scatter(
                    df, x=x, y=y, color="cluster",
                    color_discrete_sequence=["#00E5B4", "#4D9EFF", "#F0A500", "#FF4D6D", "#A78BFA"],
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="#0D1117",
                    plot_bgcolor="#080C10",
                    font_family="DM Mono",
                    font_color="#4A6080",
                    margin=dict(l=20, r=20, t=20, b=20),
                    legend=dict(bgcolor="#0D1117", bordercolor="#1A2535", borderwidth=1),
                )
                fig.update_xaxes(gridcolor="#1A2535", zerolinecolor="#1A2535")
                fig.update_yaxes(gridcolor="#1A2535", zerolinecolor="#1A2535")
                st.plotly_chart(fig, use_container_width=True)

                st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)
                file_to_download1 = download_results(grouped_df)
                file_to_download2 = download_results(vip_df)
                dcol1, dcol2 = st.columns(2)
                with dcol1:
                    st.download_button(
                        "↓ Download VIP customers",
                        data=file_to_download2,
                        file_name="vip_customers.csv",
                        mime="text/csv",
                    )
                with dcol2:
                    st.download_button(
                        "↓ Download segmented customers",
                        data=file_to_download1,
                        file_name="clustered_customers.csv",
                        mime="text/csv",
                    )