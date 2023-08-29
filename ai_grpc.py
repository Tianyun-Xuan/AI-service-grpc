"""
This module is used to create a gRPC server for AI service.
It will send heartbeat to the heartbeat server regularly.
It will also receive tasks from the task server and process them.

Author: Tianyun Xuan (tianyun.xuan@cn.innovusion.com)

Usage:
    python ai_grpc.py \
        --uuid 1 \
        --heartbeat_address localhost \
        --heartbeat_port 50051 \
        --task_address localhost \
        --task_port 50052

"""
import asyncio
import logging
import argparse
import time
import grpc

from generated import ai_grpc_service_pb2
from generated import ai_grpc_service_pb2_grpc
from generated import ai_grpc_heartbeat_pb2
from generated import ai_grpc_heartbeat_pb2_grpc


class HeartbeatSender:

    def __init__(self, ip_address: str, port: str, service_id: int) -> None:
        self.service_id = service_id
        self.ip = ip_address
        self.channel = grpc.aio.insecure_channel(
            f"{ip_address}:{port}")
        self.stub = ai_grpc_heartbeat_pb2_grpc.AIGprcHeartStub(self.channel)

    async def send(self, status: ai_grpc_heartbeat_pb2.StatusCode, msg: str = '') -> None:
        request = ai_grpc_heartbeat_pb2.HeartStatus()
        request.service_id = self.service_id
        request.status = status
        request.timestamp = int(time.time())
        request.msg = msg
        request.ip = self.ip

        response = await self.stub.HeartBeat(request)
        logging.info("HeartbeatSender: %s", response)
        print(response)


class AIGrpcTaskService(ai_grpc_service_pb2_grpc.AIGprcTaskServiceServicer):
    def __init__(self, ip_address: str, port: str, service_id: int) -> None:
        self.service_id = service_id
        self.ip_address = ip_address
        self.port = port
        self.heartbeat_sender = HeartbeatSender(
            ip_address, port, service_id)

        self.status = ai_grpc_heartbeat_pb2.StatusCode.SLEEPING
        self.status_message = "Heartbeat"

        self.tasks_queue = asyncio.Queue()

    async def SendTask(
        self,
        request: ai_grpc_service_pb2.TaskRequest,
        context: grpc.aio.ServicerContext,
    ) -> ai_grpc_service_pb2.TaskReply:

        # insert your code here
        self.status = ai_grpc_heartbeat_pb2.StatusCode.WORKING
        self.status_message = "Heartbeat"

        await self.tasks_queue.put(
            self.heartbeat_sender.send(self.status, self.status_message))

        return ai_grpc_service_pb2.TaskReply(code=ai_grpc_service_pb2.ResponseCode.OK)

    async def insert_tasks(self):
        while True:
            await self.tasks_queue.put(
                self.heartbeat_sender.send(self.status, self.status_message))
            await asyncio.sleep(5)

    async def process_tasks(self):
        while True:
            task = await self.tasks_queue.get()
            await task


async def main(params):
    service = AIGrpcTaskService(
        params.heartbeat_address, params.heartbeat_port, params.uuid)
    server = grpc.aio.server()
    ai_grpc_service_pb2_grpc.add_AIGprcTaskServiceServicer_to_server(
        service, server)
    listen_addr = params.task_address + ":" + params.task_port
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

    args = parser.parse_args()

    asyncio.run(main(args))
