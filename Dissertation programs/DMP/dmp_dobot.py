import math
import numpy as np
from dmp_discrete import dmp_discrete
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def extend(arr):
    new_arr = np.array([])
    arr = np.array(arr)
    for i in range(arr.shape[0]):
        if i != arr.shape[0]-1:
            a = np.linspace(arr[i],arr[i+1],10)
            new_arr = np.append(new_arr, a)
    
    new_arr = np.reshape(new_arr, (int(new_arr.shape[0]/3),3))
    #print(new_arr.shape)
    return new_arr.T

def flatten_arr(lists):
    modify = lists[0]

    flattened_list = []
    length_list = []

    for sublist in modify:
        flattened_list.extend(sublist)
        length_list.append(len(sublist))

    str_list = []
    for i in flattened_list:
        str_list.append(str(i))

    return str_list, length_list

def calc_speed(length_list):
        #Seconds
        VELO1 = 200
        ACC1 = 500
        VELO2 = 200
        ACC2 = 200
        VELO3 = 200
        ACC3 = 150

        max_number = max(length_list)
        time_list = []
        if max_number == 1:
            for _ in range(len(length_list)-1):
                time_list.append((VELO1, ACC1))

        elif max_number == 2:
            for i, value in enumerate(length_list):

                if i == 0:  # 判断第一个值

                    if value == 1:
                        continue
                    elif value == 2:
                        time_list.append((VELO2, ACC2))
                else:
                    if value == 1:
                        time_list.append((VELO1, ACC1))  # 如果值为1，添加一个 (VELO1, ACC1)
                    elif value == 2:
                        time_list.extend([(VELO2, ACC2)] * 2)
        elif max_number == 4:
            for i, value in enumerate(length_list):
                if i == 0:
                    if value == 1:
                        continue
                    elif value == 2:
                        time_list.append((VELO2, ACC2))
                    elif value == 4:
                        time_list.extend([(VELO3, ACC3)] * 3)
                else:
                    if value == 1:
                        time_list.append((VELO1, ACC1))
                    elif value == 2:
                        time_list.extend([(VELO2, ACC2)] * 2)
                    elif value == 4:
                        time_list.extend([(VELO3, ACC3)] * 4)
        return time_list

#dmp learning
def dobot_move_to(init_position, goal_position):
    df = pd.read_csv('./smoothed_data.csv', header=None)
    train = np.array(df)

    extend_train = extend(train)

    dmp_process = extend_train
    data_dim = dmp_process.shape[0]
    data_len = dmp_process.shape[1]
    #print(train)

    dmp = dmp_discrete(n_dmps=data_dim, n_bfs=1000, dt=1.0/data_len)
    dmp.learning(dmp_process)

    reproduced, _, _ = dmp.reproduce(initial=init_position, goal=goal_position)

    #x = np.array([extend_train[0]])
    #y = np.array([extend_train[1]])
    #z = np.array([extend_train[2]])

    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #ax.scatter(x, y, z)
    #plt.show()

    shrink_reproduced = reproduced[::17]
    shrink_reproduced = shrink_reproduced[:-1]  # 删除最后一位
    shrink_reproduced = np.append(shrink_reproduced, [reproduced[-1]], axis=0)

    #print(reproduced[-1])
    
    #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #ax.scatter(shrink_reproduced[:,0], shrink_reproduced[:,1], shrink_reproduced[:,2])
    #plt.show()
    #print(shrink_reproduced)
    return shrink_reproduced
    #return reproduced

def calc_distance(paths):
    all_path = []
    velocity = []
    acceleration = []
    p = [paths]
    distance = 0
    for path in p:

        for i in range(len(path)-1):
            distance += math.sqrt((path[i+1][0]-path[i][0])**2+
                                (path[i+1][1]-path[i][1])**2+
                                (path[i+1][2]-path[i][2])**2)

    return distance






