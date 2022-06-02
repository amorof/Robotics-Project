import rclpy
from rclpy.node import Node
from rclpy.task import Future

import sys
from math import pow, atan2, sqrt

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from turtlesim.msg import Pose


class Move2GoalNode(Node):
    def __init__(self ):
        super().__init__('move2goal')
        self.goal = Twist()
        self.vel_publisher = self.create_publisher(Twist, '/robo1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(Twist, '/cmd_vel', self.vel_callback, 10)
    
    def start_moving(self):
        self.timer = self.create_timer(0.1, self.move_callback)
        self.done_future = Future()
        return self.done_future
        
    def vel_callback(self, msg):
        self.goal = Twist()
        self.vel_publisher.publish(msg)
            

        
    def move_callback(self):
        """Callback called periodically by the timer to publish a new command."""
        
        if self.goal is None:
            # Wait until we receive the current pose of the turtle for the first time
            return
        
        self.vel_publisher.publish(self.goal)
            
            # Mark the future as completed, which will shutdown the node

def main():
    # Get the input from the user.
    

    # Initialize the ROS client library
    rclpy.init(args=sys.argv)
    
    # Create an instance of your node class
    node = Move2GoalNode()
    done = node.start_moving()
    
    # Keep processings events until the turtle has reached the goal
    rclpy.spin_until_future_complete(node, done)
    
    # Alternatively, if you don't want to exit unless someone manually shuts down the node
    # rclpy.spin(node)


if __name__ == '__main__':
    main()

