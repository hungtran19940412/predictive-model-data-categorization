from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from ..schemas.request import CategoryRequest
from ..schemas.response import CategoryResponse
from ..services.model import ModelService
from ..services.monitoring import MonitoringService

router = APIRouter()
model_service = ModelService()
monitoring_service = MonitoringService()

@router.post("/predict", response_model=CategoryResponse)
async def predict_category(request: CategoryRequest) -> CategoryResponse:
    """
    Predict categories for input data using the trained model.
    """
    try:
        # Log prediction request
        monitoring_service.log_prediction_request(request)
        
        # Get model predictions
        predictions = model_service.predict(request.data)
        
        # Log prediction results
        monitoring_service.log_prediction_result(predictions)
        
        return CategoryResponse(
            categories=predictions["categories"],
            confidence_scores=predictions["confidence_scores"],
            model_version=model_service.get_model_version()
        )
    except Exception as e:
        monitoring_service.log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-predict")
async def batch_predict(requests: List[CategoryRequest]) -> List[CategoryResponse]:
    """
    Batch prediction endpoint for multiple data points.
    """
    try:
        results = []
        for request in requests:
            prediction = await predict_category(request)
            results.append(prediction)
        return results
    except Exception as e:
        monitoring_service.log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_available_categories() -> Dict[str, Any]:
    """
    Get list of available categories and their descriptions.
    """
    try:
        categories = model_service.get_categories()
        return {
            "categories": categories,
            "total": len(categories),
            "model_version": model_service.get_model_version()
        }
    except Exception as e:
        monitoring_service.log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
