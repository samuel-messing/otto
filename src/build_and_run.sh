#!/bin/bash
set -e

# Builds entire project and runs the server.

# TODO - check that we're running in top-level dir.
# TODO - kill existing server first.

function install_command() {
  if [[ ! $(command -v $1) ]]; then
    echo "[one-time] Installing $1";
    sudo apt-get install $2
  fi
}

install_command 'clang-format' 'clang-format'
install_command 'protoc' 'protobuf-compiler'
install_command 'virtualenv' 'virtualenv'

function make_dir() {
  if [[ ! -d $1 ]]; then
    echo "[one-time] Creating local $1/ directory";
    mkdir $1
  fi
}

make_dir 'db'
make_dir 'logs'

readonly REPO_LOCATION="/home/pi/otto"
readonly ROOT="src"
readonly CONFIGS_ROOT="configs"
readonly DB_ROOT="db"
readonly GENFILES_ROOT="${ROOT}/genfiles"
readonly VIRTUALENV_ROOT="otto-env"
readonly CLEANING__________="Cleaning................."
readonly SOURCE_VIRTUALENV_="Sourcing virutalenv......"
readonly INSTALL_VIRTUALENV="Installing virtualenv...."
readonly FORMAT_PYTHON_____="Formatting python........"
readonly FORMAT_PROTOS_____="Formatting protos........"
readonly BUILD_PROTOS______="Building protos.........."
readonly START_SERVER______="Starting server.........."
readonly EXIT_VIRTUALENV___="Exiting virtualenv......."
readonly DONE="...done!"

# DEFAULTS ===========================================
readonly DEFAULT_CONFIG="${CONFIGS_ROOT}/p0_v5.pbtxt"
readonly DEFAULT_DB_PATH="${DB_ROOT}/otto.db"
readonly DEFAULT_LOGGING_CONFIG="${CONFIGS_ROOT}/p0_v0.logging.config"

# HACK: To install as a systemd service, ensure we're running in the repo.
pushd "${REPO_LOCATION}"

# CLEANING ===========================================
echo -n "${CLEANING__________}"
rm -f "${GENFILES_ROOT}/*"
rm -f "${ROOT}/*.pyc"
touch "${GENFILES_ROOT}/__init__.py"
echo "${DONE}"

# VIRTUALENV =========================================
if [ ! -d "${VIRTUALENV_ROOT}" ]; then
	echo "No virtualenv found at ${VIRTUALENV_ROOT}!"
	echo "${INSTALL_VIRTUALENV}"
	virtualenv -p python3 otto-env
	# activate is idempotent
	. otto-env/bin/activate
	pip install -r "${ROOT}/requirements.txt"
	echo "${DONE}"
fi
function finish {
	echo "Server killed!"
	echo -n "${EXIT_VIRTUALENV___}"
	deactivate
	echo "${DONE}"
	echo "\"This is Otto, signing off!\" ~ Otto"
}
trap finish EXIT
echo -n "${SOURCE_VIRTUALENV_}"
# activate is idempotent
. otto-env/bin/activate
#pip install -r "${ROOT}/requirements.txt"
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
PYTHONPATH="${GENFILES_ROOT}" python3 ${ROOT}/app.py \
    --config_file="${DEFAULT_CONFIG}" \
    --db_file="${DEFAULT_DB_PATH}" \
    --logging_config_file="${DEFAULT_LOGGING_CONFIG}"
