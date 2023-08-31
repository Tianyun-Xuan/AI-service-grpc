from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DEFAULT: ActionCode
DESCRIPTOR: _descriptor.FileDescriptor
Error: ResponseCode
OK: ResponseCode

class TaskReply(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: ResponseCode
    def __init__(self, code: _Optional[_Union[ResponseCode, str]] = ...) -> None: ...

class TaskRequest(_message.Message):
    __slots__ = ["action", "msg"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    action: ActionCode
    msg: str
    def __init__(self, action: _Optional[_Union[ActionCode, str]] = ..., msg: _Optional[str] = ...) -> None: ...

class ActionCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ResponseCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
