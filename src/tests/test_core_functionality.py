import unittest
import json
import os
from unittest.mock import MagicMock, patch
from src.ai_engine import AIEngine
from src.telephony.telephony_service import TelephonyService
from src.telephony.call_manager import CallManager

class TestAICallCenter(unittest.TestCase):
    """Test cases for AI Call Center core functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock AI Engine
        self.ai_engine = MagicMock(spec=AIEngine)
        
        # Mock conversation manager
        self.ai_engine.conversation_manager = MagicMock()
        self.ai_engine.conversation_manager.start_conversation.return_value = {
            "id": "conv-123",
            "history": [
                {"speaker": "system", "text": "Hello! How can I help you today?"}
            ]
        }
        self.ai_engine.conversation_manager.process.return_value = {
            "conversation_id": "conv-123",
            "intent": "information",
            "entities": {},
            "sentiment": "positive",
            "sentiment_score": 0.8,
            "response": "I'd be happy to provide that information for you.",
            "next_state": "information",
            "transfer_required": False
        }
        
        # Mock TTS Engine
        self.ai_engine.tts_engine = MagicMock()
        self.ai_engine.tts_engine.synthesize.return_value = {
            "audio_data": b"SIMULATED_AUDIO_DATA",
            "format": "wav",
            "voice_id": "default",
            "text": "Hello! How can I help you today?"
        }
        
        # Mock STT Engine
        self.ai_engine.stt_engine = MagicMock()
        self.ai_engine.stt_engine.transcribe.return_value = {
            "text": "I need information about your services.",
            "confidence": 0.9,
            "language": "en-US"
        }
        
        # Mock Telephony Service
        self.telephony_service = MagicMock(spec=TelephonyService)
        self.telephony_service.make_call.return_value = {
            "call_id": "call-123",
            "direction": "outbound",
            "from": "+15551234567",
            "to": "+15559876543",
            "status": "initiated"
        }
        
        # Initialize Call Manager with mocks
        self.call_manager = CallManager(self.ai_engine, self.telephony_service)
    
    def test_handle_incoming_call(self):
        """Test handling an incoming call."""
        call_data = {
            "call_id": "call-123",
            "from": "+15559876543",
            "to": "+15551234567"
        }
        
        result = self.call_manager.handle_incoming_call(call_data)
        
        # Verify call was answered
        self.telephony_service.answer_call.assert_called_once_with("call-123")
        
        # Verify conversation was started
        self.ai_engine.conversation_manager.start_conversation.assert_called_once()
        
        # Verify TTS was called
        self.ai_engine.tts_engine.synthesize.assert_called_once()
        
        # Verify result
        self.assertEqual(result["call_id"], "call-123")
        self.assertEqual(result["status"], "initiated")
        self.assertEqual(result["direction"], "inbound")
        self.assertIsNotNone(result["conversation_id"])
    
    def test_make_outbound_call(self):
        """Test making an outbound call."""
        result = self.call_manager.make_outbound_call("+15559876543")
        
        # Verify call was made
        self.telephony_service.make_call.assert_called_once_with("+15559876543")
        
        # Verify conversation was started
        self.ai_engine.conversation_manager.start_conversation.assert_called_once()
        
        # Verify TTS was called
        self.ai_engine.tts_engine.synthesize.assert_called_once()
        
        # Verify result
        self.assertEqual(result["call_id"], "call-123")
        self.assertEqual(result["status"], "in-progress")
        self.assertEqual(result["direction"], "outbound")
        self.assertIsNotNone(result["conversation_id"])
    
    def test_process_speech(self):
        """Test processing speech from a call."""
        # First create a call session
        call_data = {
            "call_id": "call-123",
            "from": "+15559876543",
            "to": "+15551234567"
        }
        
        self.call_manager.handle_incoming_call(call_data)
        
        # Now process speech
        audio_data = b"SIMULATED_AUDIO_DATA"
        result = self.call_manager.process_speech("call-123", audio_data)
        
        # Verify STT was called
        self.ai_engine.stt_engine.transcribe.assert_called_once_with(audio_data)
        
        # Verify conversation was processed
        self.ai_engine.conversation_manager.process.assert_called_once()
        
        # Verify TTS was called
        self.assertEqual(self.ai_engine.tts_engine.synthesize.call_count, 2)
        
        # Verify result
        self.assertEqual(result["action"], "continue")
        self.assertEqual(result["message"], "I'd be happy to provide that information for you.")
        self.assertEqual(result["next_state"], "information")
    
    def test_end_call(self):
        """Test ending a call."""
        # First create a call session
        call_data = {
            "call_id": "call-123",
            "from": "+15559876543",
            "to": "+15551234567"
        }
        
        self.call_manager.handle_incoming_call(call_data)
        
        # Now end the call
        result = self.call_manager.end_call("call-123", "user_hangup")
        
        # Verify call was ended
        self.telephony_service.end_call.assert_called_once_with("call-123", "user_hangup")
        
        # Verify result
        self.assertEqual(result["call_id"], "call-123")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["end_reason"], "user_hangup")
        self.assertIsNotNone(result["summary"])

if __name__ == '__main__':
    unittest.main()
