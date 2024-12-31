# Project File Structure

## Project File Structure
```
predictive-model-data-categorization/
├── data/
│   ├── raw/                # Raw input data (text, CSV, JSON)
│   ├── processed/          # Cleaned and processed data
│   ├── features/           # Engineered features (text embeddings, numerical features)
│   └── retraining/         # Feedback and retraining data
├── models/
│   ├── trained/            # Trained model versions (PyTorch models)
│   ├── configs/            # Model configurations (hyperparameters, training configs)
│   └── evaluation/         # Model evaluation results (metrics, reports)
├── src/
│   ├── preprocessing/
│   │   ├── text_cleaner.py     # Text preprocessing using SpaCy
│   │   ├── data_validator.py   # Data validation using Pandas
│   │   └── feature_generator.py # Feature engineering using transformer models
│   ├── model/
│   │   ├── architecture.py     # Model definition using PyTorch
│   │   ├── trainer.py          # Training logic
│   │   └── predictor.py        # Prediction service
│   ├── api/
│   │   ├── routes/
│   │   │   ├── predict.py      # Prediction endpoints using FastAPI
│   │   │   ├── feedback.py     # Feedback collection
│   │   │   └── health.py       # Health checks
│   │   └── middleware/
│   │       ├── auth.py         # Authentication using JWT
│   │       └── rate_limit.py   # Rate limiting using Redis
│   └── monitoring/
│       ├── metrics.py          # Custom metrics using Prometheus
│       └── alerts.py           # Alert configurations
├── config/                     # Configuration files (YAML format)
├── deployment/                 # Deployment configurations (Docker, Kubernetes)
├── tests/                      # Test cases (unit, integration, performance)
├── monitoring/                 # Monitoring configurations (Prometheus, Grafana)
└── docs/                       # Project documentation
```

## Key Files and Their Roles

### Data Processing
- `src/preprocessing/text_cleaner.py`: Text cleaning and normalization using SpaCy
- `src/preprocessing/feature_generator.py`: Feature engineering using transformer models
- `data/features/feature_store/`: Versioned feature storage

### Model Management
- `src/model/architecture.py`: Model definition using PyTorch
- `src/model/trainer.py`: Training logic
- `models/trained/current/`: Current production model

### API Layer
- `src/api/routes/predict.py`: Prediction endpoints using FastAPI
- `src/api/middleware/auth.py`: Authentication using JWT
- `src/api/middleware/rate_limit.py`: Rate limiting using Redis

### Monitoring
- `src/monitoring/metrics.py`: Custom metrics using Prometheus
- `src/monitoring/alerts.py`: Alert configurations
- `monitoring/prometheus/`: Prometheus configurations

### Configuration
- `config/model_config.yaml`: Model hyperparameters
- `config/api_config.yaml`: API settings
- `config/monitoring_config.yaml`: Monitoring settings

## File Connections
1. **Data Flow**
   - Raw data → Preprocessing → Feature engineering → Model prediction
   - Feedback → Retraining → Model versioning

2. **API Flow**
   - Request → Authentication → Rate limiting → Prediction → Response

3. **Monitoring Flow**
   - Metrics collection → Alerting → System health checks

4. **Deployment Flow**
   - CI/CD pipeline → Containerization → Orchestration → Monitoring

## Cross-References
- For detailed application flow, refer to [Application Flow Documentation](App-flow.md)
- For technology stack details, refer to [Tech Stack Documentation](Tech-stack.md)
- For comprehensive project requirements, refer to [Project Requirements Document](PRD.md)