import os
import yaml
import logging
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch
from .preprocessing import preprocess_text
from .monitoring import log_training_metrics

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """Initialize the model trainer with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.model_name = self.config['model']['name']
        self.model_version = self.config['model']['version']
        self.categories = self.config['categories']
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            'bert-base-uncased',
            num_labels=len(self.categories)
        )

    def prepare_data(self, data_path: str):
        """Prepare and preprocess the training data."""
        # Load data
        df = pd.read_csv(data_path)
        
        # Preprocess text
        df['processed_text'] = df['text'].apply(preprocess_text)
        
        # Convert categories to numerical labels
        self.label2id = {label: i for i, label in enumerate(self.categories)}
        df['label'] = df['category'].map(self.label2id)
        
        # Split data
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            df['processed_text'].values,
            df['label'].values,
            test_size=self.config['training']['validation_split'],
            random_state=42
        )
        
        return train_texts, val_texts, train_labels, val_labels

    def train(self, train_data: Dict[str, Any], validation_data: Dict[str, Any]):
        """Train the model with the prepared data."""
        try:
            # Set up training arguments
            training_args = TrainingArguments(
                output_dir=f"models/trained_model/{self.model_name}-{self.model_version}",
                num_train_epochs=self.config['training']['num_epochs'],
                per_device_train_batch_size=self.config['training']['batch_size'],
                per_device_eval_batch_size=self.config['training']['batch_size'],
                learning_rate=self.config['training']['learning_rate'],
                evaluation_strategy="epoch",
                save_strategy="epoch",
                load_best_model_at_end=True,
            )

            # Initialize trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=train_data,
                eval_dataset=validation_data,
            )

            # Train model
            train_result = trainer.train()
            
            # Log metrics
            metrics = train_result.metrics
            log_training_metrics(metrics)
            
            # Save model
            trainer.save_model()
            self.tokenizer.save_pretrained(training_args.output_dir)
            
            logger.info(f"Model training completed. Metrics: {metrics}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error during model training: {str(e)}")
            raise

    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate the model on test data."""
        try:
            trainer = Trainer(model=self.model)
            metrics = trainer.evaluate(test_data)
            log_training_metrics(metrics, prefix="test")
            return metrics
        except Exception as e:
            logger.error(f"Error during model evaluation: {str(e)}")
            raise

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Prepare data
    train_texts, val_texts, train_labels, val_labels = trainer.prepare_data("data/processed/training_data.csv")
    
    # Train model
    train_metrics = trainer.train(train_texts, train_labels)
    
    # Evaluate model
    test_metrics = trainer.evaluate(val_texts, val_labels)
    
    logger.info(f"Training completed. Test metrics: {test_metrics}")
