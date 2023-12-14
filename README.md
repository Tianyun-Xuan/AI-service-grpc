# AI-service-grpc

## How to use
    1. install dependency and build proto file
        ./build.sh
    2. change parameters in file [task_method.py]
        {docker_name}
        {scripte_name}
    3. change ip_address and port in file [async_ai_grpc.py]
        {uuid} 
        {heartbeat_address}
        {heartbeat_port}
        {task_address}
        {task_port}
        {log_dir}

## Update logs
### [1.0.1] 04-09-2023
    1. 把方法入口包装单独拿出来，方便部署时修改
    2. 修改了任务池中的Exception逻辑
    3. 增加了对于Exception的单元测试

### [1.0.2] 18-09-2023
    1. 修复了method_wrapper 引用文件错误的问题
    2. 修复了心跳传输的IP地址不正确的问题

### [1.0.3] 14-12-2023
    1. 再增加了一层包装可以运行docker内脚本
    2. 输入参数使用了base64编码解码