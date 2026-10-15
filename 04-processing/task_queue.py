"""
Asynchronous Task Queue & Worker Pool for High-Volume, Strategic High-Value,
and Processing-Intensive Tasks in the Reverse Engineering Loop Harness.
"""

import os
import sys
import time
import json
import uuid
import heapq
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

class TaskPriority:
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3

class Task:
    def __init__(
        self,
        task_type: str,
        payload: Dict[str, Any],
        priority: int = TaskPriority.NORMAL,
        task_id: Optional[str] = None
    ):
        self.task_id = task_id or str(uuid.uuid4())[:8]
        self.task_type = task_type
        self.payload = payload
        self.priority = priority
        self.status = "QUEUED"
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None

    def __lt__(self, other):
        return self.priority < other.priority

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "result": self.result,
            "error": self.error
        }

class ProcessingTaskQueue:
    def __init__(self, max_concurrency: int = 4):
        self.max_concurrency = max_concurrency
        self.queue: List[Task] = []
        self.running: Dict[str, Task] = {}
        self.completed: Dict[str, Task] = {}

    def enqueue(self, task_type: str, payload: Dict[str, Any], priority: int = TaskPriority.NORMAL) -> str:
        """Enqueues a task with specified priority."""
        task = Task(task_type, payload, priority)
        heapq.heappush(self.queue, task)
        print(f"[TaskQueue] Enqueued task {task.task_id} (Type: {task_type}, Priority: {priority})")
        return task.task_id

    def pop_next(self) -> Optional[Task]:
        """Pops highest priority task ready for execution."""
        if self.queue and len(self.running) < self.max_concurrency:
            task = heapq.heappop(self.queue)
            task.status = "RUNNING"
            task.started_at = time.time()
            self.running[task.task_id] = task
            return task
        return None

    def complete_task(self, task_id: str, result: Dict[str, Any], error: Optional[str] = None) -> None:
        """Marks a task as completed or errored."""
        task = self.running.pop(task_id, None)
        if task:
            task.completed_at = time.time()
            task.result = result
            task.error = error
            task.status = "FAILED" if error else "COMPLETED"
            self.completed[task_id] = task
            print(f"[TaskQueue] Task {task_id} marked {task.status}")

    def get_status(self) -> Dict[str, Any]:
        return {
            "queued_count": len(self.queue),
            "running_count": len(self.running),
            "completed_count": len(self.completed),
            "recent_completed": [t.to_dict() for t in list(self.completed.values())[-5:]]
        }


if __name__ == "__main__":
    tq = ProcessingTaskQueue(max_concurrency=2)
    tq.enqueue("SCRAPE_COMPETITOR_DOCS", {"urls": ["https://example.com/api"]}, TaskPriority.HIGH)
    tq.enqueue("EVALUATION_TASK", {"iteration": 1}, TaskPriority.CRITICAL)
    
    task1 = tq.pop_next()
    print("Popped task (highest priority):", task1.task_type)
    tq.complete_task(task1.task_id, {"score": 0.96})
    print("Queue status:", tq.get_status())
