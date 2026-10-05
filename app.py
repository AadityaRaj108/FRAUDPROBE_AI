
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.model import FraudModel

MODEL_PATH = ROOT / "artifacts" / "fraud_model.joblib"
DATA_PATH = ROOT / "data" / "train_transaction.csv"

st.set_page_config(
    page_title="FRAUDPROBE AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM UI
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(16,185,129,.08), transparent 28%),
        radial-gradient(circle at 10% 90%, rgba(16,185,129,.045), transparent 25%),
        #080b0a;
    color: #f5f7f6;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 3rem 4rem;
}

section[data-testid="stSidebar"] {
    background: #0b0f0e;
    border-right: 1px solid rgba(255,255,255,.07);
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

.logo {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.logo span {
    color: #19d98b;
}

.logo-sub {
    color: #78827e;
    font-size: 11px;
    margin-bottom: 28px;
}

.nav-label {
    color: #5e6965;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 18px 0 8px;
}

.hero {
    padding: 10px 0 24px;
}

.eyebrow {
    color: #19d98b;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.hero h1 {
    font-size: 40px;
    line-height: 1.05;
    letter-spacing: -1.8px;
    margin: 0;
    color: #f7faf8;
}

.hero p {
    color: #89938f;
    margin-top: 10px;
    font-size: 14px;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(25,217,139,.08);
    border: 1px solid rgba(25,217,139,.18);
    color: #72e9b7;
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 11px;
    font-weight: 600;
}

.dot {
    width: 7px;
    height: 7px;
    background: #19d98b;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(25,217,139,.8);
}

.kpi {
    background: linear-gradient(145deg, #101514, #0c100f);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px;
    padding: 19px;
    min-height: 125px;
    box-shadow: 0 12px 35px rgba(0,0,0,.18);
}

.kpi-title {
    color: #7e8985;
    font-size: 11px;
    font-weight: 600;
}

.kpi-value {
    color: #f5f8f6;
    font-size: 29px;
    font-weight: 800;
    margin-top: 10px;
    letter-spacing: -1px;
}

.kpi-green {
    color: #19d98b;
}

.kpi-danger {
    color: #ff7373;
}

.card {
    background: linear-gradient(145deg, rgba(18,23,21,.98), rgba(12,16,15,.98));
    border: 1px solid rgba(255,255,255,.065);
    border-radius: 18px;
    padding: 21px;
    margin-bottom: 18px;
}

.card-title {
    font-size: 15px;
    font-weight: 700;
    color: #edf2ef;
}

.card-sub {
    color: #737e79;
    font-size: 11px;
    margin-top: 4px;
    margin-bottom: 15px;
}

.risk {
    border-radius: 16px;
    padding: 24px;
    background: linear-gradient(145deg, #101816, #0d1210);
    border: 1px solid rgba(25,217,139,.18);
    text-align: center;
}

.risk-score {
    font-size: 62px;
    font-weight: 800;
    line-height: 1;
    color: #19d98b;
}

.risk-label {
    color: #88938e;
    font-size: 11px;
    margin-top: 7px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.signal {
    padding: 13px 15px;
    border-radius: 12px;
    background: #111715;
    border: 1px solid rgba(255,255,255,.05);
    margin: 7px 0;
    color: #b7c0bc;
    font-size: 12px;
}

.signal strong {
    color: #f0f4f2;
}

div[data-testid="stButton"] > button {
    border-radius: 10px;
    border: 1px solid rgba(25,217,139,.25);
    background: #102019;
    color: #dff9ec;
    font-weight: 600;
    transition: all .2s ease;
}

div[data-testid="stButton"] > button:hover {
    border-color: #19d98b;
    background: #143025;
    transform: translateY(-1px);
}

div[data-testid="stDownloadButton"] > button {
    border-radius: 10px;
    background: #19d98b;
    color: #06120c;
    font-weight: 800;
    border: none;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stTextArea textarea {
    background: #0e1311 !important;
    border-color: rgba(255,255,255,.08) !important;
    color: #f4f7f5 !important;
    border-radius: 10px !important;
}

label {
    color: #9da8a3 !important;
    font-size: 12px !important;
}

div[data-testid="stFileUploader"] {
    background: #0d1210;
    border: 1px dashed rgba(25,217,139,.3);
    border-radius: 15px;
    padding: 12px;
}

[data-testid="stMetric"] {
    background: #101513;
    border: 1px solid rgba(255,255,255,.06);
    padding: 14px;
    border-radius: 14px;
}

hr {
    border-color: rgba(255,255,255,.06);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    try:
        return FraudModel().load(MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Model loading failed: {type(e).__name__}: {e}") from e


@st.cache_data
def load_sample_data():
    if not DATA_PATH.exists():
        return None
    try:
        return pd.read_csv(DATA_PATH, nrows=25000)
    except Exception:
        return None


def money(x):
    return f"${x:,.2f}"


def risk_level(prob):
    if prob >= 0.85:
        return "CRITICAL"
    if prob >= 0.65:
        return "HIGH"
    if prob >= 0.35:
        return "MEDIUM"
    return "LOW"


def risk_color(level):
    return {
        "LOW": "#19d98b",
        "MEDIUM": "#eab308",
        "HIGH": "#f97316",
        "CRITICAL": "#ef4444",
    }.get(level, "#19d98b")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="logo">FRAUD<span>PROBE</span> AI</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="logo-sub">RISK INTELLIGENCE PLATFORM</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Command Center",
            "Fraud Detection",
            "Batch Analysis",
            "Investigations",
            "Analytics",
            "Model Intelligence",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    model = load_model()

    if model:
        st.markdown(
            '<div class="status"><span class="dot"></span> AI ENGINE ONLINE</div>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Model not found")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("FRAUDPROBE AI v1.0")
    st.caption("IEEE-CIS Fraud Detection")


# ============================================================
# DATA
# ============================================================

df = load_sample_data()

if df is not None and "isFraud" in df.columns:
    total_tx = len(df)
    fraud_tx = int(df["isFraud"].sum())
    fraud_rate = fraud_tx / total_tx if total_tx else 0
    avg_amount = float(df["TransactionAmt"].mean()) if "TransactionAmt" in df else 0
    fraud_value = float(
        df.loc[df["isFraud"] == 1, "TransactionAmt"].sum()
    ) if "TransactionAmt" in df else 0
else:
    total_tx = fraud_tx = 0
    fraud_rate = avg_amount = fraud_value = 0


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">AI SECURITY OPERATIONS</div>
        <h1>Command Center</h1>
        <p>Real-time fraud intelligence, transaction risk and threat visibility.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">TRANSACTIONS ANALYZED</div>
            <div class="kpi-value">{total_tx:,}</div>
            <div class="kpi-green">● Dataset active</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">FRAUD DETECTED</div>
            <div class="kpi-value kpi-danger">{fraud_tx:,}</div>
            <div class="kpi-danger">● Suspicious activity</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">FRAUD RATE</div>
            <div class="kpi-value">{fraud_rate:.2%}</div>
            <div class="kpi-green">● Detection baseline</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">VALUE AT RISK</div>
            <div class="kpi-value">{money(fraud_value)}</div>
            <div class="kpi-danger">● Fraud exposure</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.7, 1])

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Fraud Activity</div>
            <div class="card-sub">Observed transaction fraud distribution</div>
        """, unsafe_allow_html=True)

        if df is not None:
            chart_df = df.copy()
            chart_df["Status"] = chart_df["isFraud"].map(
                {0: "Legitimate", 1: "Fraud"}
            )

            fig = px.histogram(
                chart_df,
                x="TransactionAmt",
                color="Status",
                nbins=45,
                log_y=True,
            )

            fig.update_layout(
                height=330,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8c9792"),
                legend=dict(orientation="h"),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Threat Distribution</div>
            <div class="card-sub">Fraudulent vs legitimate transactions</div>
        """, unsafe_allow_html=True)

        if df is not None:
            counts = df["isFraud"].value_counts().rename(
                index={0: "Legitimate", 1: "Fraud"}
            )

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=counts.index,
                        values=counts.values,
                        hole=.68,
                        textinfo="percent",
                    )
                ]
            )

            fig.update_layout(
                height=330,
                margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8c9792"),
                showlegend=True,
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Recent Threat Intelligence</div>
        <div class="card-sub">Latest transactions requiring attention</div>
    """, unsafe_allow_html=True)

    if df is not None:
        recent = df[df["isFraud"] == 1].head(8)

        if len(recent):
            show_cols = [
                c for c in
                ["TransactionID", "TransactionAmt", "ProductCD", "card1", "isFraud"]
                if c in recent.columns
            ]

            display = recent[show_cols].copy()

            if "TransactionAmt" in display:
                display["TransactionAmt"] = display["TransactionAmt"].map(
                    lambda x: f"${x:,.2f}"
                )

            display["Risk"] = "HIGH"
            display = display.drop(columns=["isFraud"], errors="ignore")

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FRAUD DETECTION
# ============================================================

elif page == "Fraud Detection":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">TRANSACTION INTELLIGENCE</div>
        <h1>Fraud Detection</h1>
        <p>Analyze an individual transaction using the trained AI risk engine.</p>
    </div>
    """, unsafe_allow_html=True)

    if model is None:
        st.error("Fraud model is unavailable. Train the model first.")
        st.stop()

    left, right = st.columns([1.15, .85])

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Transaction Input</div>
            <div class="card-sub">Enter the transaction attributes available to the model.</div>
        """, unsafe_allow_html=True)

        amount = st.number_input(
            "Transaction Amount",
            min_value=0.0,
            value=120.00,
            step=10.0,
        )

        col1, col2 = st.columns(2)

        with col1:
            product = st.selectbox(
                "Product Category",
                ["W", "H", "C", "S", "R"]
            )

        with col2:
            card1 = st.number_input(
                "Card Identifier",
                min_value=1,
                value=10000,
                step=1,
            )

        col3, col4 = st.columns(2)

        with col3:
            addr1 = st.number_input(
                "Billing Address",
                min_value=0,
                value=100,
                step=1,
            )

        with col4:
            addr2 = st.number_input(
                "Region",
                min_value=0,
                value=87,
                step=1,
            )

        email = st.text_input(
            "Purchaser Email Domain",
            value="gmail.com"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        analyze = st.button(
            "⚡ ANALYZE TRANSACTION",
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        if analyze:
            sample = pd.DataFrame([{
                "TransactionAmt": amount,
                "ProductCD": product,
                "card1": card1,
                "addr1": addr1,
                "addr2": addr2,
                "P_emaildomain": email,
            }])

            try:
                probability = float(model.predict_proba(sample)[0])

                score = int(max(0, min(100, probability * 100)))
                level = risk_level(probability)
                rc = risk_color(level)

                st.markdown(f"""
                <div class="risk" style="border-color:{rc}55">
                    <div class="risk-score" style="color:{rc}">{score}</div>
                    <div class="risk-label">Risk Score / 100</div>
                    <br>
                    <div style="
                        display:inline-block;
                        padding:7px 15px;
                        border-radius:999px;
                        background:{rc}18;
                        color:{rc};
                        font-weight:800;
                        font-size:11px;
                    ">
                        {level}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown("""
                <div class="card">
                    <div class="card-title">AI Assessment</div>
                    <div class="card-sub">Model-generated transaction risk interpretation</div>
                """, unsafe_allow_html=True)

                if level in ["HIGH", "CRITICAL"]:
                    explanation = (
                        "The model identifies this transaction as requiring "
                        "additional review based on its learned transaction patterns."
                    )
                elif level == "MEDIUM":
                    explanation = (
                        "The transaction contains signals that differ from "
                        "normal activity. Additional verification is recommended."
                    )
                else:
                    explanation = (
                        "The transaction currently appears consistent with "
                        "lower-risk patterns in the trained dataset."
                    )

                st.write(explanation)

                st.markdown(f"""
                    <div class="signal">
                        <strong>Risk probability</strong> — {probability:.2%}
                    </div>
                    <div class="signal">
                        <strong>Transaction amount</strong> — ${amount:,.2f}
                    </div>
                    <div class="signal">
                        <strong>Product category</strong> — {product}
                    </div>
                    <div class="signal">
                        <strong>Recommended action</strong> — 
                        {"Investigate" if score >= 65 else "Monitor"}
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction failed: {e}")

        else:
            st.markdown("""
            <div class="card" style="min-height:370px;display:flex;align-items:center;justify-content:center;">
                <div style="text-align:center;">
                    <div style="font-size:48px;">🛡️</div>
                    <div style="font-size:18px;font-weight:700;margin-top:12px;">
                        Awaiting transaction
                    </div>
                    <div style="color:#707b76;font-size:12px;margin-top:6px;">
                        Enter transaction data and run the AI analysis.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# BATCH ANALYSIS
# ============================================================

elif page == "Batch Analysis":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">MASS TRANSACTION SCREENING</div>
        <h1>Batch Analysis</h1>
        <p>Upload a transaction CSV and screen multiple records through the AI engine.</p>
    </div>
    """, unsafe_allow_html=True)

    if model is None:
        st.error("Fraud model is unavailable.")
        st.stop()

    uploaded = st.file_uploader(
        "Drop transaction CSV here",
        type=["csv"],
    )

    if uploaded:

        with st.spinner("Processing transaction batch..."):
            try:
                batch = pd.read_csv(uploaded)

                st.success(
                    f"Loaded {len(batch):,} transactions successfully."
                )

                try:
                    probabilities = model.predict_proba(batch)
                    batch["fraud_probability"] = probabilities
                    batch["risk_score"] = (probabilities * 100).round(1)
                    batch["risk_level"] = [
                        risk_level(x) for x in probabilities
                    ]

                    high_risk = batch[
                        batch["risk_level"].isin(["HIGH", "CRITICAL"])
                    ]

                    a, b, c, d = st.columns(4)

                    a.metric("Transactions", f"{len(batch):,}")
                    b.metric("High Risk", f"{len(high_risk):,}")
                    c.metric(
                        "High-Risk Rate",
                        f"{len(high_risk) / len(batch):.2%}" if len(batch) else "0%"
                    )
                    d.metric(
                        "Max Risk",
                        f"{batch['risk_score'].max():.1f}" if len(batch) else "0"
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                    st.dataframe(
                        batch.head(500),
                        use_container_width=True,
                        hide_index=True,
                    )

                    csv = batch.to_csv(index=False).encode("utf-8")

                    st.download_button(
                        "⬇ DOWNLOAD ANALYSIS CSV",
                        csv,
                        "fraudprobe_analysis.csv",
                        "text/csv",
                    )

                except Exception as e:
                    st.error(
                        "The uploaded CSV does not contain enough compatible "
                        f"features for the current model.\n\n{e}"
                    )

            except Exception as e:
                st.error(f"CSV processing failed: {e}")

    else:
        st.markdown("""
        <div class="card" style="padding:55px;text-align:center;">
            <div style="font-size:46px;">⇧</div>
            <div style="font-size:19px;font-weight:700;margin-top:10px;">
                Upload transaction data
            </div>
            <div style="color:#707b76;font-size:12px;margin-top:7px;">
                CSV files can be analyzed in bulk by the AI engine.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# INVESTIGATIONS
# ============================================================

elif page == "Investigations":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">THREAT RESPONSE</div>
        <h1>Investigations</h1>
        <p>Review suspicious activity and prioritize transactions for investigation.</p>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.warning("Dataset unavailable.")
        st.stop()

    suspicious = df[df["isFraud"] == 1].head(50)

    col1, col2 = st.columns([1.1, .9])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Investigation Queue</div>
            <div class="card-sub">Prioritized suspicious transactions</div>
        """, unsafe_allow_html=True)

        columns = [
            c for c in
            ["TransactionID", "TransactionAmt", "ProductCD", "card1"]
            if c in suspicious.columns
        ]

        st.dataframe(
            suspicious[columns],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">AI Investigation Brief</div>
            <div class="card-sub">Automated analyst context</div>

            <div class="signal">
                <strong>Priority</strong><br>
                High — transaction requires review.
            </div>

            <div class="signal">
                <strong>Detection signal</strong><br>
                Transaction matches patterns associated with fraudulent activity.
            </div>

            <div class="signal">
                <strong>Suggested action</strong><br>
                Verify cardholder identity and transaction context.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">DATA INTELLIGENCE</div>
        <h1>Analytics</h1>
        <p>Explore transaction behavior, fraud patterns and exposure.</p>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.warning("Dataset unavailable.")
        st.stop()

    c1, c2, c3 = st.columns(3)

    c1.metric("Average Transaction", money(avg_amount))
    c2.metric("Fraud Transactions", f"{fraud_tx:,}")
    c3.metric("Fraud Exposure", money(fraud_value))

    st.markdown("<br>", unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
            <div class="card-title">Fraud by Product Category</div>
        """, unsafe_allow_html=True)

        if "ProductCD" in df:
            temp = (
                df.groupby("ProductCD")["isFraud"]
                .sum()
                .reset_index(name="Fraud")
            )

            fig = px.bar(temp, x="ProductCD", y="Fraud")
            fig.update_layout(
                height=320,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8c9792"),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
            <div class="card-title">Transaction Amount Distribution</div>
        """, unsafe_allow_html=True)

        fig = px.box(
            df,
            x="isFraud",
            y="TransactionAmt",
            log_y=True,
        )

        fig.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8c9792"),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MODEL INTELLIGENCE
# ============================================================

elif page == "Model Intelligence":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">MODEL OPERATIONS</div>
        <h1>Model Intelligence</h1>
        <p>Understand the current fraud detection engine and its performance.</p>
    </div>
    """, unsafe_allow_html=True)

    if model is None:
        st.error("Model unavailable.")
        st.stop()

    metrics = getattr(model, "metrics", {}) or {}

    a, b, c, d = st.columns(4)

    a.metric(
        "ROC-AUC",
        f"{metrics.get('roc_auc', 0):.3f}"
    )

    b.metric(
        "PR-AUC",
        f"{metrics.get('average_precision', 0):.3f}"
    )

    c.metric(
        "Training Rows",
        f"{metrics.get('rows', 0):,}"
    )

    d.metric(
        "Features",
        f"{metrics.get('features', 0):,}"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Model Status</div>
            <div class="card-sub">Current deployed intelligence engine</div>

            <div class="signal">
                <strong>Model</strong><br>
                Logistic Regression — balanced classification
            </div>

            <div class="signal">
                <strong>Dataset</strong><br>
                IEEE-CIS Fraud Detection
            </div>

            <div class="signal">
                <strong>Detection Target</strong><br>
                isFraud
            </div>

            <div class="signal">
                <strong>Threshold</strong><br>
        """, unsafe_allow_html=True)

        st.write(f"{metrics.get('threshold', 0.5):.4f}")

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Model Performance</div>
            <div class="card-sub">Validation metrics from current training run</div>
        """, unsafe_allow_html=True)

        perf = pd.DataFrame({
            "Metric": ["ROC-AUC", "PR-AUC"],
            "Score": [
                metrics.get("roc_auc", 0),
                metrics.get("average_precision", 0),
            ],
        })

        fig = px.bar(
            perf,
            x="Metric",
            y="Score",
            range_y=[0, 1],
            text_auto=".3f",
        )

        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8c9792"),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">SECURITY REPORTING</div>
        <h1>Reports</h1>
        <p>Generate a concise snapshot of the current fraud environment.</p>
    </div>
    """, unsafe_allow_html=True)

    report = f"""
FRAUDPROBE AI — FRAUD INTELLIGENCE REPORT

Transactions analyzed: {total_tx:,}
Fraud transactions: {fraud_tx:,}
Fraud rate: {fraud_rate:.2%}
Average transaction value: ${avg_amount:,.2f}
Fraud exposure: ${fraud_value:,.2f}

Detection engine:
IEEE-CIS Fraud Detection
Target: isFraud

Current model:
ROC-AUC: {getattr(model, "metrics", {}).get("roc_auc", 0) if model else 0:.4f}
PR-AUC: {getattr(model, "metrics", {}).get("average_precision", 0) if model else 0:.4f}

Generated by FRAUDPROBE AI.
"""

    st.markdown("""
    <div class="card">
        <div class="card-title">Executive Security Summary</div>
        <div class="card-sub">Current dataset intelligence snapshot</div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Report Preview",
        report,
        height=330,
        label_visibility="collapsed",
    )

    st.download_button(
        "⬇ EXPORT SECURITY REPORT",
        report.encode("utf-8"),
        "fraudprobe_security_report.txt",
        "text/plain",
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center;color:#4e5955;font-size:10px;margin-top:35px;'>"
    "FRAUDPROBE AI • AI-POWERED CREDIT CARD FRAUD DETECTION & RISK INTELLIGENCE"
    "</div>",
    unsafe_allow_html=True,
)

