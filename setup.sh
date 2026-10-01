#!/bin/sh
# =============================================================================
# setup.sh — operator helper for a local pyenv install of this checkout
# =============================================================================
#
# GENERAL PURPOSE:
# Select CPython 3.14 with `pyenv shell 3.14`, remove a previous VideoSpeed
# from that interpreter only, and install this checkout with pip so the console
# script can be tested.
# The video-speed program does not install or remove itself. You run this file.
# FFmpeg stays a system program on PATH. This script does not install it.
#
# Usage:
#   ./setup.sh
#   pyenv shell 3.14
#   video-speed --version
#
# requirement-python-packaging.md
# HOME stays the login home. This script does not assign HOME.
# =============================================================================

set -eu

ROOT=$(CDPATH= cd -P -- "$(dirname -- "$0")" && pwd)

if [ -z "${ROOT}" ] || [ "${ROOT}" = "/" ]; then
    printf 'error: refusing to use checkout root %s\n' "${ROOT:-empty}" >&2
    printf 'Next: run ./setup.sh from a VideoSpeed checkout\n' >&2
    exit 1
fi

HOME_RESOLVED=
if [ -n "${HOME:-}" ]; then
    if ! HOME_RESOLVED=$(CDPATH= cd -P -- "${HOME}" && pwd); then
        printf 'error: cannot resolve HOME\n' >&2
        exit 1
    fi
fi

if [ -n "${HOME_RESOLVED}" ] && [ "${ROOT}" = "${HOME_RESOLVED}" ]; then
    printf 'error: refusing to run when the checkout is the login home\n' >&2
    printf 'Next: run ./setup.sh inside the VideoSpeed project directory\n' >&2
    exit 1
fi

if [ ! -f "${ROOT}/pyproject.toml" ]; then
    printf 'error: pyproject.toml is missing under %s\n' "${ROOT}" >&2
    printf 'Next: run ./setup.sh from a VideoSpeed checkout\n' >&2
    exit 1
fi

# `pyenv shell` is the shell function installed by `pyenv init`. A /bin/sh
# script does not have that function, so define it and call it below.
# PYENV_SHELL=sh makes `pyenv sh-shell` print a POSIX export.
if ! command -v pyenv >/dev/null 2>&1; then
    printf 'error: pyenv is not on PATH\n' >&2
    printf 'Next: install pyenv, run: pyenv install 3.14\n' >&2
    exit 1
fi

pyenv() {
    pyenv_command=${1:-}
    if [ "$#" -gt 0 ]; then
        shift
    fi
    case "${pyenv_command}" in
        shell)
            pyenv_shell_exports=$(command pyenv sh-shell "$@") || return 1
            eval "${pyenv_shell_exports}"
            ;;
        *)
            command pyenv "${pyenv_command}" "$@"
            ;;
    esac
}

PYENV_SHELL=sh
export PYENV_SHELL

printf 'pyenv shell 3.14\n'
if ! pyenv shell 3.14; then
    printf 'error: pyenv shell 3.14 failed\n' >&2
    printf 'Next: install that version with: pyenv install 3.14\n' >&2
    exit 1
fi

if ! PY_BIN=$(pyenv which python3); then
    printf 'error: pyenv shell 3.14 did not select python3\n' >&2
    printf 'Next: run: pyenv install 3.14\n' >&2
    exit 1
fi

PY_VER=$("${PY_BIN}" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
if [ "${PY_VER}" != "3.14" ]; then
    printf 'error: pyenv shell 3.14 resolved Python %s at %s\n' "${PY_VER}" "${PY_BIN}" >&2
    printf 'Next: run: pyenv install 3.14\n' >&2
    exit 1
fi

if ! "${PY_BIN}" -m pip --version >/dev/null 2>&1; then
    printf 'error: %s has no pip module\n' "${PY_BIN}" >&2
    printf 'Next: reinstall that interpreter with: pyenv install 3.14\n' >&2
    exit 1
fi

if ! PY_PREFIX=$(pyenv prefix); then
    printf 'error: pyenv prefix failed after pyenv shell 3.14\n' >&2
    printf 'Next: run: pyenv install 3.14\n' >&2
    exit 1
fi

printf 'interpreter: %s\n' "${PY_BIN}"
printf 'prefix: %s\n' "${PY_PREFIX}"

# =============================================================================
# CIAO-Lite Protection Zone
# Resolve before delete. Allow only named leaves under this checkout.
# Do NOT simplify, refactor, or remove without explicit user instruction.
# This section exists for safety and anti-fragility reasons.
# =============================================================================
remove_named_leaf() {
    leaf=$1
    target="${ROOT}/${leaf}"
    if [ ! -e "${target}" ] && [ ! -L "${target}" ]; then
        return 0
    fi
    if ! resolved=$(CDPATH= cd -P -- "${target}" && pwd); then
        printf 'error: cannot resolve %s\n' "${target}" >&2
        printf 'Next: remove that path by hand only if you mean that exact leaf\n' >&2
        exit 1
    fi
    expected="${ROOT}/${leaf}"
    if [ "${resolved}" != "${expected}" ]; then
        printf 'error: refusing to remove %s (resolved %s)\n' "${target}" "${resolved}" >&2
        exit 1
    fi
    if [ -n "${HOME_RESOLVED}" ] && [ "${resolved}" = "${HOME_RESOLVED}" ]; then
        printf 'error: refusing to remove the login home\n' >&2
        exit 1
    fi
    if [ "${resolved}" = "${ROOT}" ] || [ "${resolved}" = "/" ]; then
        printf 'error: refusing to remove %s\n' "${resolved}" >&2
        exit 1
    fi
    rm -rf -- "${resolved}"
}

if "${PY_BIN}" -m pip show VideoSpeed >/dev/null 2>&1; then
    printf 'removing previous VideoSpeed from %s\n' "${PY_PREFIX}"
    "${PY_BIN}" -m pip uninstall -y VideoSpeed
fi

# The duration probe only uses VideoCapture. The Qt build of opencv-python
# needs libGL.so.1, which this script does not install. The headless wheel
# imports without that library. The two distributions both own cv2, so the
# GUI wheel has to go before the headless wheel can be installed.
if "${PY_BIN}" -m pip show opencv-python >/dev/null 2>&1; then
    printf 'removing opencv-python from %s\n' "${PY_PREFIX}"
    if ! "${PY_BIN}" -m pip uninstall -y opencv-python; then
        printf 'error: could not remove opencv-python\n' >&2
        printf 'Next: uninstall opencv-python from %s and retry ./setup.sh\n' "${PY_PREFIX}" >&2
        exit 1
    fi
fi

# Floor matches requirement-python-dependency-management / pyproject.toml.
cv_meets_floor() {
    "${PY_BIN}" -c '
import importlib.metadata as meta
try:
    raw = meta.version("opencv-python-headless")
except meta.PackageNotFoundError:
    raise SystemExit(1)
parts = []
for piece in raw.split("."):
    digits = ""
    for ch in piece:
        if ch.isdigit():
            digits += ch
        else:
            break
    if not digits:
        break
    parts.append(int(digits))
while len(parts) < 4:
    parts.append(0)
raise SystemExit(0 if tuple(parts[:4]) >= (5, 0, 0, 93) else 1)
'
}

if ! "${PY_BIN}" -c 'import cv2' >/dev/null 2>&1 || ! cv_meets_floor; then
    printf 'installing opencv-python-headless>=5.0.0.93 into %s\n' "${PY_PREFIX}"
    if ! "${PY_BIN}" -m pip install --no-cache-dir 'opencv-python-headless>=5.0.0.93'; then
        printf 'error: could not install opencv-python-headless>=5.0.0.93\n' >&2
        printf 'Next: install opencv-python-headless>=5.0.0.93 into %s and retry ./setup.sh\n' "${PY_PREFIX}" >&2
        exit 1
    fi
fi

# Status files use ChronicleLogger. The package install below is --no-deps,
# so this floor is installed here. See requirement-python-cli-logging.
if ! "${PY_BIN}" -c 'import importlib.metadata as m
parts = []
for piece in m.version("ChronicleLogger").split("."):
    digits = ""
    for ch in piece:
        if ch.isdigit():
            digits += ch
        else:
            break
    if not digits:
        break
    parts.append(int(digits))
while len(parts) < 3:
    parts.append(0)
raise SystemExit(0 if tuple(parts[:3]) >= (1, 3, 1) else 1)
' >/dev/null 2>&1; then
    printf 'installing ChronicleLogger>=1.3.1 into %s\n' "${PY_PREFIX}"
    if ! "${PY_BIN}" -m pip install --no-cache-dir 'ChronicleLogger>=1.3.1'; then
        printf 'error: could not install ChronicleLogger>=1.3.1\n' >&2
        printf 'Next: install ChronicleLogger>=1.3.1 into %s and retry ./setup.sh\n' "${PY_PREFIX}" >&2
        exit 1
    fi
fi

remove_named_leaf "build"
remove_named_leaf "dist"
remove_named_leaf "VideoSpeed.egg-info"
remove_named_leaf "src/VideoSpeed.egg-info"

# --no-deps: opencv-python-headless and ChronicleLogger are installed above.
# The checkout install must not ask the index to resolve them again.
printf 'installing this checkout into %s\n' "${PY_PREFIX}"
if ! "${PY_BIN}" -m pip install --no-cache-dir --force-reinstall --no-deps "${ROOT}"; then
    printf 'error: pip could not install this checkout\n' >&2
    printf 'Next: read the pip output above and retry ./setup.sh\n' >&2
    exit 1
fi

CONSOLE="${PY_PREFIX}/bin/video-speed"
if [ ! -x "${CONSOLE}" ]; then
    printf 'error: console script was not created at %s\n' "${CONSOLE}" >&2
    printf 'Next: read the pip output above and retry ./setup.sh\n' >&2
    exit 1
fi

if ! pyenv rehash; then
    printf 'warning: pyenv rehash failed\n' >&2
    printf 'Next: run pyenv rehash, then pyenv shell 3.14\n' >&2
fi

printf 'installed: '
"${CONSOLE}" --version
printf '\n'
printf 'This script ran: pyenv shell 3.14\n'
printf 'In the shell where you want the command:\n'
printf '  pyenv shell 3.14\n'
printf '  video-speed --version\n'
printf '  video-speed --help\n'
printf 'Direct path:\n'
printf '  %s --version\n' "${CONSOLE}"
printf 'FFmpeg is still required on PATH before a cut. This script does not install it.\n'

if ! "${PY_BIN}" -c 'import cv2' >/dev/null 2>&1; then
    printf 'warning: opencv-python-headless is installed but import cv2 failed\n' >&2
    printf 'Next: read the traceback from: %s -c '\''import cv2'\''\n' "${PY_BIN}" >&2
    printf 'This script does not install OS packages.\n' >&2
fi

if command -v video-speed >/dev/null 2>&1; then
    outside=$(command -v video-speed)
    shim_root=$(pyenv root)
    shim="${shim_root}/shims/video-speed"
    if [ "${outside}" != "${CONSOLE}" ] && [ "${outside}" != "${shim}" ]; then
        printf 'warning: PATH already has video-speed at %s\n' "${outside}" >&2
        printf 'Next: run pyenv shell 3.14 before typing video-speed\n' >&2
    fi
fi
