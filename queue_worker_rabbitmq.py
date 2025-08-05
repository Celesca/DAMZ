import os
import pika
import uuid
import json
import threading
import time
import logging
from typing import Any, Dict, Callable, Optional
import base64
from datetime import datetime

from model import ModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "team06-mq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password123")
TASK_QUEUE = os.getenv("TASK_QUEUE", "team06_detection_tasks")
RESULT_QUEUE = os.getenv("RESULT_QUEUE", "team06_detection_results")

class TaskManager:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.task_results = {}  # In-memory storage for task results
        self._connect()

    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare queues
            self.channel.queue_declare(queue=TASK_QUEUE, durable=True)
            self.channel.queue_declare(queue=RESULT_QUEUE, durable=True)
            
            logger.info(f"Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def submit_detection_task(self, image_data: Any, image_type: str, text_queries: Any, 
                            box_threshold: float, text_threshold: float, 
                            return_visualization: bool, priority: int = 5) -> str:
        """Submit a detection task to the queue"""
        task_id = str(uuid.uuid4())
        
        # Handle image data serialization
        if image_type == "bytes":
            # Convert bytes to base64 for JSON serialization
            image_data_serialized = base64.b64encode(image_data).decode('utf-8')
        else:
            # URL string
            image_data_serialized = image_data
        
        task = {
            "task_id": task_id,
            "image_data": image_data_serialized,
            "image_type": image_type,
            "text_queries": text_queries,
            "box_threshold": box_threshold,
            "text_threshold": text_threshold,
            "return_visualization": return_visualization,
            "priority": priority,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Initialize task result status
            self.task_results[task_id] = {
                "status": "submitted",
                "task_id": task_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Publish task to queue
            self.channel.basic_publish(
                exchange='',
                routing_key=TASK_QUEUE,
                body=json.dumps(task),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    priority=priority
                )
            )
            
            logger.info(f"Task {task_id} submitted to queue")
            return task_id
            
        except Exception as e:
            logger.error(f"Failed to submit task {task_id}: {e}")
            self.task_results[task_id] = {
                "status": "failed",
                "task_id": task_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            raise

    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Get task result by task_id"""
        if task_id in self.task_results:
            return self.task_results[task_id]
        else:
            return {
                "status": "not_found",
                "task_id": task_id,
                "error": "Task not found"
            }

    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Cancel a task (mark as cancelled)"""
        if task_id in self.task_results:
            self.task_results[task_id]["status"] = "cancelled"
            return {
                "status": "cancelled",
                "task_id": task_id,
                "message": "Task marked as cancelled"
            }
        else:
            return {
                "status": "not_found",
                "task_id": task_id,
                "error": "Task not found"
            }

    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status and statistics"""
        try:
            # Get queue info
            task_queue_info = self.channel.queue_declare(queue=TASK_QUEUE, passive=True)
            task_count = task_queue_info.method.message_count
            
            # Count task statuses
            active_tasks = len([t for t in self.task_results.values() if t["status"] == "processing"])
            completed_tasks = len([t for t in self.task_results.values() if t["status"] == "completed"])
            failed_tasks = len([t for t in self.task_results.values() if t["status"] == "failed"])
            
            return {
                "status": "ok",
                "active_tasks": active_tasks,
                "scheduled_tasks": task_count,
                "reserved_tasks": 0,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "workers": ["consumer-1"],  # Placeholder
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get queue status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    def update_task_result(self, task_id: str, result: Dict[str, Any]):
        """Update task result (called by consumer)"""
        self.task_results[task_id] = result

    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()


# Consumer class for processing tasks
class DetectionConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.model_manager = ModelManager()
        self.task_manager = TaskManager()
        self._connect()

    def _connect(self):
        """Establish connection to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare queues
            self.channel.queue_declare(queue=TASK_QUEUE, durable=True)
            self.channel.queue_declare(queue=RESULT_QUEUE, durable=True)
            
            logger.info("Consumer connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a detection task"""
        task_id = task_data["task_id"]
        
        try:
            logger.info(f"Processing task {task_id}")
            
            # Update task status
            self.task_manager.update_task_result(task_id, {
                "status": "processing",
                "task_id": task_id,
                "stage": "loading_model",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Get model
            model = self.model_manager.get_model()
            
            # Update task status
            self.task_manager.update_task_result(task_id, {
                "status": "processing",
                "task_id": task_id,
                "stage": "processing_image",
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Prepare image data
            image_data = task_data["image_data"]
            image_type = task_data["image_type"]
            
            if image_type == "bytes":
                # Decode base64 back to bytes
                image_source = base64.b64decode(image_data)
            else:
                # URL string
                image_source = image_data
            
            # Process detection
            result = model.process_detection(
                image_source=image_source,
                text_queries=task_data["text_queries"],
                box_threshold=task_data["box_threshold"],
                text_threshold=task_data["text_threshold"],
                return_visualization=task_data["return_visualization"]
            )
            
            # Update task with result
            if result["success"]:
                self.task_manager.update_task_result(task_id, {
                    "status": "completed",
                    "task_id": task_id,
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
                logger.info(f"Task {task_id} completed successfully")
            else:
                self.task_manager.update_task_result(task_id, {
                    "status": "failed",
                    "task_id": task_id,
                    "error": result.get("error", "Unknown error"),
                    "timestamp": datetime.utcnow().isoformat()
                })
                logger.error(f"Task {task_id} failed: {result.get('error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Task {task_id} failed with exception: {e}")
            self.task_manager.update_task_result(task_id, {
                "status": "failed",
                "task_id": task_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            return {"success": False, "error": str(e)}

    def callback(self, ch, method, properties, body):
        """RabbitMQ callback function"""
        try:
            task_data = json.loads(body)
            self.process_task(task_data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        """Start consuming tasks from the queue"""
        try:
            logger.info("Loading Grounding DINO model...")
            self.model_manager.get_model()
            logger.info("Model loaded successfully!")
            
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=TASK_QUEUE, on_message_callback=self.callback)
            
            logger.info(f"[*] Consumer waiting for messages on queue: {TASK_QUEUE}")
            logger.info("To exit press CTRL+C")
            
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
            self.channel.stop_consuming()
            self.connection.close()
        except Exception as e:
            logger.error(f"Consumer error: {e}")
            raise

    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()


# Initialize task manager
task_manager = TaskManager()

if __name__ == "__main__":
    # Run consumer
    consumer = DetectionConsumer()
    consumer.start_consuming()
