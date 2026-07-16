from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

from textsummarizer.pipeline.prediction import PredictionPipeline
from textsummarizer.components.analysis_service import (
    DEMO_ARTICLES,
    analyze_article_with_gemini,
    answer_question_with_gemini,
    local_sentiment_analysis,
    local_entity_extraction,
    local_qa_search
)

app = FastAPI(title="Text Summarizer & Sentiment Analysis MLOps Hub")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predicting pipeline
pipeline = PredictionPipeline()

# Pydantic models for request validation
class PreprocessRequest(BaseModel):
    text: str

class AnalyzeRequest(BaseModel):
    text: str
    apiKey: Optional[str] = None
    demoId: Optional[str] = None

class QAHistoryItem(BaseModel):
    role: str
    content: str

class QARequest(BaseModel):
    text: str
    question: str
    chatHistory: List[QAHistoryItem] = []
    apiKey: Optional[str] = None
    demoId: Optional[str] = None

@app.post("/api/preprocess")
def api_preprocess(req: PreprocessRequest):
    try:
        stats = pipeline.run_preprocessing(req.text)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")

@app.post("/api/analyze")
def api_analyze(req: AnalyzeRequest):
    # 1. Handle Demo Mode
    if req.demoId and req.demoId in DEMO_ARTICLES:
        demo_data = DEMO_ARTICLES[req.demoId]
        return {
            "title": demo_data["title"],
            "summary": demo_data["analysis"]["summary"],
            "sentiment": demo_data["analysis"]["sentiment"],
            "entities": demo_data["analysis"]["entities"],
            "isDemo": True
        }
    
    # Check if text is blank
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
        
    # 2. Handle Live Gemini Analysis
    if req.apiKey and req.apiKey.strip():
        result = analyze_article_with_gemini(req.text, req.apiKey)
        return {
            **result,
            "isDemo": False,
            "usingAI": True
        }
        
    # 3. Handle Local Fallback
    local_summary = pipeline.run_extractive_summary(req.text)
    local_sentiment = local_sentiment_analysis(req.text)
    local_entities = local_entity_extraction(req.text)
    
    return {
        "summary": local_summary,
        "sentiment": local_sentiment,
        "entities": local_entities,
        "isDemo": False,
        "usingAI": False,
        "warning": "Running in Local NLP mode. Add Gemini API Key for deep AI analysis."
    }

@app.post("/api/qa")
def api_qa(req: QARequest):
    # 1. Handle Demo Mode Answers
    if req.demoId and req.demoId in DEMO_ARTICLES:
        demo_qa = DEMO_ARTICLES[req.demoId]["qa"]
        question_lower = req.question.lower().strip()
        
        best_match = None
        best_score = 0
        for key_phrase, answer in demo_qa.items():
            key_words = set(key_phrase.split())
            q_words = set(question_lower.split())
            matches = len(key_words.intersection(q_words))
            if matches > best_score:
                best_score = matches
                best_match = answer
                
        if best_score > 0 and best_match:
            return {"answer": best_match}
            
    # Check if text is blank
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Article text cannot be empty.")
        
    # 2. Handle Live Gemini Q&A
    if req.apiKey and req.apiKey.strip():
        history_list = [{"role": item.role, "content": item.content} for item in req.chatHistory]
        result = answer_question_with_gemini(req.text, req.question, history_list, req.apiKey)
        return result
        
    # 3. Handle Local Fallback Search
    local_answer = local_qa_search(req.text, req.question)
    return {"answer": local_answer}

# Serve the static files from the frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: frontend directory not found at {frontend_path}")
