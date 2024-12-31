# AI Data Categorization System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

A production-ready system for automatic data categorization using machine learning, deployed on cloud infrastructure with complete CI/CD pipeline and monitoring capabilities.

## Project Structure

```plaintext
predictive-model-data-categorization/
├── data/
│   ├── raw/
│   │   ├── text_data/           # Raw text files for categorization
│   │   ├── structured_data/     # CSV/JSON files
│   │   └── metadata/            # Data descriptions and schemas
│   ├── processed/
│   │   ├── training_sets/       # Cleaned data for model training
│   │   ├── validation_sets/     # Validation data
│   │   └── test_sets/          # Hold-out test data
│   ├── features/
│   │   ├── text_features/       # Processed text embeddings
│   │   ├── numeric_features/    # Scaled numerical features
│   │   └── feature_store/       # Feature versioning
│   └── retraining/
│       ├── feedback_data/       # User feedback for retraining
│       └── performance_logs/    # Model performance data
├── models/
│   ├── trained/
│   │   ├── current/            # Currently deployed model
│   │   └── archive/            # Previous model versions
│   ├── configs/
│   │   ├── model_params/       # Model hyperparameters
│   │   └── training_configs/   # Training configurations
│   └── evaluation/
│       ├── metrics/            # Performance metrics
│       └── reports/            # Evaluation reports
├── src/
│   ├── preprocessing/
│   │   ├── text_cleaner.py     # Text preprocessing
│   │   ├── data_validator.py   # Data validation
│   │   └── feature_generator.py # Feature engineering
│   ├── model/
│   │   ├── architecture.py     # Model definition
│   │   ├── trainer.py          # Training logic
│   │   └── predictor.py        # Prediction service
│   ├── api/
│   │   ├── routes/
│   │   │   ├── predict.py      # Prediction endpoints
│   │   │   ├── feedback.py     # Feedback collection
│   │   │   └── health.py       # Health checks
│   │   └── middleware/
│   │       ├── auth.py         # Authentication
│   │       └── rate_limit.py   # Rate limiting
│   └── monitoring/
│       ├── metrics.py          # Custom metrics
│       └── alerts.py           # Alert configurations
└── [rest of structure remains the same]
```

## Configuration Examples

### Model Configuration
```yaml
# config/model_config.yaml
model:
  architecture: "transformer"
  embedding_dim: 768
  num_heads: 12
  num_layers: 6
  dropout_rate: 0.1
  max_sequence_length: 512

training:
  batch_size: 32
  learning_rate: 2e-5
  num_epochs: 10
  warmup_steps: 1000
  weight_decay: 0.01
  gradient_clip: 1.0

evaluation:
  metrics:
    - accuracy
    - f1_score
    - precision
    - recall
  threshold: 0.5
```

### API Configuration
```yaml
# config/api_config.yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 60

rate_limiting:
  requests_per_minute: 100
  burst_limit: 20

authentication:
  jwt_secret: "your-secret-key"
  token_expire_minutes: 60
  algorithm: "HS256"

caching:
  ttl: 3600
  max_size: 1000
```

### Monitoring Configuration
```yaml
# config/monitoring_config.yaml
metrics:
  collection_interval: 60
  retention_days: 30

alerts:
  model_performance:
    accuracy_threshold: 0.95
    latency_threshold_ms: 100
    error_rate_threshold: 0.01

  system:
    cpu_threshold: 80
    memory_threshold: 85
    disk_threshold: 90

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## API Routes

### Prediction Endpoint
```python
@router.post("/predict", response_model=PredictionResponse)
async def predict(
    data: PredictionRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(get_current_user)
):
    """
    Predict categories for input data.
    
    Parameters:
    - data: Input text or structured data
    - background_tasks: For async processing
    - token: JWT authentication token
    
    Returns:
    - categories: Predicted categories
    - confidence: Confidence scores
    - model_version: Version of model used
    """
    predictions = await prediction_service.predict(data.text)
    background_tasks.add_task(log_prediction, predictions)
    return predictions
```

### Feedback Collection
```python
@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    feedback: FeedbackRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(get_current_user)
):
    """
    Submit feedback for model predictions.
    
    Parameters:
    - feedback: User feedback data
    - background_tasks: For async processing
    - token: JWT authentication token
    
    Returns:
    - status: Feedback processing status
    - feedback_id: Unique identifier for feedback
    """
    feedback_id = await feedback_service.process_feedback(feedback)
    background_tasks.add_task(update_model_metrics, feedback)
    return {"status": "success", "feedback_id": feedback_id}
```

## Monitoring Metrics

### Model Performance Metrics
```python
class ModelMetrics:
    def __init__(self):
        self.prediction_counter = Counter(
            'model_predictions_total',
            'Total number of predictions made'
        )
        self.prediction_latency = Histogram(
            'model_prediction_latency_seconds',
            'Time taken for predictions',
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0)
        )
        self.accuracy_gauge = Gauge(
            'model_accuracy',
            'Current model accuracy'
        )
        self.error_counter = Counter(
            'model_errors_total',
            'Total number of model errors'
        )

    async def record_prediction(self, latency, success):
        self.prediction_counter.inc()
        self.prediction_latency.observe(latency)
        if not success:
            self.error_counter.inc()
```

### System Metrics
```python
class SystemMetrics:
    def __init__(self):
        self.cpu_usage = Gauge(
            'system_cpu_usage_percent',
            'CPU usage percentage'
        )
        self.memory_usage = Gauge(
            'system_memory_usage_bytes',
            'Memory usage in bytes'
        )
        self.disk_usage = Gauge(
            'system_disk_usage_percent',
            'Disk usage percentage'
        )
        self.request_queue = Gauge(
            'system_request_queue_size',
            'Number of requests in queue'
        )

    async def update_metrics(self):
        self.cpu_usage.set(psutil.cpu_percent())
        self.memory_usage.set(psutil.virtual_memory().used)
        self.disk_usage.set(psutil.disk_usage('/').percent)
```

## Deployment Configuration

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    environment:
      - MODEL_PATH=/app/models/current
      - LOG_LEVEL=INFO
      - METRICS_ENABLED=true
    depends_on:
      - redis
      - prometheus

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
      - prometheus_data:/prometheus

volumes:
  redis_data:
  prometheus_data:
```

## Security Configurations

### Authentication
```python
# src/api/middleware/auth.py
class AuthConfig:
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Rate Limiting
```python
# src/api/middleware/rate_limit.py
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.redis = Redis(host='localhost', port=6379)
    
    async def check_rate_limit(self, user_id: str) -> bool:
        current = await self.redis.incr(f"rate_limit:{user_id}")
        if current == 1:
            await self.redis.expire(f"rate_limit:{user_id}", 60)
        return current <= self.requests_per_minute
```

[Previous sections for License remain unchanged]

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.