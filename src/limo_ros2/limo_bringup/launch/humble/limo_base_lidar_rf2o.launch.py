from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    limo_base_dir = get_package_share_directory("limo_base")
    ydlidar_ros_dir = get_package_share_directory("ydlidar_ros2_driver")
    rf2o_dir = get_package_share_directory("rf2o_laser_odometry")

    limo_base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [limo_base_dir, "/launch", "/limo_base.launch.py"]
        ),
    )

    ydlidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [ydlidar_ros_dir, "/launch", "/ydlidar.launch.py"]
        ),
    )

    rf2o_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [rf2o_dir, "/launch", "/rf2o_laser_odometry.launch.py"]
        ),
    )

    return LaunchDescription(
        [
            limo_base_launch,
            ydlidar_launch,
            TimerAction(
                period=5.0,
                actions=[rf2o_launch],
            ),
        ]
    )