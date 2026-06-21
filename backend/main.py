from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import numpy as np
import pandas as pd
from scipy import stats
import json
import os
from datetime import datetime
from typing import List

app = FastAPI(title="SentryAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load RoBERTa model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

# Storage for prediction history
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

class TextInput(BaseModel):
    text: str

class BatchInput(BaseModel):
    texts: List[str]

@app.get("/")
def root():
    return {"message": "SentryAI is running"}

@app.post("/predict")
def predict(input: TextInput):
    result = sentiment_pipeline(input.text)[0]
    label = result["label"]
    score = round(result["score"], 4)

    entry = {
        "text": input.text,
        "label": label,
        "score": score,
        "timestamp": datetime.now().isoformat()
    }

    history = load_history()
    history.append(entry)
    save_history(history)

    return {"label": label, "score": score}

@app.post("/predict-batch")
def predict_batch(input: BatchInput):
    """
    Analyse multiple reviews at once (e.g. from a JSON/CSV file of product reviews).
    Runs continuously without needing a human to monitor each one individually.
    """
    results = []
    history = load_history()

    for text in input.texts:
        result = sentiment_pipeline(text)[0]
        label = result["label"]
        score = round(result["score"], 4)

        entry = {
            "text": text,
            "label": label,
            "score": score,
            "timestamp": datetime.now().isoformat()
        }
        history.append(entry)
        results.append({"text": text, "label": label, "score": score})

    save_history(history)

    total = len(results)
    negative_count = sum(1 for r in results if "negative" in r["label"].lower())
    negative_pct = round((negative_count / total) * 100, 2) if total > 0 else 0

    alert = negative_pct > 40
    alert_message = None
    if negative_pct > 40:
        alert_message = f"ALERT: {negative_pct}% of reviews are negative. Immediate attention required."
    elif negative_pct > 20:
        alert_message = f"WARNING: {negative_pct}% of reviews are negative."

    return {
        "results": results,
        "total_reviews": total,
        "negative_percentage": negative_pct,
        "alert": alert,
        "alert_message": alert_message
    }

@app.get("/history")
def get_history():
    return load_history()

@app.get("/drift-status")
def drift_status():
    history = load_history()
    if len(history) < 20:
        return {"drift_detected": False, "message": "Not enough data yet"}

    scores = [h["score"] for h in history]
    mid = len(scores) // 2
    old = scores[:mid]
    new = scores[mid:]

    ks_stat, p_value = stats.ks_2samp(old, new)
    drift_detected = p_value < 0.05

    return {
        "drift_detected": drift_detected,
        "ks_statistic": round(ks_stat, 4),
        "p_value": round(p_value, 4),
        "message": "Drift detected! Model may need retraining." if drift_detected else "No drift detected."
    }