#!/usr/bin/python3
# Copyright 2020, EAIBOT
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.conditions import IfCondition
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

import os


def generate_launch_description():
    share_dir = get_package_share_directory('ydlidar_ros2_driver')
    parameter_file = LaunchConfiguration('params_file')
    name = 'ydlidar_ros2_driver_node'

    params_declare = DeclareLaunchArgument('params_file',
                                           default_value=os.path.join(
                                               share_dir, 'params', 'ydlidar.yaml'),
                                           description='FPath to the ROS2 parameters file to use.')

    publish_tf_declare = DeclareLaunchArgument(
        'publish_tf', default_value='true',
        description='Publish the static base_link to laser_link transform.')
    laser_x_declare = DeclareLaunchArgument('laser_x', default_value='0.0')
    laser_y_declare = DeclareLaunchArgument('laser_y', default_value='0.0')
    laser_z_declare = DeclareLaunchArgument('laser_z', default_value='0.02')
    laser_roll_declare = DeclareLaunchArgument('laser_roll', default_value='0.0')
    laser_pitch_declare = DeclareLaunchArgument('laser_pitch', default_value='0.0')
    laser_yaw_declare = DeclareLaunchArgument('laser_yaw', default_value='0.0')
    base_frame_declare = DeclareLaunchArgument('base_frame', default_value='base_link')
    laser_frame_declare = DeclareLaunchArgument('laser_frame', default_value='laser_link')

    driver_node = LifecycleNode(package='ydlidar_ros2_driver',
                                executable='ydlidar_ros2_driver_node',
                                name='ydlidar_ros2_driver_node',
                                output='screen',
                                emulate_tty=True,
                                parameters=[
                                    parameter_file,
                                    {'frame_id': LaunchConfiguration('laser_frame')},
                                ],
                                namespace='/',
                                )
    tf2_node = Node(package='tf2_ros',
                    executable='static_transform_publisher',
                    name='static_tf_pub_laser',
                    condition=IfCondition(LaunchConfiguration('publish_tf')),
                    arguments=[
                        LaunchConfiguration('laser_x'),
                        LaunchConfiguration('laser_y'),
                        LaunchConfiguration('laser_z'),
                        LaunchConfiguration('laser_yaw'),
                        LaunchConfiguration('laser_pitch'),
                        LaunchConfiguration('laser_roll'),
                        LaunchConfiguration('base_frame'),
                        LaunchConfiguration('laser_frame'),
                    ],
                    )

    return LaunchDescription([
        params_declare,
        publish_tf_declare,
        laser_x_declare,
        laser_y_declare,
        laser_z_declare,
        laser_roll_declare,
        laser_pitch_declare,
        laser_yaw_declare,
        base_frame_declare,
        laser_frame_declare,
        driver_node,
        tf2_node,
    ])
