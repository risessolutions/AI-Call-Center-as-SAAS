# Integrations

This directory contains integration components for connecting the AI Call Center SaaS platform with external systems.

## Technology Stack

- RESTful API clients
- GraphQL clients (where applicable)
- Webhook handlers
- Data transformation utilities

## Key Components

- CRM System Connectors (Salesforce, HubSpot, etc.)
- ERP Integration
- IVR/PBX System Integration
- Email Marketing Platform Connectors
- Custom API Integrations

## Getting Started

1. Install dependencies:
```
npm install
```

2. Configure integration credentials:
```
cp credentials.example.json credentials.json
```

3. Test connections:
```
npm run test-connections
```

## Structure

- `crm/` - Customer Relationship Management system connectors
- `erp/` - Enterprise Resource Planning system connectors
- `telephony/` - Phone system integrations
- `marketing/` - Marketing platform integrations
- `webhooks/` - Webhook handlers and processors
- `utils/` - Helper functions and utilities
