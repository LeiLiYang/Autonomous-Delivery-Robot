from robot_program import robot
from utils.brick import wait_ready_sensors

wait_ready_sensors(True)              # Wait for sensors to initialize 


if __name__ == "__main__":
    robot()