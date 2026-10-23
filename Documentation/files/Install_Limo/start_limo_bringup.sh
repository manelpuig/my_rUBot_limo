#!/usr/bin/env bash

set -euo pipefail

: "${LIMO_WORKSPACE:=/home/agilex/limo_refactor_ws}"
: "${LIMO_BASE_PORT:=ttyTHS0}"
: "${LIMO_USE_MECANUM:=true}"
: "${LIMO_USE_LIDAR:=true}"
: "${LIMO_USE_CAMERA:=true}"
: "${LIMO_USE_RF2O:=false}"
: "${LIMO_PUBLISH_ODOM_TF:=true}"
: "${LIMO_PUBLISH_CAMERA_MOUNT_TF:=false}"

source /opt/ros/foxy/setup.bash
source "${LIMO_WORKSPACE}/install/setup.bash"

cd "${LIMO_WORKSPACE}"

exec ros2 launch limo_bringup limo_robot_bringup.launch.py \
  base_port:="${LIMO_BASE_PORT}" \
  use_mecanum:="${LIMO_USE_MECANUM}" \
  use_lidar:="${LIMO_USE_LIDAR}" \
  use_camera:="${LIMO_USE_CAMERA}" \
  use_rf2o:="${LIMO_USE_RF2O}" \
  publish_odom_tf:="${LIMO_PUBLISH_ODOM_TF}" \
  publish_camera_mount_tf:="${LIMO_PUBLISH_CAMERA_MOUNT_TF}"
