from utils.sound import Sound
from utils.brick import reset_brick
import time
from colour_detection import collect_color_sensor_data, most_frequent_color
from robot_movement import move_left, move_right, move_straight, LEFT_MOTOR,RIGHT_MOTOR, FORWARD_SPEED_RIGHT,FORWARD_SPEED_LEFT
from robot_program import T_SENSOR, SENSOR_POLL_SLEEP, COLOR_SENSOR1
SOUND = Sound(duration=0.5, volume=100, pitch="A4")

def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()

def return_to_start():

    restart = False
    restart_timer = 0.0
    turn_history = []
    window_size = 20
    avgColor = []
    yellow_flag = False
        
    try:

        while True:

            if T_SENSOR.is_pressed():
                reset_brick()
                print("Shutting down...")
                exit()

            # collect and parse current color seen by color sensor
            color_sensor1_output = COLOR_SENSOR1.get_value()
            color_indicator1 = collect_color_sensor_data(color_sensor1_output, 1)
            
            # Movement on the track of the robot 
            if color_indicator1 == "Blue":
                turn_history.append(1)
                if len(turn_history)>window_size:
                    turn_history.pop(0)
                move_left()
                
            if color_indicator1 == "Red":
                turn_history.append(-1)
                if len(turn_history)>window_size:
                    turn_history.pop(0)
                move_right()

            if color_indicator1 == "White" :
                turn_history.append(0)
                if len(turn_history)>window_size:
                    turn_history.pop(0)
                move_straight()
                
            # adjust direction based off path before green
            if color_indicator1 == "Green":
                
                if len(turn_history)>0: 
                    turn_tendency = sum(turn_history)/len(turn_history)
                else:
                    turn_tendency = 0
                
                if turn_tendency < 0:
                    RIGHT_MOTOR.set_power(FORWARD_SPEED_RIGHT/1.5)
                elif turn_tendency > 0:
                    LEFT_MOTOR.set_power(FORWARD_SPEED_LEFT/1.5)
                else:
                    move_straight()

            if color_indicator1 == "Yellow" and restart == False:
                print("---------AT START---------")
                restart_timer = time.perf_counter()
                restart = True
                yellow_flag = True
            
            if yellow_flag == True:
                avgColor.append(color_sensor1_output)

            if restart == True and (time.perf_counter() - restart_timer) > 1.10:

                avgColor.pop()
                avgColor.pop()
                avgColor.pop()

                colors_collected = []
                
                for i in range(len(avgColor)):
                    colors_collected.append(collect_color_sensor_data([avgColor[i][0],avgColor[i][1],avgColor[i][2]],1))

                color_adjusted = most_frequent_color(colors_collected)

                if color_adjusted == "Yellow":

                    LEFT_MOTOR.set_power(0)
                    RIGHT_MOTOR.set_power(0)
                    print("!!!-------STARTING TURN--------!!!")
                    print(color_adjusted)
                    uTurn("start")
                    play_sound()
                    return
                
                else:

                    yellow_flag = False
                    restart = False
                    restart_timer = 0.0
                    avgColor.clear()
            
            # Use sensor polling interval here
            time.sleep(SENSOR_POLL_SLEEP)
            
    except BaseException as error:
        print(error)


def uTurn(position):

    try: 

        RIGHT_MOTOR.set_power(FORWARD_SPEED_RIGHT)
        LEFT_MOTOR.set_power(-FORWARD_SPEED_LEFT)
        flag = False

        if position == "end":
            turn_color = "Blue"
        else:
            turn_color = "Red"
        
        time.sleep(2.0)
        
        while (True):

            # collect and parse current color seen by color sensor
            color_sensor1_output = COLOR_SENSOR1.get_value()
            color_indicator1 = collect_color_sensor_data(color_sensor1_output, 1)

            if (color_indicator1 == turn_color):
                flag = True

            if (color_indicator1 == "Green"):
                time.sleep(0.5)
                RIGHT_MOTOR.set_power(0)
                LEFT_MOTOR.set_power(0)
                return

            if (flag == True and (color_indicator1 == "White" or color_indicator1 == "Green")):
                time.sleep(0.25)
                RIGHT_MOTOR.set_power(0)
                LEFT_MOTOR.set_power(0)
                return

            # Use sensor polling interval here
            time.sleep(SENSOR_POLL_SLEEP)
    
    except BaseException as error:
        print(error)