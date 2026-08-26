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

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 40%, #0a0a1a 100%);
    min-height: 100vh;
}

/* Animated background particles effect */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: 
        radial-gradient(ellipse at 20% 50%, rgba(120, 40, 200, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 150, 255, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(0, 200, 150, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* Hero header */
.hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
}

.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #7b2ff7, #00d4ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 3s linear infinite;
    text-shadow: none;
    letter-spacing: 4px;
    margin-bottom: 0.5rem;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.hero-subtitle {
    font-size: 1.2rem;
    color: rgba(150, 200, 255, 0.7);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 0.85rem;
    color: #00d4ff;
    letter-spacing: 2px;
    margin: 4px;
}

/* Glass cards */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
}

/* Metric cards */
.metric-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.metric-positive { border-color: rgba(0, 255, 150, 0.3); }
.metric-negative { border-color: rgba(255, 60, 100, 0.3); }
.metric-neutral { border-color: rgba(0, 212, 255, 0.3); }

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
}

.metric-value-positive { color: #00ff96; text-shadow: 0 0 20px rgba(0,255,150,0.5); }
.metric-value-negative { color: #ff3c64; text-shadow: 0 0 20px rgba(255,60,100,0.5); }
.metric-value-neutral { color: #00d4ff; text-shadow: 0 0 20px rgba(0,212,255,0.5); }

.metric-label {
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(150, 200, 255, 0.6);
    margin-top: 0.5rem;
}

/* Alert boxes */
.alert-danger {
    background: rgba(255, 60, 100, 0.1);
    border: 1px solid rgba(255, 60, 100, 0.4);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #ff6b8a;
    font-size: 1rem;
    letter-spacing: 1px;
    margin: 1rem 0;
}

.alert-warning {
    background: rgba(255, 180, 0, 0.1);
    border: 1px solid rgba(255, 180, 0, 0.4);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #ffcc44;
    font-size: 1rem;
    letter-spacing: 1px;
    margin: 1rem 0;
}

.alert-success {
    background: rgba(0, 255, 150, 0.1);
    border: 1px solid rgba(0, 255, 150, 0.4);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #00ff96;
    font-size: 1rem;
    letter-spacing: 1px;
    margin: 1rem 0;
}

/* Section titles */
.section-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #00d4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

/* Status dot */
.status-online {
    display: inline-block;
    width: 10px; height: 10px;
    background: #00ff96;
    border-radius: 50%;
    box-shadow: 0 0 10px #00ff96;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}

/* Streamlit overrides */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.08);
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: rgba(150,200,255,0.6);
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    letter-spacing: 1px;
    padding: 8px 20px;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,47,247,0.2)) !important;
    color: #00d4ff !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(123,47,247,0.15));
    border: 1px solid rgba(0,212,255,0.4);
    border-radius: 10px;
    color: #00d4ff;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    letter-spacing: 2px;
    padding: 0.6rem 2rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.3), rgba(123,47,247,0.3));
    border-color: rgba(0,212,255,0.8);
    box-shadow: 0 0 20px rgba(0,212,255,0.3);
    transform: translateY(-2px);
}

.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 12px !important;
    color: rgba(200,230,255,0.9) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 15px rgba(0,212,255,0.15) !important;
}

.stFileUploader {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(0,212,255,0.3) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.02) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
    border-radius: 10px !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ──
st.markdown("""
<div class="hero">
    <div class="hero-title">🛡️ SentryAI</div>
    <div class="hero-subtitle">Adaptive Sentiment Analysis & Concept Drift Monitor</div>
    <span class="hero-badge">🤖 RoBERTa Powered</span>
    <span class="hero-badge">📊 Real-Time Drift Detection</span>
    <span class="hero-badge">⚡ FastAPI Backend</span>
</div>
""", unsafe_allow_html=True)

# ── SLANG EXPLAINER ──
with st.expander("ℹ️ How does SentryAI understand slang, emojis & new language trends?"):
    st.markdown("""
    **SentryAI** uses a RoBERTa transformer model pre-trained on millions of real social media posts,
    so it already understands emojis, slang, abbreviations, and informal internet language
    (e.g. "fire 🔥", "lowkey bad", "meh") far better than traditional sentiment models.

    However, language keeps evolving. This is where **concept drift detection** comes in:
    1. As new slang/emojis become common, the model's confidence scores **shift** compared to historical patterns.
    2. SentryAI's statistical monitors — **PSI**, **KS test**, and **JS divergence** — detect this shift.
    3. When significant drift is detected, the system **flags it and triggers retraining** automatically.
    """)

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["📂  Batch Analysis", "✍️  Single Text", "📊  Dashboard"])

# ── TAB 1: Batch ──
with tab1:
    st.markdown('<div class="section-title">⚡ Batch Review Analysis</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(150,200,255,0.6);letter-spacing:1px;">Upload a JSON or CSV file containing product reviews for automatic AI analysis.</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload reviews file", type=["json", "csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".json"):
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    reviews = data
                else:
                    reviews = data.get("reviews", [])
                texts = [r if isinstance(r, str) else r.get("text", r.get("review", str(r))) for r in reviews]
            else:
                df_upload = pd.read_csv(uploaded_file)
                col = next((c for c in df_upload.columns if "review" in c.lower() or "text" in c.lower() or "comment" in c.lower()), df_upload.columns[0])
                texts = df_upload[col].dropna().tolist()

            st.markdown(f'<div class="alert-success">✅ Found {len(texts)} reviews — Analysing with RoBERTa AI...</div>', unsafe_allow_html=True)

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

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'''<div class="metric-card metric-positive">
                        <div class="metric-value metric-value-positive">{pos}</div>
                        <div class="metric-label">✅ Positive</div>
                    </div>''', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'''<div class="metric-card metric-negative">
                        <div class="metric-value metric-value-negative">{neg}</div>
                        <div class="metric-label">⚠️ Negative</div>
                    </div>''', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'''<div class="metric-card metric-neutral">
                        <div class="metric-value metric-value-neutral">{neu}</div>
                        <div class="metric-label">➖ Neutral</div>
                    </div>''', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                neg_pct = (neg / len(df_results)) * 100
                if neg_pct > 40:
                    st.markdown(f'<div class="alert-danger">🚨 CRITICAL ALERT: {neg_pct:.1f}% of reviews are negative! Immediate attention required. Consider product quality review.</div>', unsafe_allow_html=True)
                elif neg_pct > 20:
                    st.markdown(f'<div class="alert-warning">⚠️ WARNING: {neg_pct:.1f}% of reviews are negative. Monitor closely.</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success">✅ Sentiment healthy! Only {neg_pct:.1f}% negative reviews detected.</div>', unsafe_allow_html=True)

                st.dataframe(df_results, use_container_width=True)

                fig = px.pie(df_results, names="sentiment", title="Sentiment Distribution",
                            color_discrete_map={"positive": "#00ff96", "negative": "#ff3c64", "neutral": "#00d4ff"})
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="rgba(150,200,255,0.8)", family="Rajdhani"),
                    title_font=dict(color="#00d4ff", size=16),
                    legend=dict(bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.markdown(f'<div class="alert-danger">❌ Error: {e}</div>', unsafe_allow_html=True)

# ── TAB 2: Single Text ──
with tab2:
    st.markdown('<div class="section-title">✍️ Analyse Single Text</div>', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, placeholder="Type any sentence, review, emoji or slang here... 🔥")

    if st.button("⚡ Analyse Sentiment"):
        if user_input.strip() == "":
            st.markdown('<div class="alert-warning">⚠️ Please enter some text first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🤖 RoBERTa is analysing..."):
                try:
                    response = requests.post(f"{API_URL}/predict", json={"text": user_input})
                    result = response.json()
                    label = result["label"]
                    score = result["score"]

                    if "positive" in label.lower():
                        st.markdown(f'<div class="alert-success">😊 Sentiment: <strong>{label.upper()}</strong> — Confidence: {score}</div>', unsafe_allow_html=True)
                    elif "negative" in label.lower():
                        st.markdown(f'<div class="alert-danger">😞 Sentiment: <strong>{label.upper()}</strong> — Confidence: {score}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="alert-warning">😐 Sentiment: <strong>{label.upper()}</strong> — Confidence: {score}</div>', unsafe_allow_html=True)
                except:
                    st.markdown('<div class="alert-danger">❌ Cannot connect to backend. Make sure the API is running.</div>', unsafe_allow_html=True)

# ── TAB 3: Dashboard ──
with tab3:
    st.markdown('<div class="section-title">📊 Real-Time Dashboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        
        st.markdown('<p style="color:#00d4ff;font-size:1.1rem;letter-spacing:2px;text-transform:uppercase;">🔍 Drift Detection</p>', unsafe_allow_html=True)
        if st.button("⚡ Check Drift Now"):
            try:
                response = requests.get(f"{API_URL}/drift-status")
                drift = response.json()
                if drift["drift_detected"]:
                    st.markdown(f'<div class="alert-danger">🚨 {drift["message"]}<br>KS Stat: {drift["ks_statistic"]} | P-Value: {drift["p_value"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-success">✅ {drift["message"]}</div>', unsafe_allow_html=True)
            except:
                st.markdown('<div class="alert-danger">❌ Cannot connect to backend.</div>', unsafe_allow_html=True)
        

    with col2:
        
        st.markdown('<p style="color:#00d4ff;font-size:1.1rem;letter-spacing:2px;text-transform:uppercase;">🖥️ System Status</p>', unsafe_allow_html=True)
        try:
            r = requests.get(f"{API_URL}/")
            st.markdown('<p><span class="status-online"></span><span style="color:#00ff96;letter-spacing:1px;">Backend: ONLINE</span></p>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(150,200,255,0.6);font-size:0.9rem;">🤖 RoBERTa Model: Loaded<br>⚡ FastAPI: Running<br>📊 Drift Monitor: Active</p>', unsafe_allow_html=True)
        except:
            st.markdown('<p style="color:#ff3c64;">● Backend: OFFLINE</p>', unsafe_allow_html=True)
        

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Prediction History & Trends</div>', unsafe_allow_html=True)

    if "show_history" not in st.session_state:
        st.session_state.show_history = False

    if st.button("📊 Load History & Charts"):
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

                fig1 = px.histogram(df, x="label", title="Overall Sentiment Distribution",
                                   color="label",
                                   color_discrete_map={"positive": "#00ff96", "negative": "#ff3c64", "neutral": "#00d4ff"})
                fig1.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0.2)",
                    font=dict(color="rgba(150,200,255,0.8)", family="Rajdhani"),
                    title_font=dict(color="#00d4ff", size=16),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                )
                st.plotly_chart(fig1, use_container_width=True)

                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    y=df["score"],
                    mode="lines+markers",
                    line=dict(color="#00d4ff", width=2),
                    marker=dict(color="#7b2ff7", size=6),
                    fill="tozeroy",
                    fillcolor="rgba(0,212,255,0.05)"
                ))
                fig2.update_layout(
                    title="Confidence Score Over Time (Drift Indicator)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0.2)",
                    font=dict(color="rgba(150,200,255,0.8)", family="Rajdhani"),
                    title_font=dict(color="#00d4ff", size=16),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
                )
                st.plotly_chart(fig2, use_container_width=True)
        except:
            st.markdown('<div class="alert-danger">❌ Cannot connect to backend.</div>', unsafe_allow_html=True)