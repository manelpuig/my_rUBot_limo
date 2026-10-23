from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    rf2o_dir = get_package_share_directory("rf2o_laser_odometry")
    ydlidar_ros_dir = get_package_share_directory("ydlidar_ros2_driver")
    limo_base_dir = get_package_share_directory("limo_base")
    orbbec_camera_dir = get_package_share_directory("orbbec_camera")

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [limo_base_dir, "/launch", "/limo_base.launch.py"]
                ),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [rf2o_dir, "/launch", "/rf2o_laser_odometry.launch.py"]
                ),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [ydlidar_ros_dir, "/launch", "/ydlidar.launch.py"]
                ),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [orbbec_camera_dir, "/launch", "/dabai.launch.py"]
                ),
                launch_arguments={
                'color_width': '640',
                'color_height': '480',
                'color_fps': '30', 
                'depth_width': '640',
                'depth_height': '400',
                'depth_fps': '30',
                'ir_width': '640',
                'ir_height': '400',
                'ir_fps': '30'
                }.items(),
            ),
        ]
    )

