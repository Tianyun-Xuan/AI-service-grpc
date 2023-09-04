"""
This module is task pool for ai_grpc.py

Author: Tianyun Xuan (tianyun.xuan@cn.innovusion.com)

"""
import queue
import threading
import ai_grpc_heartbeat_pb2
from task_method import TaskResult


class TaskPool:
    def __init__(self, max_workers=5):
        self.queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.workers = []
        self.max_workers = max_workers
        self._create_workers()

    def _create_workers(self):
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            self.workers.append(worker)
            worker.start()

    def _worker(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            try:

                method, arg = task
                if method is None:
                    raise ValueError("Method is None")
                result = method(arg)
                # Store result in the result queue
                self.result_queue.put(result)
            except Exception as e:
                self.result_queue.put(TaskResult(
                    str(e), ai_grpc_heartbeat_pb2.StatusCode.TASK_EXCEPTION))
            finally:
                self.queue.task_done()

    def submit(self, method, arg):
        self.queue.put((method, arg))

    def join(self):
        self.queue.join()

    def close(self):
        for _ in range(self.max_workers):
            self.queue.put(None)
        for worker in self.workers:
            worker.join()

    def get_results(self):
        results = []
        while True:
            try:
                result = self.result_queue.get_nowait()
                results.append(result)
            except queue.Empty:
                break
        return results
