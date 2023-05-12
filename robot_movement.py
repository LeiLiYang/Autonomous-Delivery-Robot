from utils.brick import Motor
import time

FORWARD_SPEED_LEFT = 20              
FORWARD_SPEED_RIGHT = 22              
PUSHER_SLEEP = 2                      
MOTOR_SLEEP = 2                       

LEFT_MOTOR = Motor("D")               # Left motor in Port MA
RIGHT_MOTOR = Motor("A")              # Right motor in Port MD
PUSH_MOTOR  = Motor("C")              # Pushes the package into the dropping zone
MOVING_MOTOR = Motor("B")             # Moves the sliding mechanisim

def move_right():
    # turn right
    RIGHT_MOTOR.set_power(0)
    LEFT_MOTOR.set_power(FORWARD_SPEED_LEFT)
    

def move_left():
    # turn left
    LEFT_MOTOR.set_power(0)
    RIGHT_MOTOR.set_power(FORWARD_SPEED_RIGHT)

def move_straight():
    # turn left
    LEFT_MOTOR.set_power(FORWARD_SPEED_LEFT)
    RIGHT_MOTOR.set_power(FORWARD_SPEED_RIGHT)


# Process to deposit the colored cube
def deposit_cube(motor_rotation):
    try:
        # rotate the motor to reach the right cube
        print("Im in the deposit cube")
        MOVING_MOTOR.set_position(motor_rotation)
        time.sleep(MOTOR_SLEEP)

        PUSH_MOTOR.set_position_relative(365)
        time.sleep(PUSHER_SLEEP)

        # reset to initial position
        MOVING_MOTOR.set_position_relative(-motor_rotation)
        time.sleep(MOTOR_SLEEP)

    except BaseException as error:
        print(error)