import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("limo_navigation2")
    nav2_share = get_package_share_directory("nav2_bringup")

    map_file = LaunchConfiguration("map")
    params_file = LaunchConfiguration("params_file")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "map",
                default_value=os.path.join(package_share, "map", "limo_map.yaml"),
                description="Absolute path to a map created with Cartographer",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=os.path.join(package_share, "param", "limo_real.yaml"),
            ),
            DeclareLaunchArgument("use_sim_time", default_value="false"),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_share, "launch", "bringup_launch.py")
                ),
                launch_arguments={
                    "map": map_file,
                    "params_file": params_file,
                    "use_sim_time": use_sim_time,
                    "autostart": "true",
                }.items(),
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=[
                    "-d",
                    os.path.join(package_share, "rviz", "limo_navigation.rviz"),
                ],
                parameters=[{"use_sim_time": use_sim_time}],
                condition=IfCondition(use_rviz),
                output="screen",
            ),
        ]
    )
