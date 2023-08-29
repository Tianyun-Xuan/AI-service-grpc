mkdir -p generated
python3 -m grpc_tools.protoc -Iprotos --python_out=generated --pyi_out=generated --grpc_python_out=generated protos/ai_grpc_heartbeat.proto
python3 -m grpc_tools.protoc -Iprotos --python_out=generated --pyi_out=generated --grpc_python_out=generated protos/ai_grpc_service.proto
