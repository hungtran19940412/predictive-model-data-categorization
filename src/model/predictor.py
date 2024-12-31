import logging
import torch
from typing import Dict, Any, List
from transformers import AutoTokenizer
from src.preprocessing.text_cleaner import TextCleaner

class Predictor:
    def __init__(self, model_path: str, model_name: str, num_classes: int, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.logger = logging.getLogger(__name__)
        self.device = device
        self.model = self._load_model(model_path, model_name, num_classes)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.text_cleaner = TextCleaner()
        self.logger.info(f"Initialized Predictor on device: {device}")

    def _load_model(self, model_path: str, model_name: str, num_classes: int):
        """Load trained model"""
        try:
            from src.model.architecture import TransformerClassifier
            model = TransformerClassifier.load(model_name, num_classes, model_path)
            model.to(self.device)
            model.eval()
            return model
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            raise

    def preprocess_text(self, text: str) -> Dict[str, torch.Tensor]:
        """Preprocess text for prediction"""
        try:
            # Clean text
            cleaned_text = self.text_cleaner.clean_text(text)
            
            # Tokenize
            encoding = self.tokenizer(
                cleaned_text,
                max_length=512,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            return {
                'input_ids': encoding['input_ids'].to(self.device),
                'attention_mask': encoding['attention_mask'].to(self.device)
            }
        except Exception as e:
            self.logger.error(f"Error preprocessing text: {e}")
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        """Make prediction for a single text"""
        try:
            with torch.no_grad():
                inputs = self.preprocess_text(text)
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs, dim=1)
                pred = torch.argmax(probs, dim=1)
                
                return {
                    'prediction': pred.item(),
                    'confidence': probs.max().item(),
                    'probabilities': probs.cpu().numpy().tolist()
                }
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            raise

    def batch_predict(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Make predictions for a batch of texts"""
        return [self.predict(text) for text in texts]

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    predictor = Predictor(
        model_path="best_model.pt",
        model_name="bert-base-uncased",
        num_classes=5
    )
    
    sample_text = "This is a sample text for prediction"
    prediction = predictor.predict(sample_text)
    print(f"Prediction: {prediction}")