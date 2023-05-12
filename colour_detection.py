import math

def color_matching(unknown_color, sensor):

    # find referance data for each color (different for each sensor)
    if sensor == 1:
        red = [0.840248963,0.112033195,0.047717842]
        orange = [0.754464286, 0.205357143, 0.040178571]
        yellow = [0.526162791, 0.436046512, 0.037790698]
        green = [0.250000000, 0.658333333, 0.091666667]
        blue = [0.322916667,0.34375,0.333333333]
        purple = [0.739549839, 0.1414791, 0.118971061]
        white = [0.461388074,0.350928641,0.187683284]
    else:
        red = [0.754464286, 0.205357143, 0.040178571]
        orange = [0.696857671,0.229205176,0.073937153]
        yellow = [0.483204134,0.447028424,0.069767442]
        green = [0.193979933,0.632107023,0.173913043]
        blue = [0.185606061,0.356060606,0.458333333]
        purple = [0.64921466,0.136125654,0.214659686]
        white = [0.341421144,0.35355286,0.305025997]
  
    # distance to sample color by cluster method, location of cluster defined by center mass
    d_red = math.sqrt((unknown_color[0]-red[0])**2 + (unknown_color[1]-red[1])**2 +(unknown_color[2]-red[2])**2)
    d_orange = math.sqrt((unknown_color[0]-orange[0])**2 + (unknown_color[1]-orange[1])**2 +(unknown_color[2]-orange[2])**2)
    d_yellow = math.sqrt((unknown_color[0]-yellow[0])**2 + (unknown_color[1]-yellow[1])**2 +(unknown_color[2]-yellow[2])**2)
    d_green = math.sqrt((unknown_color[0]-green[0])**2 + (unknown_color[1]-green[1])**2 +(unknown_color[2]-green[2])**2)
    d_blue = math.sqrt((unknown_color[0]-blue[0])**2 + (unknown_color[1]-blue[1])**2 +(unknown_color[2]-blue[2])**2)
    d_purple = math.sqrt((unknown_color[0]-purple[0])**2 + (unknown_color[1]-purple[1])**2 +(unknown_color[2]-purple[2])**2)
    d_white = math.sqrt((unknown_color[0]-white[0])**2 + (unknown_color[1]-white[1])**2 +(unknown_color[2]-white[2])**2)

    # color matching sequence, shortest distance indicates closest match
    d = d_red
    color = "Red"
    
    if d > d_orange:
        d = d_orange
        color = "Orange"
        
    if d > d_yellow:
        d = d_yellow
        color = "Yellow"

    if d > d_green:
        d = d_green
        color = "Green"

    if d > d_blue:
        d = d_blue
        color = "Blue"

    if d > d_purple:
        d = d_purple
        color = "Purple"

    if d > d_white:
        d = d_white
        color = "White"
    
    return color

def collect_color_sensor_data(color_data, sensor):

    #  first 3 elements of array are RGB values
    r = color_data[0]
    g = color_data[1]
    b = color_data[2]
    color = ""

    # normalize RGB mesurements
    if color_data is not None:
        if r != 0 or g != 0 or b != 0:
            R_norm = r/(r+g+b)
            G_norm = g/(r+g+b)
            B_norm = b/(r+g+b)
            RGB = [R_norm, G_norm, B_norm]
            color = color_matching(RGB, sensor)

    return color

#predicts the turning direction when on a green line
def most_frequent_color(colors):
    color_count = {}
    max_count = 0
    most_frequent = None

    for color in colors:
        if color in color_count:
            color_count[color] += 1
        else:
            color_count[color] = 1

        if color_count[color] > max_count:
            max_count = color_count[color]
            most_frequent = color

    return most_frequent
