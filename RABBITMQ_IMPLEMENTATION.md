# Team06 Grounding DINO with RabbitMQ Implementation

## Overview
This implementation adds RabbitMQ-based RPC and queue worker functionality to your Grounding DINO API service, replacing the original Redis/Celery setup.

## Architecture

### Services
1. **team06-mq**: RabbitMQ message broker with management interface
2. **team06-grounding-dino**: Main FastAPI service (producer) with GPU support
3. **team06-producer**: HTTP proxy service for external access
4. **team06-consumer**: Queue worker for processing detection tasks

### Ports
- `1600`: Main Grounding DINO API
- `7201`: RabbitMQ message broker
- `7202`: RabbitMQ management interface (admin/password123)
- `7203`: Producer proxy service

## Key Changes

### 1. Queue Worker (`queue_worker_rabbitmq.py`)
- Replaced Celery with native RabbitMQ using `pika`
- `TaskManager` class for task submission and management
- `DetectionConsumer` class for processing tasks
- In-memory task result storage

### 2. Main Service (`server.py`)
- Updated to import RabbitMQ queue worker
- Environment variables updated for RabbitMQ configuration
- API documentation updated to reflect RabbitMQ usage

### 3. Docker Configuration
- Added RabbitMQ service with management interface
- GPU support configured for both main service and consumer
- Producer service for external HTTP access
- Consumer service for background task processing

### 4. Dependencies (`requirements.txt`)
- Added `pika==1.3.2` for RabbitMQ client
- Removed Redis and Celery dependencies

## Environment Variables

### RabbitMQ Configuration
- `RABBITMQ_HOST`: RabbitMQ hostname (default: team06-mq)
- `RABBITMQ_PORT`: RabbitMQ port (default: 5672)
- `RABBITMQ_USER`: RabbitMQ username (default: admin)
- `RABBITMQ_PASS`: RabbitMQ password (default: password123)
- `TASK_QUEUE`: Task queue name (default: team06_detection_tasks)
- `RESULT_QUEUE`: Result queue name (default: team06_detection_results)

### Other
- `ENABLE_QUEUE`: Enable queue processing (default: true)
- `GROUNDING_DINO_HOST`: Backend service hostname for producer
- `GROUNDING_DINO_PORT`: Backend service port for producer

## Usage

### Deployment
```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f team06-grounding-dino
docker-compose logs -f team06-consumer
```

### API Endpoints
- Main API: `http://localhost:1600`
- Producer proxy: `http://localhost:7203`  
- RabbitMQ management: `http://localhost:7202` (admin/password123)

### Synchronous Detection
```bash
curl -X POST "http://localhost:1600/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://images.cocodataset.org/val2017/000000039769.jpg",
    "text_queries": ["cat", "remote", "person"],
    "async_processing": false
  }'
```

### Asynchronous Detection
```bash
# Submit task
curl -X POST "http://localhost:1600/detect/async" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://images.cocodataset.org/val2017/000000039769.jpg",
    "text_queries": ["cat", "remote", "person"],
    "priority": 7
  }'

# Check task status
curl -X GET "http://localhost:1600/task/{task_id}"
```

## Benefits
1. **GPU Acceleration**: Both main service and consumer use H100 GPU
2. **Scalability**: Can scale consumer instances independently
3. **Reliability**: RabbitMQ provides message persistence and delivery guarantees
4. **Monitoring**: RabbitMQ management interface for queue monitoring
5. **Load Balancing**: Producer proxy can distribute requests

## Files Modified/Created
- `queue_worker_rabbitmq.py`: New RabbitMQ-based queue implementation
- `server.py`: Updated to use RabbitMQ queue worker
- `docker-compose.yml`: Added RabbitMQ and consumer services
- `requirements.txt`: Updated dependencies
- `consumer/`: Consumer service directory with Dockerfile and app
- `producer/`: Producer proxy service directory
- `.gitlab-ci.yml`: Updated for GPU deployment
