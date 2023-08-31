from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
SLEEPING: StatusCode
WORKING: StatusCode

class HeartReply(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class HeartStatus(_message.Message):
    __slots__ = ["ip", "msg", "service_id", "status", "timestamp"]
    IP_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ip: str
    msg: str
    service_id: int
    status: StatusCode
    timestamp: int
    def __init__(self, service_id: _Optional[int] = ..., status: _Optional[_Union[StatusCode, str]] = ..., timestamp: _Optional[int] = ..., msg: _Optional[str] = ..., ip: _Optional[str] = ...) -> None: ...

class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
