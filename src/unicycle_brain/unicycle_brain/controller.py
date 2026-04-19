import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
import math

class Controller(Node):
    def __init__(self):
        super().__init__('controller')

        self.sub = self.create_subscription(
            Pose2D,
            '/target_pose',
            self.callback,
            10
        )

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.prev_x = None
        self.prev_y = None
        self.prev_theta = None

        self.dt = 0.01

    def callback(self, msg):
        x = msg.x
        y = msg.y
        theta = msg.theta

        if self.prev_x is None:
            self.prev_x = x
            self.prev_y = y
            self.prev_theta = theta
            return

        # numeryczne pochodne
        dx = (x - self.prev_x) / self.dt
        dy = (y - self.prev_y) / self.dt
        dtheta = (theta - self.prev_theta) / self.dt

        # prędkości referencyjne
        v_r = math.sqrt(dx**2 + dy**2)
        omega_r = dtheta

        cmd = Twist()
        cmd.linear.x = v_r
        cmd.angular.z = omega_r

        self.pub.publish(cmd)

        self.prev_x = x
        self.prev_y = y
        self.prev_theta = theta

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
