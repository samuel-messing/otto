#!/bin/bash
set -e

# Builds entire project and runs the server.

# TODO - check that we're running in top-level dir.
# TODO - kill existing server first.

readonly ROOT="src"
readonly CONFIGS_ROOT="configs"
readonly GENFILES_ROOT="${ROOT}/genfiles"
readonly VIRTUALENV_ROOT="otto-env"
readonly CLEANING__________="Cleaning................."
readonly SOURCE_VIRTUALENV_="Sourcing virutalenv......"
readonly INSTALL_VIRTUALENV="Installing virtualenv...."
readonly FORMAT_PYTHON_____="Formatting python........"
readonly FORMAT_PROTOS_____="Formatting protos........"
readonly BUILD_PROTOS______="Building protos.........."
readonly START_SERVER______="Starting server.........."
readonly DONE="...done!"

# DEFAULTS ===========================================
readonly DEFAULT_CONFIG="${CONFIGS_ROOT}/p0_v0.pbtxt"
readonly DEFAULT_LOGGING_CONFIG="${CONFIGS_ROOT}/p0_v0.logging.config"

# CLEANING ===========================================
echo -n "${CLEANING__________}"
rm -f "${GENFILES_ROOT}/*"
rm -f ${ROOT}/*.pyc
touch "${GENFILES_ROOT}/__init__.py"
echo "${DONE}"

# VIRTUALENV =========================================
if [ ! -d "${VIRTUALENV_ROOT}" ]; then
	echo "No virtualenv found at ${VIRTUALENV_ROOT}!"
	echo -n "${INSTALL_VIRTUALENV}"
	virtualenv otto-env
	# activate is idempotent
	. otto-env/bin/activate
	pip install -r "${ROOT}/requirements.txt"
	echo "${DONE}"
fi
# activate is idempotent
echo -n "${SOURCE_VIRTUALENV_}"
. otto-env/bin/activate
echo "${DONE}"

# FORMATTING CODE ====================================
if [[ ! -z "$(git diff --name-only | grep .py)" ]]; then
  echo -n "${FORMAT_PYTHON_____}"
  autopep8 --in-place --recursive src/
  echo "${DONE}"
fi
if [[ ! -z "$(git diff --name-only | grep .proto)" ]]; then
  echo -n "${FORMAT_PROTOS_____}"
  clang-format -i src/proto/*
  echo "${DONE}"
fi

# BUILDING PROTOS ====================================
echo -n "${BUILD_PROTOS______}"
protoc -I="${ROOT}/proto/" \
	--python_out="${ROOT}/genfiles/" \
	${ROOT}/proto/*
echo "${DONE}"

# RUNNING SERVER =====================================
echo "${START_SERVER______}"
PYTHONPATH="${GENFILES_ROOT}" python ${ROOT}/app.py \
    --config_file="${DEFAULT_CONFIG}" \
    --logging_config_file="${DEFAULT_LOGGING_CONFIG}"
