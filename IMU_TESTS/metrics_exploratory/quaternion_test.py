import pandas as pd
from ahrs import Quaternion
import ahrs
import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.express as px
import math

# Read csv
df = pd.read_csv('./new_dataset/static.csv', delimiter=',')


acc_data = df[['Accelerometer X (m/s²)','Accelerometer Y (m/s²)','Accelerometer Z (m/s²)']].to_numpy()
gyr_data = df[['Gyroscope X (rad/s)','Gyroscope Y (rad/s)','Gyroscope Z (rad/s)']].to_numpy()
mag_data = df[['Magnetometer X (mT)','Magnetometer Y (mT)','Magnetometer Z (mT)']].to_numpy()
time_data = df[['time']].to_numpy()

attitude = ahrs.filters.Madgwick(acc=acc_data, gyr=gyr_data, gain=0.2, frequency=66.0)

quaternions_list = attitude.Q
quaternions_list = quaternions_list.tolist()

quaternions = list()

df_direction_vector = pd.DataFrame(columns=['x', 'y', 'z'])
for quaternion_data in quaternions_list :
    q = Quaternion([
        quaternion_data[3], # W
        quaternion_data[0], # X
        quaternion_data[1], # Y
        quaternion_data[2] # Z
    ])



    
