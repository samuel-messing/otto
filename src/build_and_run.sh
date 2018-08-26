#!/bin/bash
set -ex

# Builds entire project and runs the server.

# TODO - check that we're running in top-level dir.
# TODO - run server.
# TODO - kill existing server first.

readonly ROOT="src"

# Initial cleaning of old artifacts.
rm -f "${ROOT}/genfiles/*"

# Building protos.
protoc -I="${ROOT}/proto/" \
	--python_out="${ROOT}/genfiles/" \
	${ROOT}/proto/*
