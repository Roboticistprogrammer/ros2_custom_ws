#!/usr/bin/env bash

# Source this file to export Isaac Sim paths, or execute it to start the
# warehouse USD configured by WAREHOUSE_USD.

export PYTHONPATH="${PYTHONPATH:-}:/home/amir/Downloads/librealsense/build/Release"
export ISAAC_ROS_WS="${ISAAC_ROS_WS:-${HOME}/workspaces/isaac_ros-dev/}"
export ISAACSIM_PATH="${ISAACSIM_PATH:-/mnt/e/isaacsim}"
export ISAACSIM_PYTHON="${ISAACSIM_PYTHON:-${ISAACSIM_PATH}/python.bat}"
export ISAACSIM="${ISAACSIM:-${ISAACSIM_PATH}/isaac-sim.bat}"

_yolov11_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_yolov11_is_sourced() {
    [[ "${BASH_SOURCE[0]}" != "${0}" ]]
}

_yolov11_return_or_exit() {
    local code="$1"

    if _yolov11_is_sourced; then
        return "${code}"
    fi

    exit "${code}"
}

_yolov11_usage() {
    printf '%s\n' "Usage:"
    printf '%s\n' "  source scripts/launch.bash"
    printf '%s\n' "  WAREHOUSE_USD=/path/to/world.usd scripts/launch.bash [start]"
}

_yolov11_start_isaac_sim() {
    local open_stage_script="${_yolov11_script_dir}/open_warehouse_stage.py"

    if [[ -z "${WAREHOUSE_USD:-}" ]]; then
        printf '%s\n' "ERROR: WAREHOUSE_USD is not set."
        printf '%s\n' "Set it to the Isaac Sim warehouse USD path before starting."
        return 1
    fi

    if [[ ! -e "${ISAACSIM}" ]]; then
        printf '%s\n' "ERROR: ISAACSIM does not exist: ${ISAACSIM}"
        return 1
    fi

    if [[ ! -f "${open_stage_script}" ]]; then
        printf '%s\n' "ERROR: open-stage helper not found: ${open_stage_script}"
        return 1
    fi

    printf '%s\n' "Starting Isaac Sim: ${ISAACSIM}"
    printf '%s\n' "Opening warehouse stage: ${WAREHOUSE_USD}"
    "${ISAACSIM}" --exec "${open_stage_script}"
}

if _yolov11_is_sourced; then
    printf '%s\n' "Isaac Sim environment exported."
    printf '%s\n' "Set WAREHOUSE_USD and run scripts/launch.bash start to open a world."
else
    case "${1:-start}" in
        start)
            _yolov11_start_isaac_sim
            _yolov11_return_or_exit "$?"
            ;;
        help|--help|-h)
            _yolov11_usage
            ;;
        *)
            printf '%s\n' "ERROR: unknown command: ${1}"
            _yolov11_usage
            _yolov11_return_or_exit 2
            ;;
    esac
fi
