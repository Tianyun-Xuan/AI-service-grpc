mkdir -p .
python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/ai_grpc_heartbeat.proto
python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/ai_grpc_service.proto
