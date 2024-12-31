from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.model.predictor import Predictor
from src.api.middleware.auth import get_current_user
from src.api.middleware.rate_limit import RateLimiter
from fastapi import BackgroundTasks
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class PredictionRequest:
    text: str

class PredictionResponse:
    prediction: int
    confidence: float
    probabilities: list

@router.post("/predict", response_model=PredictionResponse)
async def predict(
    data: PredictionRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(get_current_user),
    rate_limiter: RateLimiter = Depends(RateLimiter)
):
    """Predict categories for input text"""
    try:
        # Check rate limit
        if not await rate_limiter.check_rate_limit(token):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Get predictor instance
        predictor = Predictor(
            model_path="models/trained/current/model.pt",
            model_name="bert-base-uncased",
            num_classes=5
        )
        
        # Make prediction
        prediction = predictor.predict(data.text)
        
        # Log prediction in background
        background_tasks.add_task(log_prediction, prediction, token)
        
        return prediction
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

def log_prediction(prediction: Dict[str, Any], user_id: str):
    """Log prediction results"""
    try:
        # Implement logging logic here
        logger.info(f"User {user_id} prediction: {prediction}")
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="0.0.0.0", port=8000)