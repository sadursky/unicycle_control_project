#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
import math

class TrajectoryGenerator(Node):
    def __init__(self):
        super().__init__('trajectory_generator')

        # Publisher trajektorii zadanej
        self.pub = self.create_publisher(Pose2D, '/target_pose', 10)
        self.timer = self.create_timer(0.01, self.update)

        # Czas symulacji
        self.t = 0.0
        self.dt = 0.01

        # Parametry trajektorii (okrąg)
        self.R = 2.0
        self.omega = 0.2

    def update(self):
        self.t += self.dt

        x_d = self.R * math.cos(self.omega * self.t)
        y_d = self.R * math.sin(self.omega * self.t)
        theta_d = self.omega * self.t

        msg = Pose2D()
        msg.x = x_d
        msg.y = y_d
        msg.theta = theta_d
        self.get_logger().info(f"x: {x_d:.2f}, y: {y_d:.2f}, theta: {theta_d:.2f}")
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryGenerator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
