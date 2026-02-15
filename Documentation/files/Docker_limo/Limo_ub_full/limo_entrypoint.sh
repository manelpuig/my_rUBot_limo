#!/bin/bash
set -e

# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

# source additional workspace setup
if [ -f "/root/limo_pi/install/setup.bash" ]; then
    source "/root/limo_pi/install/setup.bash"
fi

echo "ROS_DOMAIN_ID=$ROS_DOMAIN_ID"
echo "RMW_IMPLEMENTATION=$RMW_IMPLEMENTATION"
echo "ROS_AUTOMATIC_DISCOVERY_RANGE=$ROS_AUTOMATIC_DISCOVERY_RANGE"
echo "ROS_STATIC_PEERS=$ROS_STATIC_PEERS"

exec "$@"
