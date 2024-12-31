import logging
import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig

class TransformerClassifier(nn.Module):
    def __init__(self, model_name: str, num_classes: int, dropout_rate: float = 0.1):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = AutoConfig.from_pretrained(model_name)
        self.transformer = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(dropout_rate)
        self.classifier = nn.Linear(self.config.hidden_size, num_classes)
        self.logger.info(f"Initialized TransformerClassifier with {model_name}")

    def forward(self, input_ids, attention_mask=None):
        try:
            # Get transformer outputs
            outputs = self.transformer(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            
            # Get pooled output
            pooled_output = outputs.last_hidden_state[:, 0, :]
            
            # Apply dropout and classification
            pooled_output = self.dropout(pooled_output)
            logits = self.classifier(pooled_output)
            
            return logits
        except Exception as e:
            self.logger.error(f"Error in forward pass: {e}")
            raise

    def save(self, path: str):
        """Save model to file"""
        try:
            torch.save(self.state_dict(), path)
            self.logger.info(f"Model saved to {path}")
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            raise

    @classmethod
    def load(cls, model_name: str, num_classes: int, path: str):
        """Load model from file"""
        try:
            model = cls(model_name, num_classes)
            model.load_state_dict(torch.load(path))
            model.eval()
            return model
        except Exception as e:
            logging.getLogger(__name__).error(f"Error loading model: {e}")
            raise

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    model = TransformerClassifier("bert-base-uncased", num_classes=5)
    sample_input = torch.randint(0, 100, (1, 32))
    output = model(sample_input)
    print(f"Model output shape: {output.shape}")