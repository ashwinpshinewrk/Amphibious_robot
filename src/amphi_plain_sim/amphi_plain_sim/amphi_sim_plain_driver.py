import rclpy
from geometry_msgs.msg import Twist

# ---- Geometry (from plain_world.wbt) ----
SCREW_Y = 0.20263            # lateral offset of each screw from the body centre (m)

# ---- Command -> screw spin ----
MAX_SCREW_SPEED = 30.0       # rad/s, matches maxVelocity in the world file
LINEAR_GAIN = 20.0           # screw rad/s per 1 m/s of cmd_vel.linear.x
ANGULAR_GAIN = 20.0          # screw rad/s per 1 rad/s of cmd_vel.angular.z

# Mirrored screws: opposite spin = forward, same spin = yaw.
# Flip these signs if the robot drives backward / turns the wrong way.
FORWARD_SIGN_LEFT = 1.0
FORWARD_SIGN_RIGHT = -1.0
YAW_SIGN_LEFT = 1.0
YAW_SIGN_RIGHT = 1.0

# ---- Emulated screw physics ----
# Axial thrust (N) produced per rad/s of screw spin.
# Left screw thrust = THRUST_PER_RAD * omega * THRUST_SIGN_LEFT, etc.
# Mirrored screws -> opposite sign convention so FORWARD spin gives +x thrust on both.
THRUST_PER_RAD = 2.0
THRUST_SIGN_LEFT = 1.0
THRUST_SIGN_RIGHT = -1.0

# Drag terms emulate the thread gripping the ground. Chosen so a cmd_vel of
# (v, w) settles near (v, w). Raise DRAG_Y for less sideways slip.
DRAG_X = 2.0 * THRUST_PER_RAD * LINEAR_GAIN                      # N per m/s
DRAG_Y = 300.0                                                    # N per m/s
DRAG_YAW = 2.0 * SCREW_Y * THRUST_PER_RAD * ANGULAR_GAIN         # N*m per rad/s


def clamp(x, limit):
    return max(-limit, min(limit, x))


class PlainDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__left_motor = self.__robot.getDevice('left_screw_motor')
        self.__right_motor = self.__robot.getDevice('right_screw_motor')
        if self.__left_motor is None or self.__right_motor is None:
            print("[ERROR] 'left_screw_motor' or 'right_screw_motor' not found in the Webots model!")
            self.__left_motor = self.__right_motor = None
        else:
            for m in (self.__left_motor, self.__right_motor):
                m.setPosition(float('inf'))
                m.setVelocity(0.0)

        # Needs supervisor TRUE on the Robot (already set in your world).
        self.__body = None
        if hasattr(self.__robot, 'getSelf'):
            self.__body = self.__robot.getSelf()
        if self.__body is None:
            print("[ERROR] Could not get the robot's own node; forces cannot be applied.")

        self.__target_twist = Twist()
        rclpy.init(args=None)
        self.__node = rclpy.create_node('amphi_sim_plain_driver')
        self.__node.create_subscription(Twist, 'cmd_vel', self.__cmd_vel_callback, 1)

    def __cmd_vel_callback(self, twist):
        self.__target_twist = twist

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)
        if self.__left_motor is None:
            return

        v = self.__target_twist.linear.x
        w = self.__target_twist.angular.z

        # 1) Screw spin commands
        left = FORWARD_SIGN_LEFT * LINEAR_GAIN * v + YAW_SIGN_LEFT * ANGULAR_GAIN * w
        right = FORWARD_SIGN_RIGHT * LINEAR_GAIN * v + YAW_SIGN_RIGHT * ANGULAR_GAIN * w
        left = clamp(left, MAX_SCREW_SPEED)
        right = clamp(right, MAX_SCREW_SPEED)
        self.__left_motor.setVelocity(left)
        self.__right_motor.setVelocity(right)

        if self.__body is None:
            return

        # 2) Emulated axial thrust from each screw (robot frame, +x forward)
        thrust_left = THRUST_PER_RAD * THRUST_SIGN_LEFT * left
        thrust_right = THRUST_PER_RAD * THRUST_SIGN_RIGHT * right

        # 3) Drag in the robot frame (thread grips sideways, resists yaw)
        vel = self.__body.getVelocity()          # [vx, vy, vz, wx, wy, wz] in world frame
        R = self.__body.getOrientation()         # 3x3 row-major, local -> world
        v_local = [sum(R[j * 3 + i] * vel[j] for j in range(3)) for i in range(3)]
        w_local_z = sum(R[j * 3 + 2] * vel[3 + j] for j in range(3))

        fx = thrust_left + thrust_right - DRAG_X * v_local[0]
        fy = -DRAG_Y * v_local[1]
        # Left screw sits at y = -SCREW_Y, right at y = +SCREW_Y (see world file).
        tz = SCREW_Y * (thrust_left - thrust_right) - DRAG_YAW * w_local_z

        # Forces are cleared every step, so reapply each step.
        self.__body.addForce([fx, fy, 0.0], True)
        self.__body.addTorque([0.0, 0.0, tz], True)


def main():
    print('Hi from amphi_plain_sim.')


if __name__ == '__main__':
    main()
