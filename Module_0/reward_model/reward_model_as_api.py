"""
REWARD MODEL API - FastAPI Endpoint
====================================

A FastAPI service that provides reward model scoring as an HTTP endpoint.

Endpoints:
  - POST /score       - Score a single prompt-response pair
  - POST /rank        - Rank multiple responses for a prompt
  - GET  /health      - Health check
  - GET  /model-info  - Get information about the loaded model

Usage:
  python reward_model_api.py

  Then visit: http://localhost:8000/docs for interactive API documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import uvicorn
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

MODEL_NAME = "OpenAssistant/reward-model-deberta-v3-base"
MAX_LENGTH = 512
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class ScoreRequest(BaseModel):
    """Request model for scoring a single response"""
    prompt: str = Field(..., description="The prompt/question", min_length=1)
    response: str = Field(..., description="The response to score", min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "prompt": "How do I learn Python programming?",
                "response": "Start with basics, practice daily, build projects."
            }
        }


class ScoreResponse(BaseModel):
    """Response model for score endpoint"""
    prompt: str
    response: str
    score: float
    timestamp: str


class RankRequest(BaseModel):
    """Request model for ranking multiple responses"""
    prompt: str = Field(..., description="The prompt/question", min_length=1)
    responses: List[str] = Field(..., description="List of responses to rank", min_items=2)

    class Config:
        schema_extra = {
            "example": {
                "prompt": "How do I make scrambled eggs?",
                "responses": [
                    "Crack eggs, whisk, cook in pan with butter.",
                    "Put eggs in pan.",
                    "Whisk eggs with salt, cook slowly in buttered pan."
                ]
            }
        }


class RankedResponse(BaseModel):
    """Single ranked response"""
    rank: int
    response: str
    score: float


class RankResponse(BaseModel):
    """Response model for rank endpoint"""
    prompt: str
    ranked_responses: List[RankedResponse]
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model: str
    device: str
    timestamp: str


class ModelInfo(BaseModel):
    """Model information"""
    model_name: str
    device: str
    max_length: int
    score_range: str
    loaded_at: str


# ============================================================================
# Initialize FastAPI App
# ============================================================================

app = FastAPI(
    title="Reward Model API",
    description="Score and rank AI responses using a trained reward model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Global Model State
# ============================================================================

class ModelState:
    """Global state to hold the loaded model"""
    tokenizer = None
    model = None
    loaded_at = None


model_state = ModelState()


# ============================================================================
# Startup Event - Load Model
# ============================================================================

@app.on_event("startup")
async def load_model():
    """Load the reward model on startup"""
    logger.info(f"Loading reward model: {MODEL_NAME}")
    logger.info(f"Device: {DEVICE}")

    try:
        # Load tokenizer and model
        model_state.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model_state.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model_state.model.eval()
        model_state.model.to(DEVICE)
        model_state.loaded_at = datetime.now().isoformat()

        logger.info("✓ Model loaded successfully!")

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


# ============================================================================
# Helper Functions
# ============================================================================

def score_single_response(prompt: str, response: str) -> float:
    """
    Score a single prompt-response pair.

    Args:
        prompt: The question/instruction
        response: The response to score

    Returns:
        float: Reward score
    """
    # Combine prompt and response
    text = f"{prompt}\n\n{response}"

    # Tokenize
    inputs = model_state.tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
        padding=True
    )

    # Move to device
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Get score
    with torch.no_grad():
        outputs = model_state.model(**inputs)
        score = outputs.logits[0][0].item()

    return score


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Reward Model API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "score": "POST /score - Score a single response",
            "rank": "POST /rank - Rank multiple responses"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if model_state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return HealthResponse(
        status="healthy",
        model=MODEL_NAME,
        device=DEVICE,
        timestamp=datetime.now().isoformat()
    )


@app.get("/model-info", response_model=ModelInfo, tags=["Info"])
async def get_model_info():
    """Get information about the loaded model"""
    if model_state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return ModelInfo(
        model_name=MODEL_NAME,
        device=DEVICE,
        max_length=MAX_LENGTH,
        score_range="-2.0 to +2.0 (typically)",
        loaded_at=model_state.loaded_at
    )


@app.post("/score", response_model=ScoreResponse, tags=["Scoring"])
async def score_response(request: ScoreRequest):
    """
    Score a single prompt-response pair.

    Returns a reward score where higher values indicate better responses.
    """
    if model_state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Score the response
        score = score_single_response(request.prompt, request.response)

        return ScoreResponse(
            prompt=request.prompt,
            response=request.response,
            score=round(score, 4),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error scoring response: {e}")
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@app.post("/rank", response_model=RankResponse, tags=["Ranking"])
async def rank_responses(request: RankRequest):
    """
    Rank multiple responses for a given prompt.

    Returns responses sorted by score (best first).
    """
    if model_state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Score all responses
        scored_responses = []
        for response in request.responses:
            score = score_single_response(request.prompt, response)
            scored_responses.append((response, score))

        # Sort by score (descending)
        scored_responses.sort(key=lambda x: x[1], reverse=True)

        # Create ranked list
        ranked = [
            RankedResponse(
                rank=rank,
                response=response,
                score=round(score, 4)
            )
            for rank, (response, score) in enumerate(scored_responses, 1)
        ]

        return RankResponse(
            prompt=request.prompt,
            ranked_responses=ranked,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error ranking responses: {e}")
        raise HTTPException(status_code=500, detail=f"Ranking failed: {str(e)}")


# ============================================================================
# Batch Endpoints (Advanced)
# ============================================================================

class BatchScoreRequest(BaseModel):
    """Request model for batch scoring"""
    items: List[ScoreRequest] = Field(..., min_items=1, max_items=100)


class BatchScoreResponse(BaseModel):
    """Response model for batch scoring"""
    results: List[ScoreResponse]
    count: int
    timestamp: str


@app.post("/batch/score", response_model=BatchScoreResponse, tags=["Batch Operations"])
async def batch_score(request: BatchScoreRequest):
    """
    Score multiple prompt-response pairs in batch.

    Maximum 100 items per request.
    """
    if model_state.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        results = []
        for item in request.items:
            score = score_single_response(item.prompt, item.response)
            results.append(
                ScoreResponse(
                    prompt=item.prompt,
                    response=item.response,
                    score=round(score, 4),
                    timestamp=datetime.now().isoformat()
                )
            )

        return BatchScoreResponse(
            results=results,
            count=len(results),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error in batch scoring: {e}")
        raise HTTPException(status_code=500, detail=f"Batch scoring failed: {str(e)}")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Starting Reward Model API Server")
    print("=" * 70)
    print(f"Model: {MODEL_NAME}")
    print(f"Device: {DEVICE}")
    print(f"Max Length: {MAX_LENGTH}")
    print()
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("Health Check: http://localhost:8000/health")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )