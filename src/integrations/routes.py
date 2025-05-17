import logging
import os
import json
from flask import Blueprint, request, jsonify
from ..integrations.integration_manager import IntegrationManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Integration Manager
integration_manager = IntegrationManager()

# Create Blueprint
integrations_bp = Blueprint('integrations', __name__)

@integrations_bp.route('/', methods=['GET'])
def get_integrations():
    """Get all integrations."""
    integration_type = request.args.get('type')
    
    integrations = integration_manager.get_integrations(integration_type)
    
    # Format response
    result = {}
    for integration_id, integration in integrations.items():
        result[integration_id] = integration.get_status()
    
    return jsonify(result)

@integrations_bp.route('/', methods=['POST'])
def add_integration():
    """Add a new integration."""
    data = request.json
    
    if not data or 'type' not in data or 'config' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: type, config"
        }), 400
    
    result = integration_manager.add_integration(data['type'], data['config'])
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify(result)

@integrations_bp.route('/<integration_id>', methods=['GET'])
def get_integration(integration_id):
    """Get an integration by ID."""
    integration = integration_manager.get_integration(integration_id)
    
    if not integration:
        return jsonify({
            "success": False,
            "message": f"Integration not found: {integration_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "integration_id": integration_id,
        "status": integration.get_status()
    })

@integrations_bp.route('/<integration_id>', methods=['DELETE'])
def remove_integration(integration_id):
    """Remove an integration."""
    success = integration_manager.remove_integration(integration_id)
    
    if not success:
        return jsonify({
            "success": False,
            "message": f"Integration not found: {integration_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "message": f"Integration removed: {integration_id}"
    })

@integrations_bp.route('/<integration_id>/test', methods=['POST'])
def test_integration(integration_id):
    """Test an integration."""
    result = integration_manager.test_integration(integration_id)
    
    if not result.get('success', False):
        return jsonify(result), 400
    
    return jsonify(result)

@integrations_bp.route('/<integration_id>/sync/<data_type>', methods=['GET'])
def sync_data(integration_id, data_type):
    """Sync data from an integration."""
    filters = request.args.to_dict()
    
    data = integration_manager.sync_data(integration_id, data_type, filters)
    
    return jsonify({
        "success": True,
        "count": len(data),
        "data": data
    })

@integrations_bp.route('/types', methods=['GET'])
def get_integration_types():
    """Get available integration types."""
    return jsonify({
        "success": True,
        "types": list(integration_manager.integration_types.keys())
    })

def register_routes(app):
    """Register routes with the Flask app."""
    app.register_blueprint(integrations_bp, url_prefix='/api/integrations')
