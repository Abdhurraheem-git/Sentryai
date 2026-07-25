import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

API_URL = "https://abdhur-sentryai-backend.hf.space"

st.set_page_config(
    page_title="SentryAI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SentryAI")
st.subheader("Adaptive Sentiment Analysis & Concept Drift Monitor")
st.markdown("---")

with st.expander("ℹ️ How does SentryAI understand slang, emojis & new language trends?"):
    st.markdown("""
    **SentryAI** uses a RoBERTa transformer model pre-trained on millions of real social media posts,
    so it already understands emojis, slang, abbreviations, and informal internet language
    (e.g. "fire 🔥", "lowkey bad", "meh") far better than traditional sentiment models.

    However, language keeps evolving — new slang and trends appear constantly. This is where
    **concept drift detection** comes in:

    1. As new slang/emojis become common, the model's prediction confidence on real data
       starts to **shift** compared to historical patterns.
    2. SentryAI's statistical monitors — **PSI**, **KS test**, and **JS divergence** —
       continuously compare recent predictions against historical data to detect this shift.
    3. When significant drift is detected, the system **flags it and triggers retraining**,
       so the model adapts to new language patterns over time — without manual intervention.

    This combination of a context-aware transformer model + automatic drift detection is what
    allows SentryAI to stay accurate even as online language evolves.
    """)

tab1, tab2, tab3 = st.tabs(["📂 Batch Analysis", "✍️ Single Text", "📊 Dashboard"])

with tab1:
    st.header("Batch Review Analysis")
    st.write("Upload a JSON or CSV file containing product reviews for automatic analysis.")

    uploaded_file = st.file_uploader("Upload reviews file", type=["json", "csv"])

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

            st.success(f"Found {len(texts)} reviews. Analysing...")

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
                st.dataframe(df_results, use_container_width=True)

                col1, col2, col3 = st.columns(3)
                pos = len(df_results[df_results["sentiment"].str.contains("positive", case=False)])
                neg = len(df_results[df_results["sentiment"].str.contains("negative", case=False)])
                neu = len(df_results[df_results["sentiment"].str.contains("neutral", case=False)])

                col1.metric("Positive Reviews", pos)
                col2.metric("Negative Reviews", neg)
                col3.metric("Neutral Reviews", neu)

                neg_pct = (neg / len(df_results)) * 100
                if neg_pct > 40:
                    st.error(f"⚠️ ALERT: {neg_pct:.1f}% of reviews are negative! Immediate attention required.")
                elif neg_pct > 20:
                    st.warning(f"⚠️ WARNING: {neg_pct:.1f}% of reviews are negative.")
                else:
                    st.success(f"✅ Sentiment looks healthy. Only {neg_pct:.1f}% negative reviews.")

                fig = px.pie(df_results, names="sentiment", title="Sentiment Distribution")
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error reading file: {e}")

with tab2:
    st.header("Analyse Single Text")
    user_input = st.text_area("Enter text to analyse:", height=100, placeholder="Type any sentence here...")

    if st.button("Analyse Sentiment"):
        if user_input.strip() == "":
            st.warning("Please enter some text first.")
        else:
            with st.spinner("Analysing..."):
                try:
                    response = requests.post(f"{API_URL}/predict", json={"text": user_input})
                    result = response.json()
                    label = result["label"]
                    score = result["score"]

                    if "positive" in label.lower():
                        st.success(f"Sentiment: **{label}** — Confidence: {score}")
                    elif "negative" in label.lower():
                        st.error(f"Sentiment: **{label}** — Confidence: {score}")
                    else:
                        st.info(f"Sentiment: **{label}** — Confidence: {score}")
                except:
                    st.error("Cannot connect to backend. Make sure FastAPI is running.")

with tab3:
    st.header("Real-Time Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Drift Detection Status")
        if st.button("Check Drift Now"):
            try:
                response = requests.get(f"{API_URL}/drift-status")
                drift = response.json()
                if drift["drift_detected"]:
                    st.error(f"⚠️ {drift['message']}")
                    st.write(f"KS Statistic: {drift['ks_statistic']}")
                    st.write(f"P-Value: {drift['p_value']}")
                else:
                    st.success(f"✅ {drift['message']}")
            except:
                st.error("Cannot connect to backend.")

    with col2:
        st.subheader("System Status")
        try:
            r = requests.get(f"{API_URL}/")
            st.success("✅ Backend: Online")
        except:
            st.error("❌ Backend: Offline")

    st.subheader("Prediction History & Trends")
    if st.button("Load History"):
        try:
            response = requests.get(f"{API_URL}/history")
            history = response.json()
            if len(history) == 0:
                st.info("No predictions yet. Upload a file or analyse some text first!")
            else:
                df = pd.DataFrame(history)
                st.dataframe(df[["timestamp", "text", "label", "score"]], use_container_width=True)

                fig1 = px.histogram(df, x="label", title="Overall Sentiment Distribution", color="label")
                st.plotly_chart(fig1, use_container_width=True)

                fig2 = px.line(df, y="score", title="Confidence Score Over Time (Drift Indicator)")
                st.plotly_chart(fig2, use_container_width=True)
        except:
            st.error("Cannot connect to backend.")