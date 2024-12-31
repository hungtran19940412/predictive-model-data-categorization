# Project File Structure

## Project File Structure
```
predictive-model-data-categorization/
├── data/
│   ├── raw/                # Raw input data
│   ├── processed/          # Cleaned and processed data
│   ├── features/           # Engineered features
│   └── retraining/         # Feedback and retraining data
├── models/
│   ├── trained/            # Trained model versions
│   ├── configs/            # Model configurations
│   └── evaluation/         # Model evaluation results
├── src/
│   ├── preprocessing/      # Data cleaning and validation
│   ├── model/              # Model architecture and training
│   ├── api/                # API endpoints and middleware
│   └── monitoring/         # Monitoring and alerting
├── config/                 # Configuration files
├── deployment/             # Deployment configurations
├── tests/                  # Test cases
├── monitoring/             # Monitoring configurations
└── docs/                   # Project documentation
```

## Key Files and Their Roles

### Data Processing
- `src/preprocessing/text_cleaner.py`: Text cleaning and normalization
- `src/preprocessing/feature_generator.py`: Feature engineering
- `data/features/feature_store/`: Versioned feature storage

### Model Management
- `src/model/architecture.py`: Model definition
- `src/model/trainer.py`: Training logic
- `models/trained/current/`: Current production model

### API Layer
- `src/api/routes/predict.py`: Prediction endpoints
- `src/api/middleware/auth.py`: Authentication
- `src/api/middleware/rate_limit.py`: Rate limiting

### Monitoring
- `src/monitoring/metrics.py`: Custom metrics
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