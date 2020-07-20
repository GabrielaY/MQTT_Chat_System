# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message_prototype.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message_prototype.proto',
  package='chat_message',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17message_prototype.proto\x12\x0c\x63hat_message\"A\n\x0b\x43hatMessage\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\t\x12\x11\n\ttimestamp\x18\x03 \x02(\t'
)




_CHATMESSAGE = _descriptor.Descriptor(
  name='ChatMessage',
  full_name='chat_message.ChatMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sender', full_name='chat_message.ChatMessage.sender', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='chat_message.ChatMessage.content', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='chat_message.ChatMessage.timestamp', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=41,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['ChatMessage'] = _CHATMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChatMessage = _reflection.GeneratedProtocolMessageType('ChatMessage', (_message.Message,), {
  'DESCRIPTOR' : _CHATMESSAGE,
  '__module__' : 'message_prototype_pb2'
  # @@protoc_insertion_point(class_scope:chat_message.ChatMessage)
  })
_sym_db.RegisterMessage(ChatMessage)


# @@protoc_insertion_point(module_scope)
