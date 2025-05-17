import os
import sys
import logging
from flask import Flask, request, jsonify
from src.ai_engine import AIEngine
from src.telephony.telephony_service import TelephonyService
from src.telephony.call_manager import CallManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize AI Engine
ai_engine = AIEngine()

# Initialize Telephony Service
telephony_service = TelephonyService()

# Initialize Call Manager
call_manager = CallManager(ai_engine, telephony_service)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "services": {
            "ai_engine": "up",
            "telephony_service": "up",
            "call_manager": "up"
        }
    })

@app.route('/api/calls/inbound', methods=['POST'])
def handle_inbound_call():
    """Handle inbound call webhook."""
    data = request.json
    
    logger.info(f"Received inbound call: {data}")
    
    # Process inbound call
    result = call_manager.handle_incoming_call(data)
    
    return jsonify(result)

@app.route('/api/calls/outbound', methods=['POST'])
def make_outbound_call():
    """Make outbound call."""
    data = request.json
    
    if not data or 'phone_number' not in data:
        return jsonify({"error": "Phone number is required"}), 400
    
    logger.info(f"Making outbound call to: {data['phone_number']}")
    
    # Make outbound call
    result = call_manager.make_outbound_call(
        data['phone_number'],
        context=data.get('context')
    )
    
    return jsonify(result)

@app.route('/api/calls/<call_id>/speech', methods=['POST'])
def process_speech(call_id):
    """Process speech from a call."""
    if 'audio' not in request.files:
        return jsonify({"error": "Audio file is required"}), 400
    
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    
    logger.info(f"Processing speech for call {call_id}")
    
    # Process speech
    result = call_manager.process_speech(call_id, audio_data)
    
    return jsonify(result)

@app.route('/api/calls/<call_id>/dtmf', methods=['POST'])
def process_dtmf(call_id):
    """Process DTMF tones from a call."""
    data = request.json
    
    if not data or 'digits' not in data:
        return jsonify({"error": "DTMF digits are required"}), 400
    
    logger.info(f"Processing DTMF for call {call_id}: {data['digits']}")
    
    # Process DTMF
    result = call_manager.process_dtmf(call_id, data['digits'])
    
    return jsonify(result)

@app.route('/api/calls/<call_id>', methods=['GET'])
def get_call(call_id):
    """Get call information."""
    logger.info(f"Getting call information for {call_id}")
    
    # Get call session
    result = call_manager.get_call_session(call_id)
    
    return jsonify(result)

@app.route('/api/calls/<call_id>', methods=['DELETE'])
def end_call(call_id):
    """End a call."""
    data = request.json or {}
    
    logger.info(f"Ending call {call_id}")
    
    # End call
    result = call_manager.end_call(call_id, reason=data.get('reason'))
    
    return jsonify(result)

@app.route('/api/calls', methods=['GET'])
def get_active_calls():
    """Get all active calls."""
    logger.info("Getting active calls")
    
    # Get active calls
    result = call_manager.get_active_calls()
    
    return jsonify(result)

@app.route('/api/webhook', methods=['POST'])
def handle_webhook():
    """Handle webhook from telephony provider."""
    data = request.json
    
    logger.info(f"Received webhook: {data}")
    
    # Process webhook
    result = telephony_service.handle_webhook(data)
    
    return jsonify(result)

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run app
    app.run(host='0.0.0.0', port=port)
