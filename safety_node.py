#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time

import numpy as np
# TODO: include needed ROS msg type headers and libraries
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive


class SafetyNode(Node):
    """
    The class that handles emergency braking.
    """
    def __init__(self):
        super().__init__('safety_node')
        self.safety_pub = self.create_publisher(AckermannDriveStamped, '/drive', 10)
        self.safety_scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.safety_odom_sub = self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 10)
        """
        One publisher should publish to the /drive topic with a AckermannDriveStamped drive message.

        You should also subscribe to the /scan topic to get the LaserScan messages and
        the /ego_racecar/odom topic to get the current speed of the vehicle.

        The subscribers should use the provided odom_callback and scan_callback as callback methods

        NOTE that the x component of the linear velocity in odom is the speed
        """
        self.speed = 0.0
        self.prev_time = None
        self.get_logger().info('Safety Node has started')
        # TODO: create ROS subscribers and publishers.

    def odom_callback(self, odom_msg):
        # update current speed
        velocity = odom_msg.twist.twist.linear
        self.speed = velocity.x
        self.get_logger().info('\nCurrent speed: "%.3f"' %self.speed)

    def scan_callback(self, scan_msg):
        
        #calculate TTC
        index = 534
        cur_range = scan_msg.ranges[index]
        cur_angle = scan_msg.angle_min + scan_msg.angle_increment * index

        range_dif = self.speed * np.cos(cur_angle)

        if self.speed > 0.001:
            iTTC = cur_range / range_dif
        else:
            iTTC = float('inf')  # Set iTTC to infinity when speed is zero

        self.get_logger().info('\n\nChosen range = %.3f' %cur_range + ' and Difference = %.3f' %range_dif)
    
        self.get_logger().info('\niTTC = %.3f \n' %iTTC)

        # publish command to brake
        drive_msg = AckermannDriveStamped()
        if iTTC < 1:
            drive_msg.drive.speed = 0.0
            self.safety_pub.publish(drive_msg)
            self.get_logger().info('\nCar stopped due to iTTC\n')
        pass

def main(args=None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    rclpy.spin(safety_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    safety_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()