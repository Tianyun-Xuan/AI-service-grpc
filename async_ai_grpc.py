"""
This module is used to create a gRPC server for AI service.
It will send heartbeat to the heartbeat server regularly.
It will also receive tasks from the task server and process them.

(TODO: add unit test for aysnc methods)
This module use corotine and syncronize with asyncio.

Author: Tianyun Xuan (tianyun.xuan@cn.innovusion.com)

Usage:
    python ai_grpc.py \
        --uuid 1 \
        --heartbeat_address localhost \
        --heartbeat_port 50051 \
        --task_address localhost \
        --task_port 50052

"""
import os
import time
import grpc
import asyncio
import logging
import argparse


import ai_grpc_service_pb2
import ai_grpc_service_pb2_grpc
import ai_grpc_heartbeat_pb2
import ai_grpc_heartbeat_pb2_grpc

from task_pool import TaskPool, TaskResult, Method_Wrapper


class HeartbeatSender:

    def __init__(self, ip_address: str, port: str, service_id: int) -> None:
        self.service_id = service_id
        self.ip_address = ip_address
        self.channel = grpc.aio.insecure_channel(
            f"{ip_address}:{port}")
        self.stub = ai_grpc_heartbeat_pb2_grpc.AIGprcHeartStub(self.channel)

    async def send(self, status: ai_grpc_heartbeat_pb2.StatusCode, msg: str = '') -> None:
        request = ai_grpc_heartbeat_pb2.HeartStatus()
        request.service_id = self.service_id
        request.status = status
        request.timestamp = int(time.time())
        request.msg = msg
        request.ip = self.ip_address

        response = await self.stub.HeartBeat(request)
        logging.info("HeartbeatSender: %s", response)


class AIGrpcTaskService(ai_grpc_service_pb2_grpc.AIGprcTaskServiceServicer):
    def __init__(self, ip_address: str, port: str, service_id: int, function) -> None:
        self.service_id = service_id
        self.ip_address = ip_address
        self.port = port
        self.heartbeat_sender = HeartbeatSender(
            ip_address, port, service_id)

        self.status = ai_grpc_heartbeat_pb2.StatusCode.SLEEPING
        self.status_message = "Heartbeat"

        self.heartbeat_queue = asyncio.Queue()
        self.task_queue = TaskPool(max_workers=1)
        self.function = function

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.task_queue.join()
        for worker in self.workers:
            worker.join()

    async def SendTask(
        self,
        request: ai_grpc_service_pb2.TaskRequest,
        context: grpc.aio.ServicerContext,
    ) -> ai_grpc_service_pb2.TaskReply:

        if self.status == ai_grpc_heartbeat_pb2.StatusCode.SLEEPING:
            self.status = ai_grpc_heartbeat_pb2.StatusCode.WORKING
            self.status_message = "Working"
            self.task_queue.submit(self.function, self.status_message)
            await self.heartbeat_queue.put(self.heartbeat_sender.send(self.status, self.status_message))
            return ai_grpc_service_pb2.TaskReply(code=ai_grpc_service_pb2.ResponseCode.OK)
        else:
            return ai_grpc_service_pb2.TaskReply(code=ai_grpc_service_pb2.ResponseCode.Error)

    async def insert_tasks(self):
        while True:
            status_list = self.task_queue.get_results()

            if (status_list.__len__() > 0):
                for status in status_list:
                    await self.heartbeat_queue.put(self.heartbeat_sender.send(status.status, str(status)))
                    self.status = status_list[-1].status
                    self.status_message = status_list[-1].msg
            else:
                await self.heartbeat_queue.put(self.heartbeat_sender.send(self.status, self.status_message))
            await asyncio.sleep(5)

    async def process_tasks(self):
        while True:
            task = await self.heartbeat_queue.get()
            await task


async def main(params):
    service = AIGrpcTaskService(
        params.heartbeat_address, params.heartbeat_port, params.uuid, Method_Wrapper)
    server = grpc.aio.server()
    ai_grpc_service_pb2_grpc.add_AIGprcTaskServiceServicer_to_server(
        service, server)
    listen_addr = f"{params.task_address}:{params.task_port}"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    server_task = asyncio.create_task(server.start())
    tasks = [
        service.insert_tasks(),     # regular heartbeat
        service.process_tasks(),    # send heartbeat
        server_task                 # server task
    ]

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        await server.stop(None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--uuid', '-u', type=int, default=1)
    parser.add_argument('--heartbeat_address', '-ha',
                        type=str, default='localhost')
    parser.add_argument('--heartbeat_port', '-hp', type=str, default='50051')
    parser.add_argument('--task_address', '-ta', type=str, default='localhost')
    parser.add_argument('--task_port', '-tp', type=str, default='50052')
    parser.add_argument('--log_dir', '-ld', type=str, default='logs')

    args = parser.parse_args()

    os.makedirs(args.log_dir, exist_ok=True)
    start_time = time.time()
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=f'{args.log_dir}/{start_time}.log',
        filemode='a'
    )

    asyncio.run(main(args))
