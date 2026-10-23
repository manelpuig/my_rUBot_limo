#!/usr/bin/env python3
import math
import os
import time

import rclpy
import yaml
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from rclpy.node import Node


class WaypointMission(Node):
    def __init__(self):
        super().__init__("limo_waypoint_mission")
        self.declare_parameter("waypoints_file", "")
        self.declare_parameter("set_initial_pose", True)
        self.declare_parameter("timeout_seconds", 600.0)

        path = self.get_parameter("waypoints_file").value
        if not path or not os.path.isfile(path):
            raise FileNotFoundError(f"Waypoint file not found: {path}")

        with open(path, "r", encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
        if not data or "waypoints" not in data:
            raise ValueError("Waypoint YAML must contain a 'waypoints' list")

        self.initial_pose = data.get("initial_pose", [0.0, 0.0, 0.0])
        self.waypoints = data["waypoints"]
        self.set_pose = bool(self.get_parameter("set_initial_pose").value)
        self.timeout = float(self.get_parameter("timeout_seconds").value)
        self.navigator = BasicNavigator()

    def make_pose(self, values):
        if len(values) != 3:
            raise ValueError("Every pose must be [x, y, yaw_radians]")
        x, y, yaw = (float(value) for value in values)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    def run(self):
        if self.set_pose:
            self.navigator.setInitialPose(self.make_pose(self.initial_pose))

        self.get_logger().info("Waiting for Nav2 to become active")
        self.navigator.waitUntilNav2Active()

        poses = [self.make_pose(values) for values in self.waypoints]
        if not poses:
            self.get_logger().warning("The waypoint list is empty")
            return

        self.navigator.followWaypoints(poses)
        started = time.monotonic()
        feedback_time = started
        while not self.navigator.isTaskComplete():
            now = time.monotonic()
            if now - started > self.timeout:
                self.get_logger().error("Mission timeout; cancelling navigation")
                self.navigator.cancelTask()
                break
            if now - feedback_time >= 5.0:
                feedback = self.navigator.getFeedback()
                if feedback is not None:
                    self.get_logger().info(
                        f"Current waypoint: {feedback.current_waypoint + 1}/{len(poses)}"
                    )
                feedback_time = now
            time.sleep(0.1)

        self.get_logger().info(f"Mission result: {self.navigator.getResult()}")


def main(args=None):
    rclpy.init(args=args)
    node = WaypointMission()
    try:
        node.run()
    except KeyboardInterrupt:
        node.navigator.cancelTask()
    finally:
        node.navigator.destroy_node()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
