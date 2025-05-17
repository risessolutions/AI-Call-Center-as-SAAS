import logging
import os
import json
from flask import Blueprint, request, jsonify
from ..integrations.webhook_manager import WebhookManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Webhook Manager
webhook_manager = WebhookManager()

# Create Blueprint
webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/', methods=['GET'])
def get_webhooks():
    """Get all webhooks."""
    event = request.args.get('event')
    
    webhooks = webhook_manager.get_webhooks(event)
    
    return jsonify({
        "success": True,
        "count": len(webhooks),
        "webhooks": webhooks
    })

@webhooks_bp.route('/', methods=['POST'])
def register_webhook():
    """Register a new webhook."""
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({
            "success": False,
            "message": "URL is required"
        }), 400
    
    result = webhook_manager.register_webhook(
        data['url'],
        events=data.get('events'),
        description=data.get('description'),
        headers=data.get('headers')
    )
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify(result)

@webhooks_bp.route('/<webhook_id>', methods=['GET'])
def get_webhook(webhook_id):
    """Get a webhook by ID."""
    webhook = webhook_manager.get_webhook(webhook_id)
    
    if not webhook:
        return jsonify({
            "success": False,
            "message": f"Webhook not found: {webhook_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "webhook": webhook
    })

@webhooks_bp.route('/<webhook_id>', methods=['DELETE'])
def unregister_webhook(webhook_id):
    """Unregister a webhook."""
    success = webhook_manager.unregister_webhook(webhook_id)
    
    if not success:
        return jsonify({
            "success": False,
            "message": f"Webhook not found: {webhook_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "message": f"Webhook unregistered: {webhook_id}"
    })

@webhooks_bp.route('/events', methods=['GET'])
def get_events():
    """Get available webhook events."""
    return jsonify({
        "success": True,
        "events": webhook_manager.config["events"]
    })

@webhooks_bp.route('/trigger', methods=['POST'])
def trigger_event():
    """Trigger a webhook event."""
    data = request.json
    
    if not data or 'event' not in data or 'data' not in data:
        return jsonify({
            "success": False,
            "message": "Event and data are required"
        }), 400
    
    result = webhook_manager.trigger_event(data['event'], data['data'])
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify(result)

def register_routes(app):
    """Register routes with the Flask app."""
    app.register_blueprint(webhooks_bp, url_prefix='/api/webhooks')
