import logging
import json
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConversationManager:
    """
    Conversation Manager that handles the flow of conversation
    for the AI Call Center.
    """
    
    def __init__(self, nlp_engine, sentiment_analyzer):
        """
        Initialize the Conversation Manager.
        
        Args:
            nlp_engine: NLP engine for processing text
            sentiment_analyzer: Sentiment analyzer for detecting emotions
        """
        logger.info("Initializing Conversation Manager")
        
        self.nlp_engine = nlp_engine
        self.sentiment_analyzer = sentiment_analyzer
        
        # Load conversation flows
        self.flows = self._load_flows()
        
        # Active conversations
        self.active_conversations = {}
    
    def _load_flows(self):
        """Load conversation flows from configuration."""
        # In a real implementation, this would load from files or database
        # For now, we'll define some basic flows
        
        flows = {
            "default": {
                "greeting": {
                    "responses": [
                        "Hello! Thank you for calling. How can I assist you today?",
                        "Hi there! How may I help you today?",
                        "Welcome! What can I do for you?"
                    ],
                    "next_states": ["information", "booking", "complaint", "farewell"]
                },
                "information": {
                    "responses": [
                        "I'd be happy to provide that information. What specifically would you like to know?",
                        "I can help with that. Could you please specify what information you're looking for?"
                    ],
                    "next_states": ["information_detail", "booking", "complaint", "farewell"]
                },
                "booking": {
                    "responses": [
                        "I can help you schedule that. When would you like to book it?",
                        "I'd be happy to assist with booking. What date works best for you?"
                    ],
                    "next_states": ["booking_confirmation", "information", "complaint", "farewell"]
                },
                "complaint": {
                    "responses": [
                        "I'm sorry to hear that. Could you please provide more details about the issue?",
                        "I apologize for the inconvenience. Please tell me more about what happened."
                    ],
                    "next_states": ["complaint_resolution", "transfer", "farewell"]
                },
                "farewell": {
                    "responses": [
                        "Thank you for calling. Have a great day!",
                        "Is there anything else I can help you with before we end the call?",
                        "Thank you for your time. Goodbye!"
                    ],
                    "next_states": []  # End of conversation
                },
                "transfer": {
                    "responses": [
                        "I'll connect you with a human representative right away. Please hold.",
                        "I understand you'd like to speak with a person. I'm transferring you now."
                    ],
                    "next_states": []  # End of conversation, transfer to human
                }
            },
            "real_estate": {
                "greeting": {
                    "responses": [
                        "Hello! Thank you for calling our real estate service. How can I assist you today?",
                        "Welcome to our real estate hotline. How may I help you?"
                    ],
                    "next_states": ["property_inquiry", "viewing_schedule", "price_inquiry", "farewell"]
                },
                "property_inquiry": {
                    "responses": [
                        "I'd be happy to tell you about our properties. What area are you interested in?",
                        "We have several properties available. Are you looking for a specific location or type of property?"
                    ],
                    "next_states": ["property_detail", "viewing_schedule", "price_inquiry", "farewell"]
                },
                # Additional states for real estate flow...
            },
            "customer_support": {
                "greeting": {
                    "responses": [
                        "Hello! Thank you for calling customer support. How can I assist you today?",
                        "Welcome to customer support. How may I help you?"
                    ],
                    "next_states": ["issue_report", "account_inquiry", "product_inquiry", "farewell"]
                },
                "issue_report": {
                    "responses": [
                        "I'm sorry to hear you're experiencing an issue. Could you please describe the problem?",
                        "I'd be happy to help resolve your issue. What seems to be the problem?"
                    ],
                    "next_states": ["troubleshooting", "escalation", "farewell"]
                },
                # Additional states for customer support flow...
            }
        }
        
        return flows
    
    def start_conversation(self, conversation_id=None, flow_type="default", context=None):
        """
        Start a new conversation or retrieve an existing one.
        
        Args:
            conversation_id (str, optional): ID of an existing conversation
            flow_type (str): Type of conversation flow to use
            context (dict, optional): Additional context for the conversation
            
        Returns:
            dict: Conversation state
        """
        # If no conversation ID provided, generate a new one
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Check if conversation already exists
        if conversation_id in self.active_conversations:
            return self.active_conversations[conversation_id]
        
        # Use default flow if specified flow doesn't exist
        if flow_type not in self.flows:
            logger.warning(f"Flow type '{flow_type}' not found, using default")
            flow_type = "default"
        
        # Initialize new conversation
        conversation = {
            "id": conversation_id,
            "flow_type": flow_type,
            "state": "greeting",
            "history": [],
            "context": context or {},
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.active_conversations[conversation_id] = conversation
        
        # Generate initial greeting
        greeting = self._get_response(flow_type, "greeting")
        
        # Add to history
        self._add_to_history(conversation, "system", greeting)
        
        return conversation
    
    def process(self, text, context=None, call_history=None):
        """
        Process user input and generate a response.
        
        Args:
            text (str): User input text
            context (dict, optional): Additional context for processing
            call_history (list, optional): Previous call history
            
        Returns:
            dict: Processing results including response and next actions
        """
        context = context or {}
        call_history = call_history or []
        
        # Get or create conversation
        conversation_id = context.get("conversation_id")
        flow_type = context.get("flow_type", "default")
        
        conversation = self.start_conversation(conversation_id, flow_type, context)
        conversation_id = conversation["id"]
        
        # Process text with NLP
        nlp_result = self.nlp_engine.process(text, context)
        
        # Analyze sentiment
        sentiment_result = self.sentiment_analyzer.analyze(text)
        
        # Add user input to history
        self._add_to_history(conversation, "user", text, {
            "intent": nlp_result.get("intent"),
            "sentiment": sentiment_result.get("sentiment")
        })
        
        # Determine next state based on intent
        current_state = conversation["state"]
        intent = nlp_result.get("intent", "unknown")
        
        # Check if we need to transfer to human
        transfer_required = False
        if intent == "transfer" or sentiment_result.get("sentiment") == "negative" and sentiment_result.get("score", 0.5) < 0.2:
            next_state = "transfer"
            transfer_required = True
        else:
            # Get possible next states
            flow = self.flows.get(flow_type, self.flows["default"])
            current_state_info = flow.get(current_state, flow["greeting"])
            next_states = current_state_info.get("next_states", [])
            
            # Map intent to next state
            if intent in next_states:
                next_state = intent
            elif "information" in next_states and intent == "unknown":
                next_state = "information"
            elif len(next_states) > 0:
                next_state = next_states[0]
            else:
                next_state = "farewell"
        
        # Update conversation state
        conversation["state"] = next_state
        conversation["last_updated"] = datetime.now().isoformat()
        
        # Generate response
        response = self._get_response(flow_type, next_state)
        
        # Add response to history
        self._add_to_history(conversation, "system", response)
        
        # Prepare result
        result = {
            "conversation_id": conversation_id,
            "intent": intent,
            "entities": nlp_result.get("entities", {}),
            "sentiment": sentiment_result.get("sentiment"),
            "sentiment_score": sentiment_result.get("score"),
            "response": response,
            "next_state": next_state,
            "transfer_required": transfer_required
        }
        
        return result
    
    def _get_response(self, flow_type, state):
        """Get a response for the given flow type and state."""
        # Get flow
        flow = self.flows.get(flow_type, self.flows["default"])
        
        # Get state info
        state_info = flow.get(state, flow["greeting"])
        
        # Get responses
        responses = state_info.get("responses", ["I'm not sure how to respond to that."])
        
        # Select a response (in a real implementation, this would be more sophisticated)
        import random
        return random.choice(responses)
    
    def _add_to_history(self, conversation, speaker, text, metadata=None):
        """Add a message to the conversation history."""
        metadata = metadata or {}
        
        message = {
            "speaker": speaker,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }
        
        conversation["history"].append(message)
    
    def end_conversation(self, conversation_id):
        """End a conversation and remove it from active conversations."""
        if conversation_id in self.active_conversations:
            conversation = self.active_conversations.pop(conversation_id)
            logger.info(f"Ended conversation: {conversation_id}")
            return conversation
        
        logger.warning(f"Conversation not found: {conversation_id}")
        return None
    
    def get_conversation(self, conversation_id):
        """Get a conversation by ID."""
        return self.active_conversations.get(conversation_id)
    
    def get_active_conversations(self):
        """Get all active conversations."""
        return self.active_conversations
