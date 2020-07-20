#!/bin/bash

PROTO_EXECUTABLE_DIR="$1"
PROTO_SRC_DIR=./
PROTO_SRC_NAME=ChatPrototypes.proto
PROTO_DEST_JAVA=../java/api/src/main/java/
PROTO_DEST_PYTHON=../MQTT_Chat_Library/mqtt_chat_library/

# Option 1
if [ $# -eq 2 ]; then
	for filename in	$PROTO_SRC_DIR*.proto; do
		$($PROTO_EXECUTABLE_DIR"protoc" --proto_path=$PROTO_SRC_DIR --java_out=$PROTO_DEST_JAVA "$filename")
		$($PROTO_EXECUTABLE_DIR"protoc" --proto_path=$PROTO_SRC_DIR --python_out=$PROTO_DEST_PYTHON "$filename")
	done
else
	for filename in $PROTO_SRC_DIR*.proto; do
		$(protoc --proto_path=$PROTO_SRC_DIR --java_out=$PROTO_DEST_JAVA "$filename")
		$(protoc --proto_path=$PROTO_SRC_DIR --python_out=$PROTO_DEST_PYTHON "$filename")
	done
fi
