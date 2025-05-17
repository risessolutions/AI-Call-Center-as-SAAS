# AI Call Center SaaS - Deployment Guide

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Integration Setup](#integration-setup)
6. [Telephony Configuration](#telephony-configuration)
7. [AI Engine Setup](#ai-engine-setup)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)
10. [Support](#support)

## Introduction

This guide provides detailed instructions for deploying the AI Call Center SaaS platform. The platform consists of several components:

- Backend API server
- Frontend web application
- AI Engine for natural language processing
- Telephony integration services
- Database system

Follow these instructions carefully to ensure a successful deployment.

## System Requirements

### Minimum Hardware Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 50GB SSD
- **Network**: 100Mbps internet connection

### Recommended Hardware Requirements
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 100GB+ SSD
- **Network**: 1Gbps internet connection

### Software Requirements
- **Operating System**: Ubuntu 20.04 LTS or newer
- **Database**: MongoDB 4.4+
- **Node.js**: v16.x or newer
- **Python**: 3.8 or newer
- **Docker**: 20.10 or newer (optional, for containerized deployment)

## Installation

### Option 1: Standard Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/risessolutions/ai-call-center-saas.git
   cd ai-call-center-saas
   ```

2. **Install backend dependencies**
   ```bash
   cd src/backend
   npm install
   ```

3. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Install AI engine dependencies**
   ```bash
   cd ../ai_engine
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit the .env file with your configuration
   ```

### Option 2: Docker Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/risessolutions/ai-call-center-saas.git
   cd ai-call-center-saas
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up -d
   ```

## Configuration

### Database Setup

1. **MongoDB Setup**
   ```bash
   # Install MongoDB if not already installed
   sudo apt update
   sudo apt install -y mongodb
   
   # Start MongoDB service
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   
   # Create database and user
   mongo
   > use ai_call_center
   > db.createUser({user: "admin", pwd: "your_secure_password", roles: ["readWrite", "dbAdmin"]})
   > exit
   ```

2. **Update database configuration in .env file**
   ```
   MONGODB_URI=mongodb://admin:your_secure_password@localhost:27017/ai_call_center
   ```

### Backend Configuration

1. **Configure API server**
   Edit the `.env` file in the `src/backend` directory:
   ```
   PORT=5000
   NODE_ENV=production
   MONGODB_URI=mongodb://admin:your_secure_password@localhost:27017/ai_call_center
   JWT_SECRET=your_jwt_secret_key
   JWT_EXPIRE=30d
   ```

2. **Start the backend server**
   ```bash
   cd src/backend
   npm run start
   ```

### Frontend Configuration

1. **Configure frontend**
   Edit the `.env` file in the `src/frontend` directory:
   ```
   REACT_APP_API_URL=http://your-server-ip:5000/api
   ```

2. **Build the frontend**
   ```bash
   cd src/frontend
   npm run build
   ```

3. **Serve the frontend**
   ```bash
   # Using nginx (recommended for production)
   sudo apt install -y nginx
   sudo cp -r build/* /var/www/html/
   sudo systemctl restart nginx
   
   # OR using serve for testing
   npx serve -s build
   ```

## Integration Setup

### CRM Integrations

#### Salesforce Integration
1. Create a Connected App in Salesforce
2. Configure OAuth settings
3. Add the following to your `.env` file:
   ```
   SALESFORCE_CLIENT_ID=your_client_id
   SALESFORCE_CLIENT_SECRET=your_client_secret
   SALESFORCE_REDIRECT_URI=your_redirect_uri
   ```

#### HubSpot Integration
1. Create a HubSpot Developer Account
2. Register a new application
3. Add the following to your `.env` file:
   ```
   HUBSPOT_API_KEY=your_api_key
   HUBSPOT_CLIENT_ID=your_client_id
   HUBSPOT_CLIENT_SECRET=your_client_secret
   ```

### Email Integrations

Configure SMTP settings in the `.env` file:
```
SMTP_HOST=your_smtp_host
SMTP_PORT=587
SMTP_USER=your_smtp_username
SMTP_PASS=your_smtp_password
EMAIL_FROM=noreply@yourdomain.com
```

## Telephony Configuration

### Twilio Integration
1. Create a Twilio account
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Add the following to your `.env` file:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

### VoIP Configuration
1. Configure SIP settings in the `.env` file:
   ```
   SIP_SERVER=your_sip_server
   SIP_USERNAME=your_sip_username
   SIP_PASSWORD=your_sip_password
   ```

## AI Engine Setup

### Speech-to-Text Configuration
1. Choose your preferred STT provider (Google, AWS, or Azure)
2. Add the appropriate credentials to your `.env` file:

   For Google:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   ```

   For AWS:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=your_region
   ```

   For Azure:
   ```
   AZURE_SPEECH_KEY=your_speech_key
   AZURE_SPEECH_REGION=your_speech_region
   ```

### Text-to-Speech Configuration
1. Configure TTS settings in the `.env` file:
   ```
   TTS_PROVIDER=google  # or aws, azure
   TTS_VOICE_FEMALE=en-US-Standard-F
   TTS_VOICE_MALE=en-US-Standard-B
   ```

### NLP Model Configuration
1. Configure NLP settings in the `.env` file:
   ```
   NLP_MODEL_PATH=models/intent_recognition
   SENTIMENT_MODEL_PATH=models/sentiment_analysis
   ```

## Security Considerations

### SSL/TLS Configuration
1. Obtain an SSL certificate:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

2. Update your nginx configuration to use HTTPS

### Firewall Configuration
1. Configure firewall rules:
   ```bash
   sudo ufw allow 22/tcp  # SSH
   sudo ufw allow 80/tcp  # HTTP
   sudo ufw allow 443/tcp # HTTPS
   sudo ufw allow 5000/tcp # API Server
   sudo ufw enable
   ```

### Data Protection
1. Ensure database backups are scheduled
2. Implement proper access controls
3. Configure data retention policies

## Troubleshooting

### Common Issues

#### Backend Server Won't Start
- Check MongoDB connection
- Verify environment variables
- Check for port conflicts

#### Frontend Not Connecting to Backend
- Verify API URL in frontend configuration
- Check CORS settings in backend
- Ensure network connectivity

#### AI Engine Issues
- Verify Python dependencies
- Check model paths
- Ensure sufficient system resources

## Support

For additional support, please contact:
- Email: support@risessolutions.com
- Documentation: https://docs.risessolutions.com
- GitHub Issues: https://github.com/risessolutions/ai-call-center-saas/issues
