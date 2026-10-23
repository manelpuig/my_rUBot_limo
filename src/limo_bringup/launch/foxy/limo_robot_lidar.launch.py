import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    driver_share = get_package_share_directory("ydlidar_ros2_driver")
    driver_launch = os.path.join(driver_share, "launch", "ydlidar.launch.py")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "params_file",
                default_value=os.path.join(driver_share, "params", "ydlidar.yaml"),
            ),
            DeclareLaunchArgument("publish_lidar_tf", default_value="true"),
            DeclareLaunchArgument("base_frame", default_value="base_link"),
            DeclareLaunchArgument("laser_frame", default_value="laser_link"),
            DeclareLaunchArgument("laser_x", default_value="0.0"),
            DeclareLaunchArgument("laser_y", default_value="0.0"),
            DeclareLaunchArgument(
                "laser_z",
                default_value="0.02",
                description="Placeholder from the current driver; measure before release.",
            ),
            DeclareLaunchArgument("laser_roll", default_value="0.0"),
            DeclareLaunchArgument("laser_pitch", default_value="0.0"),
            DeclareLaunchArgument("laser_yaw", default_value="0.0"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(driver_launch),
                launch_arguments={
                    "params_file": LaunchConfiguration("params_file"),
                    "publish_tf": LaunchConfiguration("publish_lidar_tf"),
                    "base_frame": LaunchConfiguration("base_frame"),
                    "laser_frame": LaunchConfiguration("laser_frame"),
                    "laser_x": LaunchConfiguration("laser_x"),
                    "laser_y": LaunchConfiguration("laser_y"),
                    "laser_z": LaunchConfiguration("laser_z"),
                    "laser_roll": LaunchConfiguration("laser_roll"),
                    "laser_pitch": LaunchConfiguration("laser_pitch"),
                    "laser_yaw": LaunchConfiguration("laser_yaw"),
                }.items(),
            ),
        ]
    )
