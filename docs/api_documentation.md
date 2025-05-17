# AI Call Center SaaS - API Documentation

## Overview

This document provides comprehensive documentation for the AI Call Center SaaS API. The API allows developers to integrate our AI call center capabilities into their own applications and systems.

## Base URL

All API requests should be made to:

```
https://api.your-domain.com/v1
```

## Authentication

### API Keys

All API requests require authentication using API keys. To obtain an API key:

1. Log in to your AI Call Center SaaS account
2. Navigate to Settings > API
3. Generate a new API key

Include your API key in all requests using the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

### Rate Limiting

API requests are limited to 100 requests per minute per API key. If you exceed this limit, you'll receive a 429 Too Many Requests response.

## Endpoints

### Calls

#### Create a Call

```
POST /calls
```

Create a new outbound call.

**Request Body:**

```json
{
  "phone": "+15551234567",
  "contactId": "60a2e7f3b9c1a83e94d8f2a1",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "variables": {
    "companyName": "Acme Inc",
    "productName": "Premium Widget"
  },
  "scheduled": "2025-05-20T15:30:00Z",
  "callerId": "+15559876543"
}
```

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2c3",
  "status": "scheduled",
  "phone": "+15551234567",
  "contactId": "60a2e7f3b9c1a83e94d8f2a1",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "scheduled": "2025-05-20T15:30:00Z",
  "callerId": "+15559876543",
  "createdAt": "2025-05-17T14:25:00Z"
}
```

#### Get Call Details

```
GET /calls/{id}
```

Retrieve details for a specific call.

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2c3",
  "status": "completed",
  "phone": "+15551234567",
  "contactId": "60a2e7f3b9c1a83e94d8f2a1",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "scheduled": "2025-05-20T15:30:00Z",
  "startedAt": "2025-05-20T15:30:02Z",
  "endedAt": "2025-05-20T15:33:45Z",
  "duration": 223,
  "recording": "https://api.your-domain.com/recordings/60a2e7f3b9c1a83e94d8f2c3.mp3",
  "transcript": "https://api.your-domain.com/transcripts/60a2e7f3b9c1a83e94d8f2c3.json",
  "outcome": "successful",
  "notes": "Customer expressed interest in the premium plan",
  "callerId": "+15559876543",
  "createdAt": "2025-05-17T14:25:00Z"
}
```

#### List Calls

```
GET /calls
```

Retrieve a list of calls with optional filtering.

**Query Parameters:**

- `status` - Filter by call status (scheduled, in-progress, completed, failed)
- `contactId` - Filter by contact ID
- `campaignId` - Filter by campaign ID
- `startDate` - Filter by start date (ISO format)
- `endDate` - Filter by end date (ISO format)
- `page` - Page number for pagination (default: 1)
- `limit` - Number of results per page (default: 20, max: 100)

**Response:**

```json
{
  "data": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2c3",
      "status": "completed",
      "phone": "+15551234567",
      "contactId": "60a2e7f3b9c1a83e94d8f2a1",
      "templateId": "60a2e7f3b9c1a83e94d8f2b2",
      "scheduled": "2025-05-20T15:30:00Z",
      "duration": 223,
      "outcome": "successful",
      "createdAt": "2025-05-17T14:25:00Z"
    },
    // More calls...
  ],
  "pagination": {
    "total": 157,
    "page": 1,
    "limit": 20,
    "pages": 8
  }
}
```

#### Cancel Call

```
POST /calls/{id}/cancel
```

Cancel a scheduled call.

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2c3",
  "status": "cancelled",
  "message": "Call successfully cancelled"
}
```

### Campaigns

#### Create a Campaign

```
POST /campaigns
```

Create a new call campaign.

**Request Body:**

```json
{
  "name": "Summer Promotion",
  "description": "Outreach for summer sale",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "contacts": [
    "60a2e7f3b9c1a83e94d8f2a1",
    "60a2e7f3b9c1a83e94d8f2a2"
  ],
  "contactListIds": [
    "60a2e7f3b9c1a83e94d8f2d1"
  ],
  "schedule": {
    "startDate": "2025-05-20T09:00:00Z",
    "endDate": "2025-05-25T17:00:00Z",
    "timeZone": "America/New_York",
    "callHours": {
      "start": "09:00",
      "end": "17:00"
    },
    "daysOfWeek": [1, 2, 3, 4, 5]
  },
  "callSettings": {
    "maxConcurrentCalls": 10,
    "callerId": "+15559876543",
    "retrySettings": {
      "maxAttempts": 3,
      "retryInterval": 60
    }
  }
}
```

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2e1",
  "name": "Summer Promotion",
  "description": "Outreach for summer sale",
  "status": "scheduled",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "totalContacts": 152,
  "schedule": {
    "startDate": "2025-05-20T09:00:00Z",
    "endDate": "2025-05-25T17:00:00Z",
    "timeZone": "America/New_York",
    "callHours": {
      "start": "09:00",
      "end": "17:00"
    },
    "daysOfWeek": [1, 2, 3, 4, 5]
  },
  "callSettings": {
    "maxConcurrentCalls": 10,
    "callerId": "+15559876543",
    "retrySettings": {
      "maxAttempts": 3,
      "retryInterval": 60
    }
  },
  "createdAt": "2025-05-17T14:30:00Z"
}
```

#### Get Campaign Details

```
GET /campaigns/{id}
```

Retrieve details for a specific campaign.

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2e1",
  "name": "Summer Promotion",
  "description": "Outreach for summer sale",
  "status": "active",
  "templateId": "60a2e7f3b9c1a83e94d8f2b2",
  "totalContacts": 152,
  "completedCalls": 45,
  "successfulCalls": 32,
  "progress": 29.6,
  "schedule": {
    "startDate": "2025-05-20T09:00:00Z",
    "endDate": "2025-05-25T17:00:00Z",
    "timeZone": "America/New_York",
    "callHours": {
      "start": "09:00",
      "end": "17:00"
    },
    "daysOfWeek": [1, 2, 3, 4, 5]
  },
  "callSettings": {
    "maxConcurrentCalls": 10,
    "callerId": "+15559876543",
    "retrySettings": {
      "maxAttempts": 3,
      "retryInterval": 60
    }
  },
  "createdAt": "2025-05-17T14:30:00Z",
  "startedAt": "2025-05-20T09:00:02Z",
  "lastRunAt": "2025-05-20T16:45:12Z"
}
```

#### List Campaigns

```
GET /campaigns
```

Retrieve a list of campaigns with optional filtering.

**Query Parameters:**

- `status` - Filter by campaign status (scheduled, active, paused, completed)
- `page` - Page number for pagination (default: 1)
- `limit` - Number of results per page (default: 20, max: 100)

**Response:**

```json
{
  "data": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2e1",
      "name": "Summer Promotion",
      "description": "Outreach for summer sale",
      "status": "active",
      "totalContacts": 152,
      "completedCalls": 45,
      "progress": 29.6,
      "createdAt": "2025-05-17T14:30:00Z"
    },
    // More campaigns...
  ],
  "pagination": {
    "total": 12,
    "page": 1,
    "limit": 20,
    "pages": 1
  }
}
```

#### Update Campaign Status

```
POST /campaigns/{id}/status
```

Update the status of a campaign.

**Request Body:**

```json
{
  "status": "paused"
}
```

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2e1",
  "status": "paused",
  "message": "Campaign successfully paused"
}
```

### Contacts

#### Create a Contact

```
POST /contacts
```

Create a new contact.

**Request Body:**

```json
{
  "name": "John Smith",
  "phone": "+15551234567",
  "email": "john.smith@example.com",
  "company": "Acme Inc",
  "tags": ["customer", "vip"],
  "customFields": {
    "industry": "Technology",
    "lastPurchase": "2025-04-15"
  }
}
```

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2a1",
  "name": "John Smith",
  "phone": "+15551234567",
  "email": "john.smith@example.com",
  "company": "Acme Inc",
  "tags": ["customer", "vip"],
  "customFields": {
    "industry": "Technology",
    "lastPurchase": "2025-04-15"
  },
  "createdAt": "2025-05-17T14:35:00Z"
}
```

#### Get Contact Details

```
GET /contacts/{id}
```

Retrieve details for a specific contact.

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2a1",
  "name": "John Smith",
  "phone": "+15551234567",
  "email": "john.smith@example.com",
  "company": "Acme Inc",
  "tags": ["customer", "vip"],
  "customFields": {
    "industry": "Technology",
    "lastPurchase": "2025-04-15"
  },
  "callHistory": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2c3",
      "date": "2025-05-20T15:30:02Z",
      "duration": 223,
      "outcome": "successful"
    }
  ],
  "createdAt": "2025-05-17T14:35:00Z",
  "updatedAt": "2025-05-20T15:34:00Z"
}
```

#### List Contacts

```
GET /contacts
```

Retrieve a list of contacts with optional filtering.

**Query Parameters:**

- `tag` - Filter by tag
- `search` - Search by name, email, or phone
- `page` - Page number for pagination (default: 1)
- `limit` - Number of results per page (default: 20, max: 100)

**Response:**

```json
{
  "data": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2a1",
      "name": "John Smith",
      "phone": "+15551234567",
      "email": "john.smith@example.com",
      "company": "Acme Inc",
      "tags": ["customer", "vip"],
      "createdAt": "2025-05-17T14:35:00Z"
    },
    // More contacts...
  ],
  "pagination": {
    "total": 1243,
    "page": 1,
    "limit": 20,
    "pages": 63
  }
}
```

### Templates

#### Create a Template

```
POST /templates
```

Create a new call template.

**Request Body:**

```json
{
  "name": "Sales Outreach",
  "description": "Template for initial sales calls",
  "industry": "sales",
  "steps": [
    {
      "type": "greeting",
      "content": "Hello, this is {companyName}. Am I speaking with {contactName}?"
    },
    {
      "type": "information",
      "content": "I'm calling to tell you about our new {productName} that I think would be perfect for your business."
    },
    {
      "type": "question",
      "content": "Do you have a few minutes to discuss how this could benefit your company?"
    },
    {
      "type": "response",
      "content": "Great! Let me tell you about our key features..."
    },
    {
      "type": "closing",
      "content": "Thank you for your time. Would you like to schedule a follow-up call with one of our specialists?"
    }
  ],
  "variables": ["companyName", "contactName", "productName"]
}
```

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2b2",
  "name": "Sales Outreach",
  "description": "Template for initial sales calls",
  "industry": "sales",
  "steps": [
    {
      "id": "1",
      "type": "greeting",
      "content": "Hello, this is {companyName}. Am I speaking with {contactName}?"
    },
    // More steps...
  ],
  "variables": ["companyName", "contactName", "productName"],
  "createdAt": "2025-05-17T14:40:00Z"
}
```

#### Get Template Details

```
GET /templates/{id}
```

Retrieve details for a specific template.

**Response:**

```json
{
  "id": "60a2e7f3b9c1a83e94d8f2b2",
  "name": "Sales Outreach",
  "description": "Template for initial sales calls",
  "industry": "sales",
  "steps": [
    {
      "id": "1",
      "type": "greeting",
      "content": "Hello, this is {companyName}. Am I speaking with {contactName}?"
    },
    // More steps...
  ],
  "variables": ["companyName", "contactName", "productName"],
  "usageCount": 245,
  "createdAt": "2025-05-17T14:40:00Z",
  "updatedAt": "2025-05-17T14:40:00Z"
}
```

#### List Templates

```
GET /templates
```

Retrieve a list of templates with optional filtering.

**Query Parameters:**

- `industry` - Filter by industry
- `search` - Search by name or description
- `page` - Page number for pagination (default: 1)
- `limit` - Number of results per page (default: 20, max: 100)

**Response:**

```json
{
  "data": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2b2",
      "name": "Sales Outreach",
      "description": "Template for initial sales calls",
      "industry": "sales",
      "stepCount": 5,
      "usageCount": 245,
      "createdAt": "2025-05-17T14:40:00Z"
    },
    // More templates...
  ],
  "pagination": {
    "total": 28,
    "page": 1,
    "limit": 20,
    "pages": 2
  }
}
```

### Analytics

#### Get Call Statistics

```
GET /analytics/calls
```

Retrieve call statistics with optional filtering.

**Query Parameters:**

- `startDate` - Start date for analysis (ISO format)
- `endDate` - End date for analysis (ISO format)
- `campaignId` - Filter by campaign ID
- `groupBy` - Group results by (day, week, month)

**Response:**

```json
{
  "totalCalls": 1284,
  "completedCalls": 1156,
  "avgDuration": 204,
  "successRate": 76.5,
  "callsByOutcome": {
    "successful": 884,
    "noAnswer": 156,
    "voicemail": 89,
    "rejected": 27
  },
  "callsByTime": [
    {
      "date": "2025-05-01",
      "calls": 42
    },
    // More data points...
  ]
}
```

#### Get Campaign Performance

```
GET /analytics/campaigns
```

Retrieve campaign performance metrics.

**Query Parameters:**

- `startDate` - Start date for analysis (ISO format)
- `endDate` - End date for analysis (ISO format)
- `campaignIds` - Comma-separated list of campaign IDs

**Response:**

```json
{
  "campaigns": [
    {
      "id": "60a2e7f3b9c1a83e94d8f2e1",
      "name": "Summer Promotion",
      "totalCalls": 152,
      "completedCalls": 145,
      "successfulCalls": 112,
      "conversionRate": 73.7,
      "avgDuration": 215
    },
    // More campaigns...
  ],
  "overall": {
    "totalCampaigns": 5,
    "totalCalls": 687,
    "avgConversionRate": 68.2,
    "avgDuration": 198
  }
}
```

## Webhooks

### Overview

Webhooks allow you to receive real-time notifications when specific events occur in your AI Call Center SaaS account.

### Setting Up Webhooks

1. Navigate to Settings > Webhooks in your account
2. Add a new webhook endpoint URL
3. Select the events you want to subscribe to
4. Save your webhook configuration

### Event Types

- `call.started` - Triggered when a call begins
- `call.completed` - Triggered when a call ends
- `call.failed` - Triggered when a call fails
- `campaign.started` - Triggered when a campaign begins
- `campaign.completed` - Triggered when a campaign ends
- `campaign.paused` - Triggered when a campaign is paused

### Webhook Payload

```json
{
  "id": "evt_60a2e7f3b9c1a83e94d8f2f1",
  "type": "call.completed",
  "created": "2025-05-20T15:33:45Z",
  "data": {
    "callId": "60a2e7f3b9c1a83e94d8f2c3",
    "contactId": "60a2e7f3b9c1a83e94d8f2a1",
    "campaignId": "60a2e7f3b9c1a83e94d8f2e1",
    "duration": 223,
    "outcome": "successful",
    "recording": "https://api.your-domain.com/recordings/60a2e7f3b9c1a83e94d8f2c3.mp3"
  }
}
```

### Security

Webhook requests include a signature in the `X-Signature` header. Verify this signature to ensure the request came from our servers:

```
X-Signature: sha256=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
```

The signature is a HMAC SHA-256 hash of the request body using your webhook secret as the key.

## Error Handling

### Error Codes

- `400` - Bad Request: Invalid parameters
- `401` - Unauthorized: Invalid or missing API key
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource not found
- `429` - Too Many Requests: Rate limit exceeded
- `500` - Internal Server Error: Something went wrong on our end

### Error Response Format

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "The parameter 'phone' is invalid",
    "details": {
      "field": "phone",
      "reason": "must be a valid phone number"
    }
  }
}
```

## SDK Libraries

We provide official SDK libraries for easy integration:

- [JavaScript/Node.js](https://github.com/risessolutions/ai-call-center-node)
- [Python](https://github.com/risessolutions/ai-call-center-python)
- [PHP](https://github.com/risessolutions/ai-call-center-php)
- [Ruby](https://github.com/risessolutions/ai-call-center-ruby)
- [Java](https://github.com/risessolutions/ai-call-center-java)
- [.NET](https://github.com/risessolutions/ai-call-center-dotnet)

## Support

If you need assistance with our API, please contact:

- Email: api-support@risessolutions.com
- Documentation: https://docs.risessolutions.com/api
- GitHub Issues: https://github.com/risessolutions/ai-call-center-api/issues
