import asyncio
import logging

import grpc
from generated import ai_grpc_heartbeat_pb2
from generated import ai_grpc_heartbeat_pb2_grpc


class Greeter(ai_grpc_heartbeat_pb2_grpc.AIGprcHeartServicer):
    async def HeartBeat(
        self,
        request: ai_grpc_heartbeat_pb2.HeartStatus,
        context: grpc.aio.ServicerContext,
    ) -> ai_grpc_heartbeat_pb2.HeartReply:
        print("HeartBeat: %s" % request.status)
        return ai_grpc_heartbeat_pb2.HeartReply(msg="request: %s" % request.status)


async def serve() -> None:
    server = grpc.aio.server()
    ai_grpc_heartbeat_pb2_grpc.add_AIGprcHeartServicer_to_server(
        Greeter(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
