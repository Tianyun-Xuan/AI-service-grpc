''''''
import queue
import threading
import time
import ai_grpc_heartbeat_pb2

import json


def Method_Wrapper(arg):
    msg = f"Method_Wrapper: {arg}"
    flag = False
    try:
        arg_str = json.loads(arg)
        # result = your_methode(**arg_str)
        time.sleep(5)
        flag = True
    except Exception as e:
        msg = f"Method_Wrapper: {e}"
        flag = False
    return TaskResult(msg, flag)


class TaskResult:
    def __init__(self, msg: str = "", flag: bool = True, status: ai_grpc_heartbeat_pb2.StatusCode = ai_grpc_heartbeat_pb2.StatusCode.SLEEPING):
        self.msg = msg
        self.flag = flag
        self.status = status

    def __str__(self):
        # use json format
        return f"{{'msg': '{self.msg}', 'flag': {self.flag}, 'status': {self.status}}}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TaskResult):
            return self.msg == __value.msg and self.flag == __value.flag and self.status == __value.status
        else:
            return False


class TaskPool:
    def __init__(self, max_workers=5):
        self.queue = queue.Queue()
        self.result_queue = queue.Queue()  # Added result queue
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
            method, arg = task
            try:
                result = method(arg)
                # Store result in the result queue
                self.result_queue.put(result)
            except Exception as e:
                self.result_queue.put(TaskResult(e, False))
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
        while not self.result_queue.empty():
            result = self.result_queue.get()
            results.append(result)
        return results
