from pydobot import Dobot
import os
import time
from serial.tools import list_ports
import numpy as np

class dobot_trajectory:
    def __init__(self):
        port = list_ports.comports()[0].device
        time.sleep(7)
        self.device = Dobot(port=port, verbose=False)

    def record_trajectory(self):
        records = []
        time.sleep(1)
        start_time = time.time()
        while round(time.time()-start_time) < 35:
            print(time.time()-start_time)
            new_point = self.device.pose()
            print(new_point)
            records.append(new_point[:3])
            time.sleep(0.1)

        return np.array(records)

if __name__ == "__main__":
    tra = dobot_trajectory()
    train_trajectory = np.array(tra.record_trajectory())
    print(train_trajectory)
    train_path = "./DMP/trianing_trajectory.npy"
    empty_data = np.array([])
    np.load(train_path)
    np.save(train_path, empty_data)
    
    np.load(train_path)
    np.save(train_path, train_trajectory)



            
