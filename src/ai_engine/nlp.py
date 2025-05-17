import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseNLP(ABC):
    """Base class for NLP providers"""
    
    @abstractmethod
    def process_text(self, text, context=None):
        """Process text to extract intent, entities, and other information"""
        pass
    
    @abstractmethod
    def generate_response(self, intent, entities, context=None):
        """Generate a response based on intent and entities"""
        pass
    
    @abstractmethod
    def get_supported_languages(self):
        """Get list of supported languages"""
        pass

class DefaultNLP(BaseNLP):
    """Default NLP implementation using rule-based approaches"""
    
    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "farewell": ["goodbye", "bye", "see you", "talk to you later"],
            "information": ["what is", "how does", "can you tell me", "i want to know"],
            "booking": ["book", "schedule", "appointment", "reserve"],
            "complaint": ["problem", "issue", "not working", "broken", "complaint"],
            "transfer": ["speak to a human", "talk to a representative", "speak to a manager", "human", "agent"]
        }
    
    def process_text(self, text, context=None):
        """Process text using simple rule-based approach"""
        text = text.lower()
        
        # Default values
        intent = "unknown"
        entities = {}
        confidence = 0.0
        
        # Check for intents
        for intent_name, phrases in self.intents.items():
            for phrase in phrases:
                if phrase in text:
                    intent = intent_name
                    confidence = 0.7  # Simple confidence score
                    break
        
        # Extract basic entities (very simplified)
        if "tomorrow" in text:
            entities["time"] = "tomorrow"
        elif "today" in text:
            entities["time"] = "today"
            
        if "morning" in text:
            entities["time_of_day"] = "morning"
        elif "afternoon" in text:
            entities["time_of_day"] = "afternoon"
        elif "evening" in text:
            entities["time_of_day"] = "evening"
        
        return {
            "intent": intent,
            "entities": entities,
            "confidence": confidence,
            "text": text
        }
    
    def generate_response(self, intent, entities, context=None):
        """Generate a response based on intent and entities"""
        responses = {
            "greeting": "Hello! How can I help you today?",
            "farewell": "Thank you for calling. Have a great day!",
            "information": "I'd be happy to provide that information for you.",
            "booking": "I can help you schedule that appointment.",
            "complaint": "I'm sorry to hear about that issue. Let me help resolve it.",
            "transfer": "I'll connect you with a human representative right away.",
            "unknown": "I'm not sure I understand. Could you please rephrase that?"
        }
        
        response = responses.get(intent, responses["unknown"])
        
        # Customize based on entities
        if intent == "booking" and "time" in entities:
            response = f"I can help you schedule that appointment for {entities['time']}."
            
        return response
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return ["en"]  # English only for the default implementation

class OpenAINLP(BaseNLP):
    """NLP implementation using OpenAI API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            logger.warning("OpenAI API key not provided. OpenAI NLP will not function.")
    
    def process_text(self, text, context=None):
        """Process text using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not provided")
            return {
                "intent": "unknown",
                "entities": {},
                "confidence": 0.0,
                "text": text
            }
        
        try:
            # In a real implementation, this would use the OpenAI API
            # For now, we'll simulate a response
            logger.info(f"Processing text with OpenAI: {text}")
            
            # Simulate intent detection
            intent = "unknown"
            if "hello" in text.lower() or "hi" in text.lower():
                intent = "greeting"
            elif "bye" in text.lower() or "goodbye" in text.lower():
                intent = "farewell"
            elif "book" in text.lower() or "schedule" in text.lower():
                intent = "booking"
            elif "problem" in text.lower() or "issue" in text.lower():
                intent = "complaint"
            elif "human" in text.lower() or "agent" in text.lower():
                intent = "transfer"
            elif "what" in text.lower() or "how" in text.lower():
                intent = "information"
            
            # Simulate entity extraction
            entities = {}
            if "tomorrow" in text.lower():
                entities["time"] = "tomorrow"
            elif "today" in text.lower():
                entities["time"] = "today"
                
            return {
                "intent": intent,
                "entities": entities,
                "confidence": 0.9,  # Higher confidence with OpenAI
                "text": text
            }
            
        except Exception as e:
            logger.error(f"Error processing text with OpenAI: {e}")
            return {
                "intent": "unknown",
                "entities": {},
                "confidence": 0.0,
                "text": text,
                "error": str(e)
            }
    
    def generate_response(self, intent, entities, context=None):
        """Generate a response using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not provided")
            return "I'm sorry, I'm having trouble generating a response right now."
        
        try:
            # In a real implementation, this would use the OpenAI API
            # For now, we'll simulate a response
            logger.info(f"Generating response with OpenAI for intent: {intent}")
            
            # Basic responses based on intent
            responses = {
                "greeting": "Hello! I'm your AI assistant. How can I help you today?",
                "farewell": "Thank you for calling. Have a wonderful day ahead!",
                "information": "I'd be happy to provide that information for you. What specifically would you like to know?",
                "booking": "I can help you schedule that. When would you like to book it?",
                "complaint": "I'm sorry to hear you're experiencing an issue. Let me help resolve that for you.",
                "transfer": "I understand you'd like to speak with a human. I'll connect you with a representative right away.",
                "unknown": "I'm not entirely sure what you're asking for. Could you please provide more details?"
            }
            
            response = responses.get(intent, responses["unknown"])
            
            # Customize based on entities
            if intent == "booking" and "time" in entities:
                response = f"I can help you schedule that for {entities['time']}. What time would work best for you?"
                
            return response
            
        except Exception as e:
            logger.error(f"Error generating response with OpenAI: {e}")
            return "I'm sorry, I'm having trouble generating a response right now."
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return ["en", "es", "fr", "de", "it", "pt", "nl", "ja", "ko", "zh"]

class NLPEngine:
    """
    NLP Engine that provides natural language processing capabilities
    for the AI Call Center.
    """
    
    def __init__(self, provider="default", api_key=None):
        """Initialize the NLP Engine with the specified provider."""
        logger.info(f"Initializing NLP Engine with provider: {provider}")
        
        self.provider = provider
        self.api_key = api_key
        
        # Initialize the appropriate NLP provider
        if provider == "openai":
            self.nlp = OpenAINLP(api_key)
        else:
            logger.info("Using default NLP provider")
            self.nlp = DefaultNLP()
    
    def process(self, text, context=None):
        """
        Process text to extract intent, entities, and other information.
        
        Args:
            text (str): The text to process
            context (dict, optional): Additional context for processing
            
        Returns:
            dict: Results of processing including intent, entities, etc.
        """
        logger.info(f"Processing text: {text[:50]}...")
        return self.nlp.process_text(text, context)
    
    def generate_response(self, intent, entities, context=None):
        """
        Generate a response based on intent and entities.
        
        Args:
            intent (str): The detected intent
            entities (dict): Extracted entities
            context (dict, optional): Additional context for response generation
            
        Returns:
            str: Generated response
        """
        logger.info(f"Generating response for intent: {intent}")
        return self.nlp.generate_response(intent, entities, context)
    
    def get_supported_languages(self):
        """Get list of supported languages."""
        return self.nlp.get_supported_languages()
