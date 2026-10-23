import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    default_file = os.path.join(
        get_package_share_directory("limo_nav_control"),
        "config",
        "waypoints_real.yaml",
    )
    return LaunchDescription(
        [
            DeclareLaunchArgument("waypoints_file", default_value=default_file),
            DeclareLaunchArgument("set_initial_pose", default_value="true"),
            DeclareLaunchArgument("timeout_seconds", default_value="600.0"),
            Node(
                package="limo_nav_control",
                executable="waypoint_mission",
                name="limo_waypoint_mission",
                output="screen",
                parameters=[
                    {
                        "waypoints_file": LaunchConfiguration("waypoints_file"),
                        "set_initial_pose": LaunchConfiguration("set_initial_pose"),
                        "timeout_seconds": LaunchConfiguration("timeout_seconds"),
                    }
                ],
            ),
        ]
    )
