import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

            DeclareLaunchArgument(
                'laser_scan_topic', default_value='/scan',
                description='LaserScan topic used by RF2O.'),
            DeclareLaunchArgument(
                'odom_topic', default_value='/rf2o/odom',
                description='Odometry topic published by RF2O.'),
            DeclareLaunchArgument(
                'publish_tf', default_value='false',
                description='Publish odom_frame_id to base_frame_id TF.'),
            DeclareLaunchArgument('base_frame_id', default_value='base_link'),
            DeclareLaunchArgument('odom_frame_id', default_value='odom'),

            Node(
                package='rf2o_laser_odometry',
                executable='rf2o_laser_odometry_node',
                name='rf2o_laser_odometry',
                output='screen',
                parameters=[{
                    'laser_scan_topic' : LaunchConfiguration('laser_scan_topic'),
                    'odom_topic' : LaunchConfiguration('odom_topic'),
                    'publish_tf' : LaunchConfiguration('publish_tf'),
                    'base_frame_id' : LaunchConfiguration('base_frame_id'),
                    'odom_frame_id' : LaunchConfiguration('odom_frame_id'),
                    'init_pose_from_topic' : '',
                    'freq' : 10.0}],
            ),
    ])
