from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from .routes import categorization, models, feedback
from .middleware.auth import get_current_user
from .middleware.rate_limiter import RateLimiter
from .middleware.logging import LoggingMiddleware

app = FastAPI(
    title="AI Data Categorization System",
    description="A production-ready system for automatic data categorization using machine learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
rate_limiter = RateLimiter()
app.add_middleware(rate_limiter)

# Add Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include routers
app.include_router(
    categorization.router,
    prefix="/api/v1",
    tags=["categorization"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    models.router,
    prefix="/api/v1/models",
    tags=["models"]
)
app.include_router(
    feedback.router,
    prefix="/api/v1/feedback",
    tags=["feedback"]
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
