# -*- coding: utf-8 -*-
"""Ragflow MCP Search Service Module"""

import logging
import sys

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    # Use alternative solution for Windows console encoding issues
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

# Import other modules
import logging
import threading
import queue
import uuid
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from fastmcp import FastMCP

# Configure logging
logger = logging.getLogger('ragflow_mcp')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create task storage dictionary and thread pool
search_tasks = {}
task_queue = queue.Queue()
executor = ThreadPoolExecutor(max_workers=5)  # Adjust based on server performance
lock = threading.Lock()  # For thread safety

# Create an MCP server
mcp = FastMCP("ragflow_mcp")

# Worker thread function
def search_worker():
    """Background worker thread to handle search tasks"""
    while True:
        task_id = task_queue.get()
        if task_id is None:  # Received stop signal
            break
            
        try:
            logger.info(f"Processing search task: {task_id}")
            task = search_tasks[task_id]
            question = task["question"]
            
            # Actual search request
            url = "http://localhost/api/v1/retrieval"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer ragflow-MyMjRkODQ2NTU3YjExZjBiZjE1MGFjMz"
            }
            data = {
                "question": question,
                "dataset_ids": ["96da6822557111f0b2ac0ac373b69adc"],
                "document_ids": [],
                "highlight": False,
                "similarity_threshold": 0.30,
                "top_k": 128,
                "page_size": 2,
                "return_fields": ["content_ltks", "document_keyword", "similarity"]  # Return only necessary fields
            }
            
            # Send request
            start_time = time.time()
            response = requests.post(url, headers=headers, json=data, timeout=30)
            duration = time.time() - start_time
            logger.info(f"Search task {task_id} completed in {duration:.2f}s with status: {response.status_code}")
            
            # Process response
            with lock:
                if response.status_code == 200:
                    result = []
                    response_data = response.json()
                    logger.info(f"Response data: {response_data}")
                    for item in response_data.get("data", []).get("chunks", []):
                        # Process each result item
                        logger.info(f"Processing item: {item}")
                        # Extract only necessary fields
                        result.append({
                            "content_ltks": item.get("content_ltks", ""),
                            "document_keyword": item.get("document_keyword", ""),
                            "similarity": item.get("similarity", 0.0),
                        })
                    
                    if result:
                        search_tasks[task_id]["status"] = "completed"
                        search_tasks[task_id]["result"] = result
                    else:
                        search_tasks[task_id]["status"] = "completed"
                        search_tasks[task_id]["result"] = []
                        search_tasks[task_id]["message"] = "No results found"
                else:
                    search_tasks[task_id]["status"] = "error"
                    search_tasks[task_id]["error"] = f"API error: {response.status_code} - {response.text[:200]}"
            
        except requests.Timeout:
            with lock:
                search_tasks[task_id]["status"] = "error"
                search_tasks[task_id]["error"] = "Request timed out"
            logger.error(f"Search task {task_id} timed out")
        except Exception as e:
            with lock:
                search_tasks[task_id]["status"] = "error"
                search_tasks[task_id]["error"] = str(e)
            logger.exception(f"Error processing search task {task_id}: {str(e)}")
        finally:
            task_queue.task_done()

# Start worker threads
for i in range(executor._max_workers):
    executor.submit(search_worker)

@mcp.tool()
def start_search(question: str) -> dict:
    """
    Start Ragflow search task and return task ID for further result retrieval.
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Starting search task {task_id} for question: {question}")
    
    # Initialize task status
    with lock:
        search_tasks[task_id] = {
            "status": "queued",
            "question": question,
            "start_time": time.time(),
            "result": None,
            "error": None
        }
    
    # Add task to queue
    task_queue.put(task_id)
    logger.info(f"Task {task_id} added to queue")
    
    # Wait for the search to complete and return results directly
    while True:
        time.sleep(0.5)  # Check every 0.5 seconds
        with lock:
            if search_tasks[task_id]["status"] == "completed":
                result = search_tasks[task_id].get("result", [])
                message = search_tasks[task_id].get("message", "")
                return {
                    "success": True,
                    "status": "completed",
                    "results": result,
                    "message": message
                }
            elif search_tasks[task_id]["status"] == "error":
                error = search_tasks[task_id].get("error", "Unknown error")
                return {
                    "success": False,
                    "status": "error",
                    "error": error
                }

    return {"success": True, "task_id": task_id, "status": "queued"}

@mcp.tool()
def get_search_status(task_id: str) -> dict:
    """
    Get task status
    """
    with lock:
        task = search_tasks.get(task_id)

    if not task:
        return {"success": False, "error": "Task ID not found"}

    status_info = {
        "task_id": task_id,
        "status": task["status"],
        "question": task["question"],
        "elapsed_time": time.time() - task["start_time"]
    }

    if task["status"] == "error":
        status_info["error"] = task.get("error", "Unknown error")

    return {"success": True, **status_info}

@mcp.tool()
def get_search_results(task_id: str) -> dict:
    """
    Retrieve Ragflow search results based on the task ID.
    """
    logger.info(f"Retrieving results for task: {task_id}")
    
    with lock:
        task = search_tasks.get(task_id)

    # Check if task exists
    if not task:
        logger.error(f"Task ID {task_id} not found")
        return {"success": False, "error": "Task ID not found"}

    # Check task status
    if task["status"] == "queued":
        logger.info(f"Task {task_id} is still in queue")
        return {"success": False, "status": "queued", "message": "Task is still in queue"}

    if task["status"] == "processing":
        logger.info(f"Task {task_id} is still processing")
        return {"success": False, "status": "processing", "message": "Search in progress"}

    if task["status"] == "error":
        logger.error(f"Task {task_id} encountered an error: {task.get('error', 'Unknown error')}")
        return {"success": False, "status": "error", "error": task.get("error", "Unknown error")}

    # Process completed task
    if "result" in task:
        return {
            "success": True,
            "status": "completed",
            "results": task["result"],
            "message": task.get("message", "")
        }

    return {"success": False, "error": "Unexpected task state"}

@mcp.tool()
def cancel_search(task_id: str) -> dict:
    """
    Cancel an ongoing search task
    """
    logger.info(f"Canceling task: {task_id}")
    
    with lock:
        if task_id in search_tasks:
            # Update status to canceled
            if search_tasks[task_id]["status"] in ["queued", "processing"]:
                search_tasks[task_id]["status"] = "canceled"
                return {"success": True, "message": "Task canceled"}
            else:
                return {"success": False, "error": "Task cannot be canceled in its current state"}
        return {"success": False, "error": "Task ID not found"}

@mcp.tool()
def get_active_tasks() -> dict:
    """
    Get information about all active tasks
    """
    with lock:
        active_tasks = []
        for task_id, task in search_tasks.items():
            if task["status"] in ["queued", "processing"]:
                active_tasks.append({
                    "task_id": task_id,
                    "status": task["status"],
                    "question": task["question"],
                    "elapsed_time": time.time() - task["start_time"]
                })
        
        return {
            "success": True,
            "active_tasks": active_tasks,
            "total_tasks": len(active_tasks)
        }

def cleanup_old_tasks():
    """Periodically clean up old tasks"""
    while True:
        time.sleep(3600)  # Clean up every hour
        cleanup_time = time.time() - 86400  # Clean up tasks older than 24 hours
        
        with lock:
            # Find tasks to delete
            to_delete = []
            for task_id, task in search_tasks.items():
                if task["start_time"] < cleanup_time:
                    to_delete.append(task_id)
            
            # Delete old tasks
            for task_id in to_delete:
                del search_tasks[task_id]
            
            logger.info(f"Cleaned up {len(to_delete)} old tasks")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_tasks, daemon=True)
cleanup_thread.start()

# Start the server
if __name__ == "__main__":
    try:
        logger.info("Starting Ragflow MCP server with threaded search")
        mcp.run(transport="stdio")
    finally:
        # Graceful shutdown
        logger.info("Shutting down thread pool...")
        # Send stop signal to all worker threads
        for _ in range(executor._max_workers):
            task_queue.put(None)
        executor.shutdown(wait=True)
        logger.info("Thread pool shutdown complete")