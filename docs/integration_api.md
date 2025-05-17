# Integration API Documentation

## Overview

This document provides comprehensive documentation for the AI Call Center SaaS integration capabilities. The integration system allows the AI Call Center to connect with various third-party services including CRM systems, ERP platforms, and custom webhooks.

## Integration Manager

The Integration Manager provides a unified interface for managing connections to external systems. It supports various integration types and handles authentication, data synchronization, and connection management.

### Supported Integration Types

- **CRM Systems**
  - Salesforce
  - HubSpot

- **ERP Systems**
  - SAP

### API Endpoints

#### Get All Integrations
```
GET /api/integrations/
```
Query Parameters:
- `type` (optional): Filter integrations by type (e.g., "crm", "erp")

#### Add Integration
```
POST /api/integrations/
```
Request Body:
```json
{
  "type": "salesforce",
  "config": {
    "username": "user@example.com",
    "password": "password",
    "security_token": "token",
    "domain": "company.salesforce.com"
  }
}
```

#### Get Integration
```
GET /api/integrations/{integration_id}
```

#### Remove Integration
```
DELETE /api/integrations/{integration_id}
```

#### Test Integration
```
POST /api/integrations/{integration_id}/test
```

#### Sync Data
```
GET /api/integrations/{integration_id}/sync/{data_type}
```
Path Parameters:
- `integration_id`: ID of the integration
- `data_type`: Type of data to sync (e.g., "contacts", "activities")

Query Parameters:
- Various filters depending on data type

#### Get Integration Types
```
GET /api/integrations/types
```

## Webhook System

The Webhook System allows external services to receive notifications about events in the AI Call Center.

### Supported Events

- `call.started`: Triggered when a call begins
- `call.ended`: Triggered when a call ends
- `call.transferred`: Triggered when a call is transferred
- `call.recording.available`: Triggered when a call recording is available
- `call.transcript.available`: Triggered when a call transcript is available
- `contact.created`: Triggered when a contact is created
- `contact.updated`: Triggered when a contact is updated

### API Endpoints

#### Get All Webhooks
```
GET /api/webhooks/
```
Query Parameters:
- `event` (optional): Filter webhooks by event

#### Register Webhook
```
POST /api/webhooks/
```
Request Body:
```json
{
  "url": "https://example.com/webhook",
  "events": ["call.started", "call.ended"],
  "description": "Call notification webhook",
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

#### Get Webhook
```
GET /api/webhooks/{webhook_id}
```

#### Unregister Webhook
```
DELETE /api/webhooks/{webhook_id}
```

#### Get Available Events
```
GET /api/webhooks/events
```

#### Trigger Event (for testing)
```
POST /api/webhooks/trigger
```
Request Body:
```json
{
  "event": "call.started",
  "data": {
    "call_id": "call-123",
    "from": "+15551234567",
    "to": "+15559876543",
    "timestamp": "2025-05-17T13:00:00Z"
  }
}
```

## Security Considerations

- All API endpoints require authentication
- Sensitive configuration data (passwords, tokens) is encrypted at rest
- HTTPS is required for all webhook URLs
- Rate limiting is applied to prevent abuse
- Webhook payloads are signed to verify authenticity

## Implementation Examples

### Registering a Salesforce Integration

```python
import requests

response = requests.post(
    "https://api.example.com/api/integrations/",
    json={
        "type": "salesforce",
        "config": {
            "username": "user@example.com",
            "password": "password",
            "security_token": "token",
            "domain": "company.salesforce.com"
        }
    },
    headers={
        "Authorization": "Bearer YOUR_API_KEY"
    }
)

print(response.json())
```

### Registering a Webhook

```python
import requests

response = requests.post(
    "https://api.example.com/api/webhooks/",
    json={
        "url": "https://example.com/webhook",
        "events": ["call.ended", "call.transcript.available"],
        "description": "Call completion notification",
        "headers": {
            "X-API-Key": "your-webhook-api-key"
        }
    },
    headers={
        "Authorization": "Bearer YOUR_API_KEY"
    }
)

print(response.json())
```

## Error Handling

All API endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (authentication required)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error

Error responses include a JSON body with details:
```json
{
  "success": false,
  "message": "Error message",
  "details": {
    "field": "Specific error for this field"
  }
}
```
