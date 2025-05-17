import logging
import os
import json
from datetime import datetime
from ..ai_engine import AIEngine
from ..telephony.telephony_service import TelephonyService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CallManager:
    """
    Call Manager that integrates AI Engine with Telephony Service
    to handle calls for the AI Call Center.
    """
    
    def __init__(self, ai_engine=None, telephony_service=None):
        """
        Initialize the Call Manager.
        
        Args:
            ai_engine (AIEngine, optional): AI Engine instance
            telephony_service (TelephonyService, optional): Telephony Service instance
        """
        logger.info("Initializing Call Manager")
        
        # Initialize AI Engine if not provided
        self.ai_engine = ai_engine or AIEngine()
        
        # Initialize Telephony Service if not provided
        self.telephony_service = telephony_service or TelephonyService()
        
        # Load configuration
        self.config = self._load_config()
        
        # Active call sessions
        self.call_sessions = {}
    
    def _load_config(self):
        """Load configuration from environment or config file."""
        config = {
            "max_call_duration": int(os.getenv("MAX_CALL_DURATION", "300")),  # 5 minutes
            "transfer_threshold": float(os.getenv("TRANSFER_THRESHOLD", "0.7")),
            "recording_enabled": os.getenv("RECORDING_ENABLED", "true").lower() == "true",
            "default_flow_type": os.getenv("DEFAULT_FLOW_TYPE", "default"),
            "transfer_numbers": {
                "default": os.getenv("DEFAULT_TRANSFER_NUMBER", "+15551234567"),
                "support": os.getenv("SUPPORT_TRANSFER_NUMBER", "+15552345678"),
                "sales": os.getenv("SALES_TRANSFER_NUMBER", "+15553456789")
            }
        }
        
        # Try to load from config file if it exists
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'call_manager_config.json')
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
    
    def handle_incoming_call(self, call_data):
        """
        Handle an incoming call.
        
        Args:
            call_data (dict): Data about the incoming call
            
        Returns:
            dict: Call session information
        """
        logger.info(f"Handling incoming call from {call_data.get('from')}")
        
        # Create call session
        call_id = call_data.get("call_id") or f"call_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        call_session = {
            "call_id": call_id,
            "direction": "inbound",
            "from": call_data.get("from"),
            "to": call_data.get("to"),
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration": 0,
            "status": "initiated",
            "conversation_id": None,
            "flow_type": call_data.get("flow_type", self.config["default_flow_type"]),
            "recording_url": None,
            "transcript": [],
            "summary": None,
            "next_action": None
        }
        
        self.call_sessions[call_id] = call_session
        
        # Answer the call
        if "call_id" in call_data:
            self.telephony_service.answer_call(call_id)
        
        # Start recording if enabled
        if self.config["recording_enabled"]:
            self.telephony_service.start_recording(call_id)
        
        # Process with AI Engine
        ai_context = {
            "call_id": call_id,
            "direction": "inbound",
            "flow_type": call_session["flow_type"]
        }
        
        # Start conversation with greeting
        conversation_result = self.ai_engine.conversation_manager.start_conversation(
            flow_type=call_session["flow_type"],
            context=ai_context
        )
        
        call_session["conversation_id"] = conversation_result["id"]
        
        # Get initial greeting from conversation history
        greeting = None
        for message in conversation_result["history"]:
            if message["speaker"] == "system":
                greeting = message["text"]
                break
        
        if greeting:
            # Add to transcript
            self._add_to_transcript(call_session, "system", greeting)
            
            # Synthesize speech
            speech_result = self.ai_engine.tts_engine.synthesize(greeting)
            
            # In a real implementation, this would play the audio to the caller
            logger.info(f"Playing greeting to caller: {greeting}")
            
            call_session["next_action"] = {
                "type": "listen",
                "timeout": 5000  # 5 seconds
            }
        
        return call_session
    
    def make_outbound_call(self, phone_number, context=None):
        """
        Make an outbound call.
        
        Args:
            phone_number (str): Phone number to call
            context (dict, optional): Additional context for the call
            
        Returns:
            dict: Call session information
        """
        context = context or {}
        logger.info(f"Making outbound call to {phone_number}")
        
        # Make call via telephony service
        call_result = self.telephony_service.make_call(phone_number)
        
        if "error" in call_result:
            logger.error(f"Error making call: {call_result['error']}")
            return call_result
        
        call_id = call_result["call_id"]
        
        # Create call session
        call_session = {
            "call_id": call_id,
            "direction": "outbound",
            "from": call_result["from"],
            "to": call_result["to"],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration": 0,
            "status": "initiated",
            "conversation_id": None,
            "flow_type": context.get("flow_type", self.config["default_flow_type"]),
            "recording_url": None,
            "transcript": [],
            "summary": None,
            "next_action": None
        }
        
        self.call_sessions[call_id] = call_session
        
        # Start recording if enabled
        if self.config["recording_enabled"]:
            self.telephony_service.start_recording(call_id)
        
        # Process with AI Engine when call is answered
        # In a real implementation, this would be triggered by a webhook
        # For now, we'll simulate it
        
        # Simulate call being answered
        call_session["status"] = "in-progress"
        
        # Process with AI Engine
        ai_context = {
            "call_id": call_id,
            "direction": "outbound",
            "flow_type": call_session["flow_type"]
        }
        
        # Start conversation with greeting
        conversation_result = self.ai_engine.conversation_manager.start_conversation(
            flow_type=call_session["flow_type"],
            context=ai_context
        )
        
        call_session["conversation_id"] = conversation_result["id"]
        
        # Get initial greeting from conversation history
        greeting = None
        for message in conversation_result["history"]:
            if message["speaker"] == "system":
                greeting = message["text"]
                break
        
        if greeting:
            # Add to transcript
            self._add_to_transcript(call_session, "system", greeting)
            
            # Synthesize speech
            speech_result = self.ai_engine.tts_engine.synthesize(greeting)
            
            # In a real implementation, this would play the audio to the caller
            logger.info(f"Playing greeting to caller: {greeting}")
            
            call_session["next_action"] = {
                "type": "listen",
                "timeout": 5000  # 5 seconds
            }
        
        return call_session
    
    def process_speech(self, call_id, audio_data):
        """
        Process speech from a call.
        
        Args:
            call_id (str): ID of the call
            audio_data (bytes): Audio data to process
            
        Returns:
            dict: Processing results
        """
        if call_id not in self.call_sessions:
            logger.error(f"Call session not found: {call_id}")
            return {"error": "Call session not found"}
        
        call_session = self.call_sessions[call_id]
        
        logger.info(f"Processing speech for call {call_id}")
        
        # Transcribe audio
        transcription_result = self.ai_engine.stt_engine.transcribe(audio_data)
        
        if "error" in transcription_result:
            logger.error(f"Error transcribing audio: {transcription_result['error']}")
            return transcription_result
        
        text = transcription_result["text"]
        
        # Add to transcript
        self._add_to_transcript(call_session, "user", text)
        
        # Process with conversation manager
        conversation_id = call_session["conversation_id"]
        flow_type = call_session["flow_type"]
        
        ai_context = {
            "call_id": call_id,
            "conversation_id": conversation_id,
            "flow_type": flow_type
        }
        
        conversation_result = self.ai_engine.conversation_manager.process(
            text=text,
            context=ai_context
        )
        
        # Check if transfer is required
        if conversation_result["transfer_required"]:
            logger.info(f"Transfer required for call {call_id}")
            
            # Get transfer number
            transfer_to = self.config["transfer_numbers"]["default"]
            
            # Transfer call
            transfer_result = self.telephony_service.transfer_call(call_id, transfer_to)
            
            call_session["status"] = "transferred"
            call_session["transfer_to"] = transfer_to
            call_session["transfer_time"] = datetime.now().isoformat()
            
            # Add to transcript
            transfer_message = f"Transferring to a human representative at {transfer_to}."
            self._add_to_transcript(call_session, "system", transfer_message)
            
            # End recording if enabled
            if self.config["recording_enabled"]:
                self.telephony_service.stop_recording(call_id)
            
            return {
                "action": "transfer",
                "transfer_to": transfer_to,
                "message": transfer_message
            }
        
        # Get response
        response = conversation_result["response"]
        
        # Add to transcript
        self._add_to_transcript(call_session, "system", response)
        
        # Synthesize speech
        speech_result = self.ai_engine.tts_engine.synthesize(response)
        
        # In a real implementation, this would play the audio to the caller
        logger.info(f"Playing response to caller: {response}")
        
        # Check if conversation is ending
        if conversation_result["next_state"] == "farewell":
            logger.info(f"Ending call {call_id}")
            
            # End call
            self.end_call(call_id, "completed")
            
            return {
                "action": "end_call",
                "message": response
            }
        
        # Set next action
        call_session["next_action"] = {
            "type": "listen",
            "timeout": 5000  # 5 seconds
        }
        
        return {
            "action": "continue",
            "message": response,
            "next_state": conversation_result["next_state"]
        }
    
    def process_dtmf(self, call_id, digits):
        """
        Process DTMF tones from a call.
        
        Args:
            call_id (str): ID of the call
            digits (str): DTMF digits received
            
        Returns:
            dict: Processing results
        """
        if call_id not in self.call_sessions:
            logger.error(f"Call session not found: {call_id}")
            return {"error": "Call session not found"}
        
        call_session = self.call_sessions[call_id]
        
        logger.info(f"Processing DTMF {digits} for call {call_id}")
        
        # Add to transcript
        self._add_to_transcript(call_session, "user", f"DTMF: {digits}")
        
        # Process with conversation manager
        # In a real implementation, this would handle DTMF-specific logic
        # For now, we'll treat it as text input
        
        conversation_id = call_session["conversation_id"]
        flow_type = call_session["flow_type"]
        
        ai_context = {
            "call_id": call_id,
            "conversation_id": conversation_id,
            "flow_type": flow_type,
            "input_type": "dtmf"
        }
        
        # Convert digits to text representation
        text = f"Pressed {digits}"
        
        conversation_result = self.ai_engine.conversation_manager.process(
            text=text,
            context=ai_context
        )
        
        # Get response
        response = conversation_result["response"]
        
        # Add to transcript
        self._add_to_transcript(call_session, "system", response)
        
        # Synthesize speech
        speech_result = self.ai_engine.tts_engine.synthesize(response)
        
        # In a real implementation, this would play the audio to the caller
        logger.info(f"Playing response to caller: {response}")
        
        # Set next action
        call_session["next_action"] = {
            "type": "listen",
            "timeout": 5000  # 5 seconds
        }
        
        return {
            "action": "continue",
            "message": response,
            "next_state": conversation_result["next_state"]
        }
    
    def end_call(self, call_id, reason=None):
        """
        End a call.
        
        Args:
            call_id (str): ID of the call to end
            reason (str, optional): Reason for ending the call
            
        Returns:
            dict: Final call information
        """
        if call_id not in self.call_sessions:
            logger.error(f"Call session not found: {call_id}")
            return {"error": "Call session not found"}
        
        logger.info(f"Ending call {call_id}")
        
        call_session = self.call_sessions[call_id]
        
        # End recording if enabled
        if self.config["recording_enabled"] and call_session.get("status") != "transferred":
            recording_result = self.telephony_service.stop_recording(call_id)
            if "url" in recording_result.get("recording", {}):
                call_session["recording_url"] = recording_result["recording"]["url"]
        
        # End call via telephony service
        call_result = self.telephony_service.end_call(call_id, reason)
        
        # Update call session
        call_session["status"] = "completed"
        call_session["end_time"] = datetime.now().isoformat()
        call_session["end_reason"] = reason or "normal"
        
        # Calculate duration
        start_time = datetime.fromisoformat(call_session["start_time"])
        end_time = datetime.fromisoformat(call_session["end_time"])
        call_session["duration"] = (end_time - start_time).total_seconds()
        
        # Generate call summary
        call_session["summary"] = self._generate_call_summary(call_session)
        
        return call_session
    
    def get_call_session(self, call_id):
        """
        Get information about a call session.
        
        Args:
            call_id (str): ID of the call
            
        Returns:
            dict: Call session information
        """
        if call_id not in self.call_sessions:
            logger.error(f"Call session not found: {call_id}")
            return {"error": "Call session not found"}
        
        return self.call_sessions[call_id]
    
    def get_active_calls(self):
        """
        Get all active call sessions.
        
        Returns:
            dict: Active call sessions
        """
        active_calls = {}
        for call_id, call_session in self.call_sessions.items():
            if call_session["status"] not in ["completed", "failed", "transferred"]:
                active_calls[call_id] = call_session
        
        return active_calls
    
    def _add_to_transcript(self, call_session, speaker, text):
        """Add a message to the call transcript."""
        message = {
            "speaker": speaker,
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        
        call_session["transcript"].append(message)
    
    def _generate_call_summary(self, call_session):
        """Generate a summary of the call."""
        # In a real implementation, this would use NLP to summarize the transcript
        # For now, we'll create a simple summary
        
        transcript = call_session["transcript"]
        
        if not transcript:
            return "No transcript available."
        
        # Count turns
        user_turns = sum(1 for msg in transcript if msg["speaker"] == "user")
        system_turns = sum(1 for msg in transcript if msg["speaker"] == "system")
        
        # Get duration
        duration_seconds = call_session.get("duration", 0)
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        
        # Create summary
        summary = f"Call lasted {minutes} minutes and {seconds} seconds with {user_turns} user turns and {system_turns} system turns. "
        
        # Add first and last messages
        if len(transcript) > 0:
            summary += f"Started with: \"{transcript[0]['text'][:50]}...\". "
        
        if len(transcript) > 1:
            summary += f"Ended with: \"{transcript[-1]['text'][:50]}...\". "
        
        return summary
