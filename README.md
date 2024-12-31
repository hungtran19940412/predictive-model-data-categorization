# AI Data Categorization System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=flat&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

A production-ready system for automatic data categorization using machine learning, deployed on cloud infrastructure with a complete CI/CD pipeline and monitoring capabilities. This system supports multiple data formats (text, CSV, JSON) and provides real-time predictions with model version control and performance monitoring.

---

## Project Structure

The project is organized as follows:

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
│   │   └── test_sets/           # Hold-out test data
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
│   │   ├── text_cleaner.py     # Text preprocessing (using SpaCy)
│   │   ├── data_validator.py   # Data validation (using Pandas)
│   │   └── feature_generator.py # Feature engineering
│   ├── model/
│   │   ├── architecture.py     # Model definition (using PyTorch)
│   │   ├── trainer.py          # Training logic
│   │   └── predictor.py        # Prediction service
│   ├── api/
│   │   ├── routes/
│   │   │   ├── predict.py      # Prediction endpoints
│   │   │   ├── feedback.py     # Feedback collection
│   │   │   └── health.py       # Health checks
│   │   └── middleware/
│   │       ├── auth.py         # Authentication (JWT)
│   │       └── rate_limit.py   # Rate limiting (Redis)
│   └── monitoring/
│       ├── metrics.py          # Custom metrics (Prometheus)
│       └── alerts.py           # Alert configurations
├── config/                     # Configuration files
├── deployment/                 # Deployment configurations (Docker, Kubernetes)
├── tests/                      # Test cases
├── monitoring/                 # Monitoring configurations (Prometheus, Grafana)
└── docs/                       # Project documentation
```

---

## Key Features

### Core Features
- **Automatic Data Categorization**: Categorizes text and structured data using transformer-based models.
- **Multi-Format Data Support**: Handles text, CSV, and JSON inputs.
- **Real-Time Predictions**: Provides low-latency predictions via RESTful API.
- **Model Version Control**: Tracks and manages multiple model versions.
- **Performance Monitoring**: Tracks model and system performance using Prometheus and Grafana.

### Development Features
- **Automated Testing**: Unit, integration, and performance tests.
- **CI/CD Pipeline**: Automated builds, tests, and deployments using GitHub Actions.
- **Containerized Deployment**: Deployed using Docker and orchestrated with Kubernetes.
- **Monitoring and Alerting**: Real-time metrics and alerts for system health and model performance.

---

## Technology Stack

### Core Technologies
- **Programming Language**: Python 3.8+
- **Web Framework**: FastAPI
- **Machine Learning**: PyTorch, Transformers
- **Data Processing**: Pandas, NumPy, SpaCy
- **Database**: Redis (caching), PostgreSQL (metadata storage)
- **Monitoring**: Prometheus, Grafana
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

For more details, refer to the [Tech Stack Documentation](Tech-stack.md).

---

## Application Flow

The system follows a structured flow for data processing, model prediction, and feedback collection:

1. **Data Input**: Accepts raw data (text, CSV, JSON) and validates it.
2. **Preprocessing**: Cleans and normalizes text data using SpaCy.
3. **Feature Engineering**: Generates text embeddings and numerical features.
4. **Model Prediction**: Makes predictions using the current model version.
5. **Feedback Collection**: Collects user feedback for model improvement.
6. **Model Retraining**: Retrains the model using feedback data.
7. **Monitoring**: Tracks model performance and system health using Prometheus and Grafana.

For a detailed flowchart, refer to the [Application Flow Documentation](App-flow.md).

---

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

---

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

---

## Deployment

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

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.