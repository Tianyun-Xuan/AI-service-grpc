"""
This module is method wrapper for task pool's input method.

Author: Tianyun Xuan (tianyun.xuan@cn.innovusion.com)

"""
import ai_grpc_heartbeat_pb2
import time
import json
import subprocess
import os
import base64

def run(arg):
    docker_name = "f2fd16a2359a"
    script_excu = "python3"
    script_name = "/apollo/data/test.py"
    encoded_data = base64.b64encode(arg.encode("UTF-8"))
    command = f'docker exec -it {docker_name} {script_excu} {script_name} {encoded_data}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    
    # decoded_data = base64.b64decode(os.sys.argv[1].encode("UTF-8"))
    # run(**json.loads(decoded_data.decode()))


class TaskResult:
    def __init__(self, msg: str = "", status: ai_grpc_heartbeat_pb2.StatusCode = ai_grpc_heartbeat_pb2.StatusCode.SLEEPING):
        self.msg = msg
        self.status = status

    def __str__(self):
        # use json format
        return f"{{'msg': '{self.msg}', 'status': {self.status}}}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, TaskResult):
            return self.msg == __value.msg and self.status == __value.status
        else:
            return False


def method_wrapper(arg):
    msg = ""
    status = ai_grpc_heartbeat_pb2.StatusCode.SLEEPING
    try:
        arg_str = json.loads(arg)
        run(arg)
        msg = f"[Method_Wrapper] Finished task : {arg_str}"
    except Exception as e:
        msg = f"[Method_Wrapper] Failed task : {e}"
        status = ai_grpc_heartbeat_pb2.StatusCode.TASK_EXCEPTION
    return TaskResult(msg, status)