import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

API_URL = "https://abdhur-sentryai-backend.hf.space"

st.set_page_config(
    page_title="SentryAI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp { background: #0f1117; }

.navbar {
    background: #161b22;
    border-bottom: 1px solid #21262d;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-logo {
    width: 32px;
    height: 32px;
    background: #3b82f6;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.nav-title {
    font-size: 18px;
    font-weight: 700;
    color: #f0f6fc;
}

.page-header {
    padding: 0 0 24px;
}

.page-title {
    font-size: 24px;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 14px;
    color: #8b949e;
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #f0f6fc;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #21262d;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 16px 0;
}

.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 18px;
}

.stat-label {
    font-size: 11px;
    font-weight: 600;
    color: #8b949e;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 6px;
}

.badge-green {
    font-size: 11px;
    color: #3fb950;
    background: rgba(63,185,80,0.1);
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}

.badge-red {
    font-size: 11px;
    color: #f85149;
    background: rgba(248,81,73,0.1);
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}

.badge-blue {
    font-size: 11px;
    color: #3b82f6;
    background: rgba(59,130,246,0.1);
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}

.alert-danger {
    background: rgba(248,81,73,0.08);
    border: 1px solid rgba(248,81,73,0.2);
    border-left: 3px solid #f85149;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    color: #fca5a5;
    font-size: 13px;
    margin: 12px 0;
}

.alert-success {
    background: rgba(63,185,80,0.08);
    border: 1px solid rgba(63,185,80,0.2);
    border-left: 3px solid #3fb950;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    color: #86efac;
    font-size: 13px;
    margin: 12px 0;
}

.alert-warning {
    background: rgba(210,153,34,0.08);
    border: 1px solid rgba(210,153,34,0.2);
    border-left: 3px solid #d2991a;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    color: #fcd34d;
    font-size: 13px;
    margin: 12px 0;
}

.status-dot-green {
    display: inline-block;
    width: 8px; height: 8px;
    background: #3fb950;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 6px #3fb950;
}

.status-dot-red {
    display: inline-block;
    width: 8px; height: 8px;
    background: #f85149;
    border-radius: 50%;
    margin-right: 6px;
}

.stButton > button {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #c9d1d9 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #3b82f6 !important;
    border-color: #3b82f6 !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 8px;
    padding: 4px;
    border: 1px solid #21262d;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #8b949e;
    font-size: 13px;
    padding: 6px 16px;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: #3b82f6 !important;
    color: white !important;
    border: none !important;
}

.stTextArea textarea {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #c9d1d9 !important;
    font-size: 14px !important;
}

.stFileUploader > div {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 10px !important;
}

.stFileUploader label { display: none !important; }

.stProgress > div > div {
    background: #3b82f6 !important;
    border-radius: 4px !important;
}

div[data-testid="stDataFrame"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <div class="nav-logo">🛡️</div>
        <span class="nav-title">SentryAI</span>
    </div>
    <span style="font-size:13px;color:#8b949e;">Adaptive Sentiment Analysis & Concept Drift Monitor</span>
</div>
""", unsafe_allow_html=True)

# ── PAGE HEADER ──
st.markdown("""
<div class="page-header">
    <div class="page-title">Sentiment Analytics Dashboard</div>
    <div class="page-subtitle">Powered by RoBERTa Transformer — Real-Time Drift Detection Active</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["📂  Batch Analysis", "✍️  Single Text", "📊  Dashboard"])

# ── TAB 1: Batch ──
with tab1:
    st.markdown('<div class="section-title">📂 Batch Review Analysis</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#8b949e;margin-bottom:12px;">Upload a JSON or CSV file containing product reviews for automatic AI-powered analysis.</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(" ", type=["json", "csv"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".json"):
                data = json.load(uploaded_file)
                reviews = data if isinstance(data, list) else data.get("reviews", [])
                texts = [r if isinstance(r, str) else r.get("text", r.get("review", str(r))) for r in reviews]
            else:
                df_upload = pd.read_csv(uploaded_file)
                col = next((c for c in df_upload.columns if "review" in c.lower() or "text" in c.lower() or "comment" in c.lower()), df_upload.columns[0])
                texts = df_upload[col].dropna().tolist()

            st.markdown(f'<div class="alert-success">✓ Found {len(texts)} reviews — Analysing with RoBERTa AI...</div>', unsafe_allow_html=True)

            results = []
            progress = st.progress(0)
            for i, text in enumerate(texts):
                try:
                    r = requests.post(f"{API_URL}/predict", json={"text": str(text)})
                    res = r.json()
                    results.append({
                        "review": str(text)[:80] + "..." if len(str(text)) > 80 else str(text),
                        "sentiment": res["label"],
                        "confidence": res["score"]
                    })
                except:
                    pass
                progress.progress((i + 1) / len(texts))

            if results:
                df_results = pd.DataFrame(results)
                pos = len(df_results[df_results["sentiment"].str.contains("positive", case=False)])
                neg = len(df_results[df_results["sentiment"].str.contains("negative", case=False)])
                neu = len(df_results[df_results["sentiment"].str.contains("neutral", case=False)])
                total = len(df_results)
                neg_pct = (neg / total) * 100

                st.markdown(f"""
                <div class="stat-row">
                    <div class="stat-card">
                        <div class="stat-label">Total Reviews</div>
                        <div class="stat-value">{total}</div>
                        <span class="badge-blue">Analysed</span>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Positive</div>
                        <div class="stat-value" style="color:#3fb950">{pos}</div>
                        <span class="badge-green">↑ {round(pos/total*100)}%</span>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Negative</div>
                        <div class="stat-value" style="color:#f85149">{neg}</div>
                        <span class="badge-red">↑ {round(neg_pct)}%</span>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Neutral</div>
                        <div class="stat-value" style="color:#8b949e">{neu}</div>
                        <span class="badge-blue">{round(neu/total*100)}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if neg_pct > 40:
                    st.markdown(f'<div class="alert-danger">⚠ Critical: {neg_pct:.1f}% negative reviews — Immediate attention required</div>', unsafe_allow_html=True)
                elif neg_pct > 20:
                    st.markdown(f'<div class="alert-warning">⚠ Warning: {neg_pct:.1f}% of reviews are negative — Monitor closely</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success">✓ Sentiment healthy — Only {neg_pct:.1f}% negative reviews</div>', unsafe_allow_html=True)

                st.dataframe(df_results, use_container_width=True)

                fig = px.pie(df_results, names="sentiment", title="Sentiment Distribution",
                            color_discrete_map={"positive": "#3fb950", "negative": "#f85149", "neutral": "#8b949e"})
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#8b949e", family="Inter"),
                    title_font=dict(color="#f0f6fc", size=14),
                    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#8b949e"))
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.markdown(f'<div class="alert-danger">❌ Error: {e}</div>', unsafe_allow_html=True)

# ── TAB 2: Single Text ──
with tab2:
    st.markdown('<div class="section-title">✍️ Analyse Single Text</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#8b949e;margin-bottom:12px;">Enter any text, review, emoji, or slang — RoBERTa will classify the sentiment instantly.</p>', unsafe_allow_html=True)

    user_input = st.text_area("", height=120, placeholder="Type any sentence, review, emoji or slang here...")

    if st.button("Analyse Sentiment"):
        if user_input.strip() == "":
            st.markdown('<div class="alert-warning">⚠ Please enter some text first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Analysing..."):
                try:
                    response = requests.post(f"{API_URL}/predict", json={"text": user_input})
                    result = response.json()
                    label = result["label"]
                    score = result["score"]

                    if "positive" in label.lower():
                        st.markdown(f'<div class="alert-success">✓ <strong>{label.upper()}</strong> &nbsp;|&nbsp; Confidence: {score}</div>', unsafe_allow_html=True)
                    elif "negative" in label.lower():
                        st.markdown(f'<div class="alert-danger">✗ <strong>{label.upper()}</strong> &nbsp;|&nbsp; Confidence: {score}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="alert-warning">– <strong>{label.upper()}</strong> &nbsp;|&nbsp; Confidence: {score}</div>', unsafe_allow_html=True)
                except:
                    st.markdown('<div class="alert-danger">❌ Cannot connect to backend.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">ℹ️ How SentryAI understands slang & emojis</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#161b22;border:1px solid #21262d;border-radius:10px;padding:16px;font-size:13px;color:#8b949e;line-height:1.7;">
    SentryAI uses a <strong style="color:#c9d1d9;">RoBERTa transformer</strong> pre-trained on millions of social media posts, 
    so it already understands emojis, slang, and informal language (e.g. "fire 🔥", "lowkey bad", "meh").<br><br>
    When new slang appears, drift detectors (<strong style="color:#c9d1d9;">PSI, KS test, JS divergence</strong>) notice the 
    shift in prediction patterns and automatically flag the system for retraining — keeping SentryAI accurate over time.
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3: Dashboard ──
with tab3:
    st.markdown('<div class="section-title">📊 Real-Time Dashboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f6fc;margin-bottom:10px;">🔍 Drift Detection</p>', unsafe_allow_html=True)
        if st.button("Check Drift Now"):
            try:
                response = requests.get(f"{API_URL}/drift-status")
                drift = response.json()
                if drift["drift_detected"]:
                    st.markdown(f'<div class="alert-danger">⚠ {drift["message"]}<br><span style="font-size:12px;">KS: {drift["ks_statistic"]} | p-value: {drift["p_value"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success">✓ {drift["message"]}</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="alert-danger">❌ Cannot connect to backend.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<p style="font-size:13px;font-weight:600;color:#f0f6fc;margin-bottom:10px;">🖥️ System Status</p>', unsafe_allow_html=True)
        try:
            r = requests.get(f"{API_URL}/")
            st.markdown('<p style="font-size:13px;"><span class="status-dot-green"></span><span style="color:#3fb950;font-weight:500;">Backend: Online</span></p>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:12px;color:#8b949e;">🤖 RoBERTa Model: Loaded</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:12px;color:#8b949e;">⚡ FastAPI: Running</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:12px;color:#8b949e;">📊 Drift Monitor: Active</p>', unsafe_allow_html=True)
        except:
            st.markdown('<p style="font-size:13px;"><span class="status-dot-red"></span><span style="color:#f85149;">Backend: Offline</span></p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Prediction History & Trends</div>', unsafe_allow_html=True)

    if "show_history" not in st.session_state:
        st.session_state.show_history = False

    if st.button("Load History & Charts"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history:
        try:
            response = requests.get(f"{API_URL}/history")
            history = response.json()
            if len(history) == 0:
                st.markdown('<div class="alert-warning">📭 No predictions yet. Upload a file or analyse some text first!</div>', unsafe_allow_html=True)
            else:
                df = pd.DataFrame(history)
                st.dataframe(df[["timestamp", "text", "label", "score"]], use_container_width=True)

                fig1 = px.histogram(df, x="label", title="Sentiment Distribution",
                                   color="label",
                                   color_discrete_map={"positive": "#3fb950", "negative": "#f85149", "neutral": "#8b949e"})
                fig1.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(22,27,34,0.8)",
                    font=dict(color="#8b949e", family="Inter"),
                    title_font=dict(color="#f0f6fc", size=14),
                    xaxis=dict(gridcolor="#21262d"),
                    yaxis=dict(gridcolor="#21262d")
                )
                st.plotly_chart(fig1, use_container_width=True)

                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    y=df["score"],
                    mode="lines+markers",
                    line=dict(color="#3b82f6", width=2),
                    marker=dict(color="#3b82f6", size=5),
                    fill="tozeroy",
                    fillcolor="rgba(59,130,246,0.05)"
                ))
                fig2.update_layout(
                    title="Confidence Score Over Time (Drift Indicator)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(22,27,34,0.8)",
                    font=dict(color="#8b949e", family="Inter"),
                    title_font=dict(color="#f0f6fc", size=14),
                    xaxis=dict(gridcolor="#21262d"),
                    yaxis=dict(gridcolor="#21262d")
                )
                st.plotly_chart(fig2, use_container_width=True)
        except:
            st.markdown('<div class="alert-danger">❌ Cannot connect to backend.</div>', unsafe_allow_html=True)