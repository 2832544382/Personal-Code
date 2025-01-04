import time
import sys


sys.path.append("./color")
from color.color_command import color_command as cc

sys.path.append("./DMP")
from DMP import dmp_dobot as dmp

sys.path.append("./LLM")
from LLM import dobot_ollama as llm
#8.5 17 34
y_diff = 0.02
z_diff = 0.18

from serial.tools import list_ports
from pydobot import Dobot
#init dobot
port = list_ports.comports()[1].device
time.sleep(7)
device = Dobot(port=port, verbose=False)
device.speed(200,500)
device.move_to(190,-150,20,0)
device.pose()

#init color ranges
#interval of each key
color_ranges = {
    "1": ([170, 155, 200, 0, 155, 200], [174, 190, 240, 5, 190, 240]),
    "2": ([9, 145, 180], [16, 220, 255]),
    "3": ([20, 120, 150], [28, 240, 255]),
    "4": ([55, 120, 120], [70, 180, 200]),
    "5": ([100, 200, 190], [105, 255, 255]),
    "6": ([108, 120, 80], [119, 220, 160]),
    "7": ([120, 90, 100], [130, 140, 140]),
    "8": ([160, 40, 220], [170, 120, 255])
}

music_score = llm.bot_chat()

#init camera & dectect keys
color_detector = cc()
time.sleep(5)
all_colors_list = []
for color in color_ranges.keys():

    lower = color_ranges[color][0]
    upper = color_ranges[color][1]
    img_center = color_detector.get_color_center(lower=lower, upper=upper)
    img_center[2] = img_center[2]-z_diff

    arm_pos = color_detector.convert_cam_to_arm(img_center)
    #print(arm_pos)
    arm_pos[1] = color_detector.diff(arm_pos[1])
    arm_pos[2] = -53.5
    all_colors_list.append(arm_pos)

color_in_arm = color_detector.form_dict(all_colors_list)
print(color_in_arm)

time.sleep(1)

device.move_to(250,0,50,0,wait=True)

all_dmp = []

#generate trajectories

flatten_list, length_list = dmp.flatten_arr(music_score)
speeds = dmp.calc_speed(length_list=length_list)
print(speeds)

for notes in range(len(flatten_list)-1):
    moving_trajectories = dmp.dobot_move_to(init_position=color_in_arm[flatten_list[notes]][:3].tolist(),
                                                goal_position=color_in_arm[flatten_list[notes+1]][:3].tolist())
    all_dmp.append(moving_trajectories)

#move arm

i = 0
for trajectories in all_dmp:
    device.speed(speeds[i][0],speeds[i][1])
    i += 1
    for trajectory in trajectories:
        device.move_to(181, color_detector.diff(trajectory[1])+5, trajectory[2], 0, wait=True)

device.speed(200,1000)
device.move_to(250,0,50,0,wait=True)

