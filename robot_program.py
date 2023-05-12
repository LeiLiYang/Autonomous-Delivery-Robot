from utils.brick import TouchSensor, EV3ColorSensor, reset_brick
import time
from robot_movement import MOVING_MOTOR, PUSH_MOTOR, LEFT_MOTOR, RIGHT_MOTOR,  FORWARD_SPEED_LEFT, FORWARD_SPEED_RIGHT, PUSHER_SLEEP, deposit_cube, move_left, move_right,move_straight
from return_to_loading_dock import uTurn, return_to_start
from colour_detection import collect_color_sensor_data

T_SENSOR = TouchSensor(4)             # Touch Sensor in Port S1
COLOR_SENSOR1 = EV3ColorSensor(3)     # Color Sensor in Port S3
COLOR_SENSOR2 = EV3ColorSensor(1)     # Color Sensor in POrt S2
SENSOR_POLL_SLEEP = 0.1               # Polling rate = 100 msec

def robot():
    try:
        
        while True:

            time.sleep(SENSOR_POLL_SLEEP)
                
            # start
            if T_SENSOR.is_pressed():

                time.sleep(0.5)

                # set variables
                drop_indicator_top = False
                drop_indicator_bottom = False
                drop_zone_color = ""
                dropped_colors = []
                restart = False
                restart_timer = 0.0
                avgColor = []
                turn_history = []      
                window_size = 20        
                
                # will move the belt until its at its leftmost max to set origin
                MOVING_MOTOR.set_power(30)
                time.sleep(2)
                MOVING_MOTOR.set_power(0)
                time.sleep(0.5)

                # set zeroed position for the moving motor and max power
                MOVING_MOTOR.reset_encoder()
                MOVING_MOTOR.set_limits(power=30)
                time.sleep(0.5)


                PUSH_MOTOR.set_limits(power=30)
                time.sleep(0.5)

                move_straight()
                
                while True: 

                    # end of track, 6 cubes have been dropped
                    if len(dropped_colors) == 6 and restart == False:
                        restart_timer = time.perf_counter()
                        restart = True

                    # stop, turn around, go back to start, turn around, stop and 
                    # wait for cubes to be reloaded then press button again
                    if restart == True and (time.perf_counter() - restart_timer) > 3.0:
                        
                        # stop
                        LEFT_MOTOR.set_power(0)
                        RIGHT_MOTOR.set_power(0)  

                        # turn
                        uTurn("end")

                        # restart
                        move_straight()
                        return_to_start()
                        print("Restart")
                        break

                    # emergency stop
                    if T_SENSOR.is_pressed():
                        reset_brick()
                        print("Shutting down...")
                        exit()

                    # collect and parse current color seen by color sensor
                    color_sensor1_output = COLOR_SENSOR1.get_value()
                    color_indicator1 = collect_color_sensor_data(color_sensor1_output, 1)
                    
                    # Movement on the track of the robot 
                    if color_indicator1 == "Red":
                        turn_history.append(1)
                        if len(turn_history) > window_size:
                            turn_history.pop(0)
                        move_left()
                        
                    if color_indicator1 == "Blue":
                        turn_history.append(-1)
                        if len(turn_history) > window_size:
                            turn_history.pop(0)
                        move_right()

                    if color_indicator1 == "White" :
                        turn_history.append(0)
                        if len(turn_history) > window_size:
                            turn_history.pop(0)
                        move_straight()
                        
                    # adjust direction based off path before green
                    if color_indicator1 == "Green":
                        
                        print("green ind")
                        drop_indicator_top = True
                        
                        turn_tendency = sum(turn_history)/len(turn_history)
                        
                        if turn_tendency < 0:
                            RIGHT_MOTOR.set_power(FORWARD_SPEED_RIGHT/1.5)
                        elif turn_tendency > 0:
                            LEFT_MOTOR.set_power(FORWARD_SPEED_LEFT/1.5)
                        else:
                            move_straight()

                    # start sensing for delivery zone
                    if drop_indicator_top == True:

                        # collect and parse current color seen by color sensor 2
                        color_sensor2_output = COLOR_SENSOR2.get_value()
                        color_indicator2 = collect_color_sensor_data(color_sensor2_output, 2)
                        #avgColor.append(color_indicator2)
                        if color_indicator2 != "White":
                            drop_zone_color = color_indicator2
                            drop_indicator_top = False
                            drop_indicator_bottom = True

                    # when the second color sensor is out of the drop zone, the robot is ready to be dropped
                    if drop_indicator_bottom == True:

                        # collect and parse current color seen by color sensor 2
                        color_sensor2_output = COLOR_SENSOR2.get_value()
                        print(color_sensor2_output)
                        color_indicator2 = collect_color_sensor_data(color_sensor2_output, 2)
                        avgColor.append(color_sensor2_output)
                        
                        # make sure second detector is dropping the right color
                        if color_indicator2 == "White" and len(dropped_colors) < 6 and len(avgColor)>4:
                            #if len(avgColor)>4:
                            avgColor.pop()
                            avgColor.pop()
                            avgColor.pop()
                        
                            avgR = 0
                            avgG = 0
                            avgB = 0
                            for i in range(len(avgColor)):
                                avgR += int(avgColor[i][0])
                                avgG += int(avgColor[i][1])
                                avgB += int(avgColor[i][2])
                            avgR = avgR/len(avgColor)
                            avgG = avgG/len(avgColor)
                            avgB = avgB/len(avgColor)
                            print("here")
                            drop_zone_color = collect_color_sensor_data([avgR,avgG,avgB],2)
                            # ready for drop
                            drop_indicator_bottom = False
                            print(color_indicator2)
                            
                            LEFT_MOTOR.set_power(0)
                            RIGHT_MOTOR.set_power(0)
                            print("Drop Zone Color: " + drop_zone_color)

                            # PURPLE will always be placed at position #1
                            if drop_zone_color == "Purple":

                                print("made it in purple")
                                dropped_colors.append(drop_zone_color)

                                # we wouldn't need to move, just push the color cube 
                                PUSH_MOTOR.set_position_relative(365)
                                time.sleep(PUSHER_SLEEP)

                            # BLUE will always be placed at position #2
                            if drop_zone_color == "Blue":

                                print("made it in blue")
                                dropped_colors.append(drop_zone_color)
                                deposit_cube(-110)

                            # GREEN will always be placed at position #3
                            if drop_zone_color == "Green":
                                print("made it in green")
                                dropped_colors.append(drop_zone_color)
                                deposit_cube(-205)

                            # YELLOW will always be placed at position #4
                            if drop_zone_color == "Yellow":
                                print("made it in yellow")
                                dropped_colors.append(drop_zone_color) 
                                deposit_cube(-290)

                            # ORANGE will always be placed at position #5
                            if drop_zone_color == "Orange":
                                print("made it in orange")
                                dropped_colors.append(drop_zone_color) 
                                deposit_cube(-390)

                            # RED will always be placed at position #6
                            if drop_zone_color == "Red":
                                print("made it in red")
                                dropped_colors.append(drop_zone_color) 
                                deposit_cube(-505)
                                
                            move_straight()
                            avgColor = []
                    # Use sensor polling interval here
                    time.sleep(SENSOR_POLL_SLEEP)


    # On exception or error, print error code
    except BaseException as error:
        print(error)
        reset_brick()
        exit()