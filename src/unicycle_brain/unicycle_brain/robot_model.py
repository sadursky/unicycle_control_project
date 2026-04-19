#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class RobotModel(Node):
    def __init__(self):
        super().__init__('robot_model')

        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        self.timer = self.create_timer(0.01, self.update)

        # stan
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # sterowanie
        self.v = 0.0
        self.omega = 0.0

        self.dt = 0.01

        self.tf_broadcaster = TransformBroadcaster(self)

    def cmd_callback(self, msg: Twist):
        self.v = msg.linear.x
        self.omega = msg.angular.z

    def update(self):
        # integracja
        self.x += self.v * math.cos(self.theta) * self.dt
        self.y += self.v * math.sin(self.theta) * self.dt
        self.theta += self.omega * self.dt

        # normalizacja kąta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

        # quaternion (NAJPIERW!)
        q = Quaternion()
        q.z = math.sin(self.theta / 2.0)
        q.w = math.cos(self.theta / 2.0)

        # ===== TF =====
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = q

        self.tf_broadcaster.sendTransform(t)

        # ===== ODOM =====
        odom = Odometry()
        odom.header.stamp = t.header.stamp
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = q

        odom.twist.twist.linear.x = self.v
        odom.twist.twist.angular.z = self.omega

        self.odom_pub.publish(odom)

        # (opcjonalnie rzadziej loguj, bo spamuje terminal)
        # self.get_logger().info(f"x: {self.x:.2f}, y: {self.y:.2f}, theta: {self.theta:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = RobotModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
