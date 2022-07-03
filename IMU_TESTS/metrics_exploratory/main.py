import pandas as pd
import pyquaternion
import ahrs
from pytransform3d.batch_rotations import quaternion_slerp_batch
from pytransform3d.rotations import q_id
from pytransform3d.trajectories import plot_trajectory
import matplotlib.pyplot as plt
import numpy as np
import sys

# Read csv
df = pd.read_csv('./dataset/test10.csv', delimiter=',')


acc_data = df[['Accelerometer X (m/s²)','Accelerometer Y (m/s²)','Accelerometer Z (m/s²)']].to_numpy()
gyr_data = df[['Gyroscope X (rad/s)','Gyroscope Y (rad/s)','Gyroscope Z (rad/s)']].to_numpy()
mag_data = df[['Magnetometer X (mT)','Magnetometer Y (mT)','Magnetometer Z (mT)']].to_numpy()

attitude = ahrs.filters.Madgwick(acc=acc_data, gyr=gyr_data, gain=0.2, frequency=25.0)



quaternions_list = attitude.Q
quaternions_list = quaternions_list.tolist()


start = np.array(quaternions_list[0])
end = np.array(quaternions_list[len(quaternions_list)-1])

slepr_quaternions = quaternion_slerp_batch(start, end, np.linspace(0, 1, len(quaternions_list)))



procesed_quaternions = list()
for i in range(len(quaternions_list)) : 
    print(i)
    row = quaternions_list[i]

    row.append(slepr_quaternions[i,1])
    row.append(slepr_quaternions[i,2])
    row.append(slepr_quaternions[i,3])

    procesed_quaternions.append(row)

procesed_quaternions = np.array(procesed_quaternions)


ax = plot_trajectory(P=procesed_quaternions, s=0.2, n_frames=100, normalize_quaternions=False, lw=2, c="k", show_direction=False)
plt.show()