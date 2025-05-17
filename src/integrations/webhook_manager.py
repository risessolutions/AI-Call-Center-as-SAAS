import logging
import os
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebhookManager:
    """
    Webhook Manager that handles webhook integrations for the AI Call Center.
    This allows third-party services to receive notifications about call events.
    """
    
    def __init__(self):
        """Initialize the Webhook Manager."""
        logger.info("Initializing Webhook Manager")
        
        # Load configuration
        self.config = self._load_config()
        
        # Registered webhooks
        self.webhooks = {}
    
    def _load_config(self):
        """Load configuration from environment or config file."""
        config = {
            "max_retries": int(os.getenv("WEBHOOK_MAX_RETRIES", "3")),
            "retry_delay": int(os.getenv("WEBHOOK_RETRY_DELAY", "5")),  # seconds
            "timeout": int(os.getenv("WEBHOOK_TIMEOUT", "10")),  # seconds
            "events": [
                "call.started",
                "call.ended",
                "call.transferred",
                "call.recording.available",
                "call.transcript.available",
                "contact.created",
                "contact.updated"
            ]
        }
        
        # Try to load from config file if it exists
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'webhook_config.json')
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
    
    def register_webhook(self, url, events=None, description=None, headers=None):
        """
        Register a new webhook.
        
        Args:
            url (str): URL to send webhook events to
            events (list, optional): List of events to subscribe to
            description (str, optional): Description of the webhook
            headers (dict, optional): Custom headers to include in webhook requests
            
        Returns:
            dict: Webhook information
        """
        logger.info(f"Registering webhook: {url}")
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            logger.error(f"Invalid webhook URL: {url}")
            return {
                "success": False,
                "message": "Invalid webhook URL"
            }
        
        # Validate events
        if events:
            invalid_events = [event for event in events if event not in self.config["events"]]
            if invalid_events:
                logger.error(f"Invalid webhook events: {invalid_events}")
                return {
                    "success": False,
                    "message": f"Invalid events: {', '.join(invalid_events)}"
                }
        else:
            # Subscribe to all events by default
            events = self.config["events"]
        
        # Generate webhook ID
        webhook_id = f"wh_{os.urandom(4).hex()}"
        
        # Create webhook
        webhook = {
            "id": webhook_id,
            "url": url,
            "events": events,
            "description": description or "",
            "headers": headers or {},
            "created_at": datetime.now().isoformat(),
            "last_triggered": None,
            "status": "active"
        }
        
        # Store webhook
        self.webhooks[webhook_id] = webhook
        
        return {
            "success": True,
            "webhook": webhook
        }
    
    def unregister_webhook(self, webhook_id):
        """
        Unregister a webhook.
        
        Args:
            webhook_id (str): ID of the webhook to unregister
            
        Returns:
            bool: Success status
        """
        logger.info(f"Unregistering webhook: {webhook_id}")
        
        if webhook_id not in self.webhooks:
            logger.error(f"Webhook not found: {webhook_id}")
            return False
        
        # Remove webhook
        del self.webhooks[webhook_id]
        
        return True
    
    def get_webhook(self, webhook_id):
        """
        Get a webhook by ID.
        
        Args:
            webhook_id (str): ID of the webhook
            
        Returns:
            dict: Webhook information
        """
        return self.webhooks.get(webhook_id)
    
    def get_webhooks(self, event=None):
        """
        Get all webhooks, optionally filtered by event.
        
        Args:
            event (str, optional): Event to filter by
            
        Returns:
            dict: Webhooks by ID
        """
        if not event:
            return self.webhooks
        
        return {
            webhook_id: webhook
            for webhook_id, webhook in self.webhooks.items()
            if event in webhook["events"]
        }
    
    def trigger_event(self, event, data):
        """
        Trigger an event and send webhooks.
        
        Args:
            event (str): Event name
            data (dict): Event data
            
        Returns:
            dict: Results of webhook deliveries
        """
        logger.info(f"Triggering event: {event}")
        
        if event not in self.config["events"]:
            logger.error(f"Invalid event: {event}")
            return {
                "success": False,
                "message": f"Invalid event: {event}"
            }
        
        # Get webhooks for this event
        webhooks = self.get_webhooks(event)
        
        if not webhooks:
            logger.info(f"No webhooks registered for event: {event}")
            return {
                "success": True,
                "message": f"No webhooks registered for event: {event}"
            }
        
        # Prepare event payload
        payload = {
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Send webhooks
        results = {}
        for webhook_id, webhook in webhooks.items():
            result = self._send_webhook(webhook, payload)
            results[webhook_id] = result
            
            # Update last triggered timestamp
            webhook["last_triggered"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "results": results
        }
    
    def _send_webhook(self, webhook, payload):
        """
        Send a webhook request.
        
        Args:
            webhook (dict): Webhook information
            payload (dict): Webhook payload
            
        Returns:
            dict: Result of webhook delivery
        """
        import requests
        
        url = webhook["url"]
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "AI-Call-Center-Webhook/1.0",
            "X-Webhook-ID": webhook["id"],
            **webhook["headers"]
        }
        
        logger.info(f"Sending webhook to {url}")
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.config["timeout"]
            )
            
            success = 200 <= response.status_code < 300
            
            return {
                "success": success,
                "status_code": response.status_code,
                "response": response.text[:1000] if success else None,
                "error": None if success else response.text[:1000]
            }
            
        except Exception as e:
            logger.error(f"Error sending webhook: {e}")
            
            return {
                "success": False,
                "status_code": None,
                "response": None,
                "error": str(e)
            }
