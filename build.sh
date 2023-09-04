#!/bin/bash

# 获取grpc包的版本值
grpc_version=$(pip show grpcio | grep "Version" | awk '{print $2}')
python3_version=$(python3 --version 2>&1)
echo "Using python version : $python3_version, with grpc version: $grpc_version"

# 比较版本号
if [[ $(echo -e "$grpc_version\n1.48.0" | sort -V | head -n 1) == "$grpc_version" ]]; then
    # https://pypi.org/project/grpcio-tools/1.41.1/
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/ai_grpc_heartbeat.proto
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/ai_grpc_service.proto
else
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/ai_grpc_heartbeat.proto
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/ai_grpc_service.proto
fi
