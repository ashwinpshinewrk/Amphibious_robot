import rclpy
from geometry_msgs.msg import Twist


HALF_DISTANCE_BETWEEN_WHEELS = 0.202
WHEEL_RADIUS = 0.090
#TODO : arbitary values , change them

MAX_SCREW_SPEED = 10.0 #rad/s
LINEAR_GAIN = 10.0 #rad/s
ANGULAR_GAIN = 5.0 #rad /s

FORWARD_SIGN_LEFT = 1.0
FORWARD_SIGN_RIGHT = -1.0

YAW_SIGN_LEFT = 1.0
YAW_SIGN_RIGHT = 1.0


def clamp(x,limit):
    return max(-limit, min(limit,x))

class PlainDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__left_motor = self.__robot.getDevice('left_screw_motor')
        self.__right_motor = self.__robot.getDevice('right_screw_motor')

        if self.__left_motor is None or self.__right_motor is None:
            print("[ERROR] Device 'left_screw' or 'right_screw' not found on the Webots robot model!")
            print("Please verify the 'name' string field of your RotationalMotors inside Webots.")
            self.__left_motor = None
            self.__right_motor = None
        else:
            # Configure motors for velocity control mode only if they exist
            self.__left_motor.setPosition(float('inf'))
            self.__left_motor.setVelocity(0)
            self.__right_motor.setPosition(float('inf'))
            self.__right_motor.setVelocity(0)
#        self.__left_motor.setPosition(float('inf'))
 #       self.__left_motor.setVelocity(0)

  #      self.__right_motor.setPosition(float('inf'))
   #     self.__right_motor.setVelocity(0)

        self.__target_twist = Twist()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('amphi_sim_plain_driver')
        self.__node.create_subscription(Twist,'cmd_vel', self.__cmd_vel_callback,1)

    def __cmd_vel_callback(self,twist):
        self.__target_twist = twist

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        forward_speed = self.__target_twist.linear.x
        angular_speed = self.__target_twist.angular.z

        command_motor_left = (forward_speed - angular_speed * HALF_DISTANCE_BETWEEN_WHEELS) / WHEEL_RADIUS

        command_motor_left = FORWARD_SIGN_LEFT * LINEAR_GAIN * forward_speed + YAW_SIGN_LEFT * ANGULAR_GAIN * angular_speed
        command_motor_right = FORWARD_SIGN_RIGHT * LINEAR_GAIN * forward_speed - YAW_SIGN_RIGHT * ANGULAR_GAIN * angular_speed
        self.__left_motor.setVelocity(clamp(command_motor_left,MAX_SCREW_SPEED))
        self.__right_motor.setVelocity(clamp(command_motor_right,MAX_SCREW_SPEED))

def main():
    print('Hi from amphi_plain_sim.')


if __name__ == '__main__':
    main()
