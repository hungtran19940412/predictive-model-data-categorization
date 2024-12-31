import logging
from typing import Dict, Any, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer

class FeatureGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000)
        self.sentence_encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.scaler = StandardScaler()
        self.logger.info("Feature generator initialized")

    def generate_text_features(self, texts: List[str]) -> Dict[str, Any]:
        """Generate text features using TF-IDF and sentence embeddings"""
        try:
            # TF-IDF features
            tfidf_features = self.tfidf_vectorizer.fit_transform(texts).toarray()
            
            # Sentence embeddings
            embeddings = self.sentence_encoder.encode(texts)
            
            # Combine features
            features = np.hstack([tfidf_features, embeddings])
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            
            return {
                'features': scaled_features,
                'feature_names': self.tfidf_vectorizer.get_feature_names_out().tolist() + ['embedding_' + str(i) for i in range(embeddings.shape[1])]
            }
        except Exception as e:
            self.logger.error(f"Error generating text features: {e}")
            return {}

    def generate_numeric_features(self, numeric_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Generate scaled numeric features"""
        try:
            scaled_features = {}
            for feature_name, values in numeric_data.items():
                scaled_values = self.scaler.fit_transform(np.array(values).reshape(-1, 1))
                scaled_features[feature_name] = scaled_values.flatten()
            return scaled_features
        except Exception as e:
            self.logger.error(f"Error generating numeric features: {e}")
            return {}

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    generator = FeatureGenerator()
    sample_texts = ["This is a sample text", "Another example text"]
    features = generator.generate_text_features(sample_texts)
    print(f"Generated features: {features}")