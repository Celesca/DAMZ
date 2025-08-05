import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Import our detection consumer
        from queue_worker_rabbitmq import DetectionConsumer
        
        logger.info("Starting Team06 Grounding DINO Consumer...")
        consumer = DetectionConsumer()
        consumer.start_consuming()
        
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Consumer failed: {e}")
        raise
