import logging
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.nn import CrossEntropyLoss
from transformers import get_linear_schedule_with_warmup
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score
from typing import Dict, Any

class ModelTrainer:
    def __init__(self, model, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.logger = logging.getLogger(__name__)
        self.model = model.to(device)
        self.device = device
        self.logger.info(f"Initialized ModelTrainer on device: {device}")

    def train(self, 
              train_loader: DataLoader, 
              val_loader: DataLoader, 
              epochs: int = 5, 
              learning_rate: float = 2e-5,
              warmup_steps: int = 1000) -> Dict[str, Any]:
        """Train the model"""
        try:
            # Initialize optimizer and scheduler
            optimizer = AdamW(self.model.parameters(), lr=learning_rate)
            total_steps = len(train_loader) * epochs
            scheduler = get_linear_schedule_with_warmup(
                optimizer, 
                num_warmup_steps=warmup_steps,
                num_training_steps=total_steps
            )
            
            # Loss function
            criterion = CrossEntropyLoss()
            
            # Training loop
            best_val_accuracy = 0
            training_history = []
            
            for epoch in range(epochs):
                self.model.train()
                epoch_loss = 0
                
                # Training phase
                for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}/{epochs}"):
                    optimizer.zero_grad()
                    
                    # Move data to device
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['labels'].to(self.device)
                    
                    # Forward pass
                    outputs = self.model(input_ids, attention_mask)
                    loss = criterion(outputs, labels)
                    
                    # Backward pass
                    loss.backward()
                    optimizer.step()
                    scheduler.step()
                    
                    epoch_loss += loss.item()
                
                # Validation phase
                val_metrics = self.evaluate(val_loader)
                
                # Save best model
                if val_metrics['accuracy'] > best_val_accuracy:
                    best_val_accuracy = val_metrics['accuracy']
                    self.model.save("best_model.pt")
                
                # Log metrics
                epoch_metrics = {
                    'epoch': epoch + 1,
                    'train_loss': epoch_loss / len(train_loader),
                    **val_metrics
                }
                training_history.append(epoch_metrics)
                self.logger.info(f"Epoch {epoch + 1} metrics: {epoch_metrics}")
            
            return {
                'training_history': training_history,
                'best_val_accuracy': best_val_accuracy
            }
        except Exception as e:
            self.logger.error(f"Error during training: {e}")
            raise

    def evaluate(self, data_loader: DataLoader) -> Dict[str, float]:
        """Evaluate model performance"""
        self.model.eval()
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for batch in data_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                outputs = self.model(input_ids, attention_mask)
                preds = torch.argmax(outputs, dim=1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        return {
            'accuracy': accuracy_score(all_labels, all_preds),
            'f1_score': f1_score(all_labels, all_preds, average='weighted')
        }

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    from src.model.architecture import TransformerClassifier
    from torch.utils.data import TensorDataset
    
    # Sample data
    input_ids = torch.randint(0, 100, (100, 32))
    attention_mask = torch.ones_like(input_ids)
    labels = torch.randint(0, 5, (100,))
    
    dataset = TensorDataset(input_ids, attention_mask, labels)
    loader = DataLoader(dataset, batch_size=16)
    
    model = TransformerClassifier("bert-base-uncased", num_classes=5)
    trainer = ModelTrainer(model)
    trainer.train(loader, loader, epochs=2)