import re
import string
from typing import Optional, Dict, Any
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import unicodedata

class TextCleaner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.logger.info("Text cleaner initialized")

    def clean_text(self, text: str) -> Optional[str]:
        """Clean and normalize text data"""
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters and numbers
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Normalize unicode characters
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
            
            # Tokenize and remove stopwords
            tokens = word_tokenize(text)
            filtered_tokens = [word for word in tokens if word not in self.stop_words]
            
            # Lemmatize words
            lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in filtered_tokens]
            
            # Join tokens back into string
            cleaned_text = ' '.join(lemmatized_tokens)
            
            return cleaned_text
        except Exception as e:
            self.logger.error(f"Error cleaning text: {e}")
            return None

    def batch_clean(self, texts: list) -> list:
        """Clean a batch of text documents"""
        return [self.clean_text(text) for text in texts if text is not None]

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    cleaner = TextCleaner()
    sample_text = "This is a sample text with numbers 123 and special characters !@#"
    cleaned_text = cleaner.clean_text(sample_text)
    print(f"Cleaned text: {cleaned_text}")