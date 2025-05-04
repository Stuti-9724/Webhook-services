# Webhook Delivery Service

A robust webhook delivery service built with FastAPI, PostgreSQL, Redis, and Celery. This service manages webhook subscriptions, delivers webhook events with retry mechanisms, and provides delivery status tracking.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Local Development](#local-development)
  - [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Features

### Current Features
- **Subscription Management**: Complete CRUD operations for webhook subscriptions
- **Event Processing**:
  - Webhook event ingestion and reliable delivery
  - Automatic retries with exponential backoff
  - Webhook signature verification for security
- **Monitoring & Tracking**:
  - Real-time delivery status tracking
  - Event type filtering capabilities
  - Comprehensive delivery logs with 72-hour retention
- **Performance Optimization**:
  - Redis caching for improved response times
  - Celery task queue for asynchronous processing

## Tech Stack

- **Backend Framework**: FastAPI
  - High-performance async framework
  - Built-in OpenAPI documentation
  - Type checking with Pydantic

- **Database**: PostgreSQL
  - Reliable data persistence
  - ACID compliance
  - Complex query capabilities

- **Caching & Message Broker**: Redis
  - Fast in-memory data store
  - Message broker for Celery
  - Subscription data caching

- **Task Queue**: Celery
  - Asynchronous task processing
  - Retry mechanisms
  - Task monitoring

- **Containerization**: Docker & Docker Compose
  - Consistent development environment
  - Easy deployment
  - Service orchestration

## Architecture

### Components
1. **API Layer (FastAPI)**
   - Handles HTTP requests
   - Manages subscriptions
   - Validates incoming events

2. **Database Layer (PostgreSQL)**
   - Stores subscription data
   - Maintains delivery logs
   - Tracks webhook statuses

3. **Cache Layer (Redis)**
   - Caches frequently accessed data
   - Reduces database load
   - Improves response times

4. **Worker Layer (Celery)**
   - Processes webhook deliveries
   - Handles retries
   - Manages async tasks

## Getting Started

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd webhook-service
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Access the services**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost:5173

### Production Deployment

The service is configured for deployment on Render using `render.yaml`:

1. **Services**:
   - Backend API (Python/FastAPI)
   - Frontend (Node.js/Vite)
   - Redis instance
   - PostgreSQL database

2. **Environment Variables**:
   - Configure through Render dashboard
   - Set up database and Redis connections
   - Configure security settings

## API Documentation

### Key Endpoints

1. **Subscription Management**
   - `POST /subscriptions`: Create new subscription
   - `GET /subscriptions`: List all subscriptions
   - `PUT /subscriptions/{id}`: Update subscription
   - `DELETE /subscriptions/{id}`: Delete subscription

2. **Webhook Events**
   - `POST /events`: Submit new webhook event
   - `GET /events`: List processed events
   - `GET /events/{id}/status`: Check delivery status

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `CELERY_BROKER_URL`: Celery broker URL
- `CELERY_RESULT_BACKEND`: Celery result backend URL

### Security Settings

- Webhook signatures for verification
- Rate limiting configurations
- IP allowlist settings

## Monitoring and Maintenance

### Logging and Monitoring
- Delivery logs retained for 72 hours
- Automatic log cleanup every 12 hours
- Celery Flower dashboard for task monitoring
- Redis caching with 10-minute TTL

### Health Checks
- API health endpoint
- Database connection monitoring
- Redis connection status
- Worker health checks