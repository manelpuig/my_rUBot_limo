#!/usr/bin/env bash

set -u

status=0

check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    printf '[OK] command: %s\n' "$1"
  else
    printf '[MISSING] command: %s\n' "$1"
    status=1
  fi
}

check_device() {
  if [[ -e "$1" ]]; then
    if [[ -r "$1" && -w "$1" ]]; then
      printf '[OK] device: %s (read/write)\n' "$1"
    else
      printf '[WARN] device: %s exists but lacks read/write permission\n' "$1"
      status=1
    fi
  else
    printf '[MISSING] device: %s\n' "$1"
    status=1
  fi
}

printf '%s\n' 'LIMO Pro native Foxy preflight'
printf 'OS: '
grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null || true
printf 'Architecture: %s\n' "$(uname -m)"
printf 'ROS_DISTRO: %s\n' "${ROS_DISTRO:-<unset>}"
printf 'RMW_IMPLEMENTATION: %s\n' "${RMW_IMPLEMENTATION:-<default>}"
printf 'ROS_DOMAIN_ID: %s\n' "${ROS_DOMAIN_ID:-0 (default)}"

if [[ "${ROS_DISTRO:-}" != "foxy" ]]; then
  printf '%s\n' '[WARN] Expected ROS_DISTRO=foxy on the robot.'
  status=1
fi

check_command ros2
check_command colcon
check_device "${LIMO_BASE_DEVICE:-/dev/ttyTHS0}"
check_device "${LIMO_LIDAR_DEVICE:-/dev/ydlidar}"

if command -v lsusb >/dev/null 2>&1; then
  if lsusb | grep -qiE '2bc5|Orbbec'; then
    printf '%s\n' '[OK] Orbbec USB device detected.'
  else
    printf '%s\n' '[WARN] No Orbbec USB device detected.'
    status=1
  fi
else
  printf '%s\n' '[WARN] lsusb is unavailable; camera detection skipped.'
fi

exit "$status"
