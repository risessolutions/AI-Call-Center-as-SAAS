import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseSentimentAnalyzer(ABC):
    """Base class for Sentiment Analysis providers"""
    
    @abstractmethod
    def analyze(self, text, options=None):
        """Analyze sentiment of text"""
        pass

class DefaultSentimentAnalyzer(BaseSentimentAnalyzer):
    """Default Sentiment Analysis implementation using rule-based approach"""
    
    def __init__(self):
        # Simple dictionaries of positive and negative words
        self.positive_words = [
            "good", "great", "excellent", "wonderful", "amazing", "fantastic",
            "happy", "pleased", "satisfied", "love", "like", "enjoy", "thank",
            "appreciate", "helpful", "perfect", "best", "better", "awesome"
        ]
        
        self.negative_words = [
            "bad", "terrible", "awful", "horrible", "poor", "disappointing",
            "unhappy", "dissatisfied", "hate", "dislike", "problem", "issue",
            "wrong", "mistake", "error", "fail", "worst", "worse", "annoying",
            "frustrating", "useless", "broken", "complaint", "angry"
        ]
    
    def analyze(self, text, options=None):
        """
        Analyze sentiment using simple word matching.
        In a real implementation, this would use more sophisticated techniques.
        """
        options = options or {}
        text = text.lower()
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        
        # Determine sentiment
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(0.5 + (positive_count - negative_count) * 0.1, 1.0)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = max(0.5 - (negative_count - positive_count) * 0.1, 0.0)
        else:
            sentiment = "neutral"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": positive_count,
            "negative_count": negative_count
        }

class OpenAISentimentAnalyzer(BaseSentimentAnalyzer):
    """Sentiment Analysis implementation using OpenAI API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            logger.warning("OpenAI API key not provided. OpenAI Sentiment Analysis will not function.")
    
    def analyze(self, text, options=None):
        """Analyze sentiment using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not provided")
            return {
                "error": "API key not provided",
                "sentiment": "neutral",
                "score": 0.5
            }
        
        options = options or {}
        
        try:
            # In a real implementation, this would use the OpenAI API
            # For now, we'll simulate a response
            logger.info(f"Analyzing sentiment with OpenAI: {text[:50]}...")
            
            # Simple simulation based on keywords
            text = text.lower()
            
            # Positive keywords
            positive_keywords = ["happy", "great", "excellent", "thank", "appreciate", "love"]
            # Negative keywords
            negative_keywords = ["unhappy", "bad", "terrible", "problem", "issue", "hate"]
            
            # Check for keywords
            positive_matches = sum(1 for word in positive_keywords if word in text)
            negative_matches = sum(1 for word in negative_keywords if word in text)
            
            # Determine sentiment
            if positive_matches > negative_matches:
                sentiment = "positive"
                score = 0.75 + (positive_matches - negative_matches) * 0.05
                score = min(score, 1.0)
            elif negative_matches > positive_matches:
                sentiment = "negative"
                score = 0.25 - (negative_matches - positive_matches) * 0.05
                score = max(score, 0.0)
            else:
                sentiment = "neutral"
                score = 0.5
            
            return {
                "sentiment": sentiment,
                "score": score,
                "details": {
                    "positive_matches": positive_matches,
                    "negative_matches": negative_matches
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment with OpenAI: {e}")
            return {
                "error": str(e),
                "sentiment": "neutral",
                "score": 0.5
            }

class SentimentAnalyzer:
    """
    Sentiment Analysis Engine that provides sentiment analysis capabilities
    for the AI Call Center.
    """
    
    def __init__(self, provider="default", api_key=None):
        """Initialize the Sentiment Analyzer with the specified provider."""
        logger.info(f"Initializing Sentiment Analyzer with provider: {provider}")
        
        self.provider = provider
        self.api_key = api_key
        
        # Initialize the appropriate sentiment analysis provider
        if provider == "openai":
            self.analyzer = OpenAISentimentAnalyzer(api_key)
        else:
            logger.info("Using default Sentiment Analyzer")
            self.analyzer = DefaultSentimentAnalyzer()
    
    def analyze(self, text, options=None):
        """
        Analyze sentiment of text.
        
        Args:
            text (str): The text to analyze
            options (dict, optional): Additional options for analysis
            
        Returns:
            dict: Results of sentiment analysis
        """
        logger.info(f"Analyzing sentiment: {text[:50]}...")
        return self.analyzer.analyze(text, options)
