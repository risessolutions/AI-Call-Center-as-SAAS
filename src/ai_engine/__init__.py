import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIEngine:
    """
    Main AI Engine class that orchestrates all AI capabilities
    for the call center system.
    """
    
    def __init__(self):
        """Initialize the AI Engine with its components."""
        logger.info("Initializing AI Engine")
        
        # Initialize components
        self.nlp_engine = None
        self.tts_engine = None
        self.stt_engine = None
        self.sentiment_analyzer = None
        self.voice_recognizer = None
        self.conversation_manager = None
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components based on configuration
        self._initialize_components()
        
    def _load_config(self):
        """Load configuration from environment or config file."""
        config = {
            "nlp_provider": os.getenv("AI_NLP_PROVIDER", "default"),
            "tts_provider": os.getenv("AI_TTS_PROVIDER", "default"),
            "stt_provider": os.getenv("AI_STT_PROVIDER", "default"),
            "sentiment_provider": os.getenv("AI_SENTIMENT_PROVIDER", "default"),
            "voice_provider": os.getenv("AI_VOICE_PROVIDER", "default"),
            "api_keys": {
                "openai": os.getenv("OPENAI_API_KEY"),
                "google": os.getenv("GOOGLE_API_KEY"),
                "azure": os.getenv("AZURE_API_KEY"),
                "aws": os.getenv("AWS_API_KEY")
            }
        }
        
        # Try to load from config file if it exists
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'ai_config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    # Update config with file values, but don't overwrite env vars
                    for key, value in file_config.items():
                        if key not in config or not config[key]:
                            config[key] = value
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
        
        return config
    
    def _initialize_components(self):
        """Initialize all AI components based on configuration."""
        from .nlp import NLPEngine
        from .tts import TTSEngine
        from .stt import STTEngine
        from .sentiment import SentimentAnalyzer
        from .voice import VoiceRecognizer
        from .conversation import ConversationManager
        
        # Initialize NLP Engine
        self.nlp_engine = NLPEngine(
            provider=self.config["nlp_provider"],
            api_key=self.config["api_keys"].get(self.config["nlp_provider"])
        )
        
        # Initialize TTS Engine
        self.tts_engine = TTSEngine(
            provider=self.config["tts_provider"],
            api_key=self.config["api_keys"].get(self.config["tts_provider"])
        )
        
        # Initialize STT Engine
        self.stt_engine = STTEngine(
            provider=self.config["stt_provider"],
            api_key=self.config["api_keys"].get(self.config["stt_provider"])
        )
        
        # Initialize Sentiment Analyzer
        self.sentiment_analyzer = SentimentAnalyzer(
            provider=self.config["sentiment_provider"],
            api_key=self.config["api_keys"].get(self.config["sentiment_provider"])
        )
        
        # Initialize Voice Recognizer
        self.voice_recognizer = VoiceRecognizer(
            provider=self.config["voice_provider"],
            api_key=self.config["api_keys"].get(self.config["voice_provider"])
        )
        
        # Initialize Conversation Manager
        self.conversation_manager = ConversationManager(
            nlp_engine=self.nlp_engine,
            sentiment_analyzer=self.sentiment_analyzer
        )
        
        logger.info("All AI Engine components initialized successfully")
    
    def process_call(self, call_data):
        """
        Process a call using the AI Engine.
        
        Args:
            call_data (dict): Data about the call including audio, context, etc.
            
        Returns:
            dict: Results of the call processing including transcription,
                  responses, sentiment, and next actions.
        """
        logger.info(f"Processing call: {call_data.get('call_id')}")
        
        results = {
            "call_id": call_data.get("call_id"),
            "processed_at": None,
            "transcription": None,
            "sentiment": None,
            "intent": None,
            "response": None,
            "next_action": None,
            "transfer_required": False
        }
        
        try:
            # Convert speech to text if audio is provided
            if "audio" in call_data:
                results["transcription"] = self.stt_engine.transcribe(call_data["audio"])
                
            # Use existing transcription if provided
            elif "transcription" in call_data:
                results["transcription"] = call_data["transcription"]
            
            # Process the transcription
            if results["transcription"]:
                # Analyze sentiment
                results["sentiment"] = self.sentiment_analyzer.analyze(results["transcription"])
                
                # Process with conversation manager
                conversation_result = self.conversation_manager.process(
                    text=results["transcription"],
                    context=call_data.get("context", {}),
                    call_history=call_data.get("call_history", [])
                )
                
                results.update(conversation_result)
                
                # Generate speech response if needed
                if results["response"] and call_data.get("generate_audio", False):
                    results["audio_response"] = self.tts_engine.synthesize(results["response"])
            
            logger.info(f"Call processing completed for: {call_data.get('call_id')}")
            
        except Exception as e:
            logger.error(f"Error processing call: {e}")
            results["error"] = str(e)
        
        return results
    
    def handle_incoming_call(self, call_data):
        """Handle an incoming call."""
        logger.info(f"Handling incoming call: {call_data.get('call_id')}")
        
        # Add call type to context
        call_data["context"] = call_data.get("context", {})
        call_data["context"]["call_type"] = "inbound"
        
        return self.process_call(call_data)
    
    def make_outbound_call(self, call_data):
        """Make an outbound call."""
        logger.info(f"Making outbound call to: {call_data.get('phone_number')}")
        
        # Add call type to context
        call_data["context"] = call_data.get("context", {})
        call_data["context"]["call_type"] = "outbound"
        
        # In a real implementation, this would initiate the call via telephony service
        # For now, we'll just process the call data
        return self.process_call(call_data)
    
    def get_available_voices(self):
        """Get list of available voices for TTS."""
        return self.tts_engine.get_available_voices()
    
    def get_supported_languages(self):
        """Get list of supported languages."""
        languages = {
            "stt": self.stt_engine.get_supported_languages(),
            "tts": self.tts_engine.get_supported_languages(),
            "nlp": self.nlp_engine.get_supported_languages()
        }
        return languages
