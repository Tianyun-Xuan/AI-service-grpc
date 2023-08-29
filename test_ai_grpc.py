import pytest
from unittest import mock
from ai_grpc import AIGrpcTaskService
from generated import ai_grpc_service_pb2

@pytest.fixture
def task_service():
    return AIGrpcTaskService("localhost", "50051", 1)

@pytest.mark.asyncio
async def test_send_task(task_service):
    request = mock.Mock()
    context = mock.Mock()
    response = await task_service.SendTask(request, context)
    assert response.code == ai_grpc_service_pb2.ResponseCode.OK

@pytest.mark.asyncio
async def test_insert_tasks(task_service):
    await task_service.insert_tasks()
    # Add assertions here to test the behavior of the insert_tasks() method

@pytest.mark.asyncio
async def test_process_tasks(task_service):
    await task_service.process_tasks()
    # Add assertions here to test the behavior of the process_tasks() method

# Add more tests as needed