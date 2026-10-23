import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    base_launch = os.path.join(
        get_package_share_directory("limo_base"), "launch", "limo_base.launch.py"
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("port_name", default_value="ttyTHS0"),
            DeclareLaunchArgument("odom_frame", default_value="odom"),
            DeclareLaunchArgument("base_frame", default_value="base_link"),
            DeclareLaunchArgument("publish_odom_tf", default_value="true"),
            DeclareLaunchArgument("use_mecanum", default_value="true"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(base_launch),
                launch_arguments={
                    "port_name": LaunchConfiguration("port_name"),
                    "odom_frame": LaunchConfiguration("odom_frame"),
                    "base_frame": LaunchConfiguration("base_frame"),
                    "pub_odom_tf": LaunchConfiguration("publish_odom_tf"),
                    "use_mecanum": LaunchConfiguration("use_mecanum"),
                }.items(),
            ),
        ]
    )
