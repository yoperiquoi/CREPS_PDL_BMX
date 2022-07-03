import pandas as pd
from ahrs import Quaternion
import ahrs
import matplotlib.pyplot as plt
import numpy as np
import sys
import plotly.express as px
import math

# Read csv
df = pd.read_csv('./new_dataset/linear_x.csv', delimiter=',')

    
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

    # https://stackoverflow.com/questions/5782658/extracting-yaw-from-a-quaternion
    roll = math.atan2(2 * (q.z * q.y + q.w * q.x), 1 - 2 * (q.x * q.x + q.y * q.y))
    pitch = math.asin(2 * (q.y * q.w - q.z * q.x))
    yaw = math.atan2(2 * (q.z * q.w + q.x * q.y), (q.w * q.w + q.x * q.x - q.y * q.y - q.z * q.z))


    # https://stackoverflow.com/questions/5782658/extracting-yaw-from-a-quaternion
    # yaw = math.atan2(2.0*(q.y*q.z + q.w*q.x), q.w*q.w - q.x*q.x - q.y*q.y + q.z*q.z)
    # pitch = math.asin(-2.0*(q.x*q.z - q.w*q.y))
    # roll = math.atan2(2.0*(q.x*q.y + q.w*q.z), q.w*q.w + q.x*q.x - q.y*q.y - q.z*q.z)

    # https://stackoverflow.com/questions/1568568/how-to-convert-euler-angles-to-directional-vector
    x = math.cos(yaw) * math.cos(pitch)
    y = math.sin(yaw)* math.cos(pitch)
    z = math.sin(pitch)

    # euler_angle = q.to_angles()
    # x = euler_angle[0]
    # y = euler_angle[1]
    # z = euler_angle[2]

    df_direction_vector = df_direction_vector.append({
        'x' : x,
        'y' : y,
        'z' : z
    }, ignore_index=True)



# Speed
speed_df = pd.DataFrame(columns=['v_x', 'v_y', 'v_z'])
distance_df = pd.DataFrame(columns=['d_x', 'd_y', 'd_z'])
position_df = pd.DataFrame(columns=['p_x', 'p_y', 'p_z', 'i'])


v_x = 0
v_y = 0
v_z = 0

i = 0


p_x = 0
p_y = 0
p_z = 0


last_p_x = 0
last_p_y = 0
last_p_z = 0
for row in acc_data :
    acc_x = row[0]
    acc_y = row[1]
    acc_z = row[2]


    v_x = v_x + acc_x * (time_data[i][0]/1000)
    v_y = v_y + acc_y * (time_data[i][0]/1000)
    v_z = v_z + acc_z * (time_data[i][0]/1000)

    speed_df = speed_df.append({
        'v_x' : v_x,
        'v_y' : v_y,
        'v_z' : v_z
    }, ignore_index=True)


    norm_speed = math.sqrt(v_x**2 + v_y**2 + v_z**2)


    d_x = v_x * (time_data[i][0]/1000)
    d_y = v_y * (time_data[i][0]/1000)
    d_z = v_z * (time_data[i][0]/1000)

    distance_df = distance_df.append({
        'd_x' : d_x,
        'd_y' : d_y,
        'd_z' : d_z 
    }, ignore_index=True)


    # y = ax + b
    # y/a - b 





    p_x = norm_speed * df_direction_vector.loc[i, 'x'] + last_p_x
    p_y = norm_speed * df_direction_vector.loc[i, 'y'] + last_p_y
    p_z = norm_speed * df_direction_vector.loc[i, 'z'] + last_p_z


    position_df = position_df.append({
        'p_x' : p_x,
        'p_y' : p_y,
        'p_z' : p_z,
        'i' : i
    }, ignore_index=True)

    last_p_x = p_x
    last_p_y = p_y
    last_p_z = p_z

    i += 1



position_df.to_csv('./output/position.csv', index=None)
speed_df.to_csv('./output/speed.csv', index=None)
print(len(position_df))




fig = px.scatter_3d(position_df, x='p_x', y='p_y', z='p_z', color='i')
fig.show()