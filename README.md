# Smart Community Health Monitoring and Early Warning System

## Overview
This system collects community health data, water quality data from IoT sensors, and predicts potential outbreaks of water-borne diseases in rural Northeast India.

## Modules
- **api/** : FastAPI backend (data ingest, alerts)
- **ml/** : AI/ML prediction service
- **iot-gateway/** : MQTT subscriber/publisher for water sensors
- **mobile-app/** : Expo React Native app for ASHA/community reporting
- **dashboard/** : React web dashboard for officials

## Quick Start
```bash
docker-compose up --build
```

API available at: `http://localhost:8000`  
ML model at: `http://localhost:8001`  
Dashboard dev server: `cd dashboard && npm install && npm start`  
Mobile app dev: `cd mobile-app && npm install && expo start`
