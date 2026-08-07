"""my_amphi controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Keyboard

# create the Robot instance.
robot = Robot()
MAX_SPEED = 6.48
keyboard = Keyboard()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

left_motor =  robot.getDevice('motor_1')
right_motor =  robot.getDevice('motor_2')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    
    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    key = keyboard.getKey()
    left_speed = 0.0
    right_speed = 0.0
    
    if key == Keyboard.UP:
        left_speed = MAX_SPEED
        right_speed = -MAX_SPEED
    elif key == Keyboard.DOWN:
        left_speed = -MAX_SPEED
        right_speed = MAX_SPEED
    elif key == Keyboard.LEFT:
        left_speed = -MAX_SPEED
        right_speed = -MAX_SPEED
    elif key == Keyboard.RIGHT:
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
    
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)


# Enter here exit cleanup code.
