# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x12\x04grpc\"\x07\n\x05\x45mpty\"B\n\x04Note\x12\x12\n\nsendername\x18\x01 \x01(\t\x12\x15\n\rrecipientname\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\x1f\n\rLoginResponse\x12\x0e\n\x06result\x18\x01 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"3\n\rSignupRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\" \n\x0eSignupResponse\x12\x0e\n\x06result\x18\x01 \x01(\t2\xc1\x01\n\nChatServer\x12\'\n\nChatStream\x12\x0b.grpc.Empty\x1a\n.grpc.Note0\x01\x12#\n\x08SendNote\x12\n.grpc.Note\x1a\x0b.grpc.Empty\x12\x30\n\x05Login\x12\x12.grpc.LoginRequest\x1a\x13.grpc.LoginResponse\x12\x33\n\x06Signup\x12\x13.grpc.SignupRequest\x1a\x14.grpc.SignupResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=20
  _EMPTY._serialized_end=27
  _NOTE._serialized_start=29
  _NOTE._serialized_end=95
  _LOGINRESPONSE._serialized_start=97
  _LOGINRESPONSE._serialized_end=128
  _LOGINREQUEST._serialized_start=130
  _LOGINREQUEST._serialized_end=180
  _SIGNUPREQUEST._serialized_start=182
  _SIGNUPREQUEST._serialized_end=233
  _SIGNUPRESPONSE._serialized_start=235
  _SIGNUPRESPONSE._serialized_end=267
  _CHATSERVER._serialized_start=270
  _CHATSERVER._serialized_end=463
# @@protoc_insertion_point(module_scope)