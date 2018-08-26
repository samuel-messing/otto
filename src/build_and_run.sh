#!/bin/bash
set -ex

# Builds entire project and runs the server.

# TODO - check that we're running in top-level dir.
# TODO - run server.
# TODO - kill existing server first.

readonly ROOT="src"
readonly GENFILES_ROOT="${ROOT}/genfiles"
readonly VIRTUALENV_ROOT="otto-env"

# CLEANING ===========================================
rm -f "${GENFILES_ROOT}/*"
touch "${GENFILES_ROOT}/__init__.py"

# VIRTUALENV =========================================
if [ ! -d "${VIRTUALENV_ROOT}" ]; then
	virtualenv otto-env
	# activate is idempotent
	. otto-env/bin/activate
	pip install -r "${ROOT}/requirements.txt"
fi

# activate is idempotent
. otto-env/bin/activate


# BUILDING PROTOS ====================================
protoc -I="${ROOT}/proto/" \
	--python_out="${ROOT}/genfiles/" \
	${ROOT}/proto/*

# RUNNING SERVER =====================================
PYTHONPATH="${GENFILES_ROOT}" python ${ROOT}/app.py
