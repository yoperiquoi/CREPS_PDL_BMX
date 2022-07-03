import pandas as pd
from scipy.signal import savgol_filter
import math

# Load raw dataset (Arduino output)
df : pd.DataFrame = pd.read_csv('./dataset/test_1.csv', delimiter=',')

# Apply Savitzky-Golay filter
#   on 3D Accel data (x, y & z axis) 
df['acc_x_filtered'] = savgol_filter(df['acc_x'], 27, 3)
df['acc_y_filtered'] = savgol_filter(df['acc_y'], 27, 3)
df['acc_z_filtered'] = savgol_filter(df['acc_z'], 27, 3)
#   on pitch, roll & yaw data
#       (https://fr.wikipedia.org/wiki/Axes_de_rotation_d%27un_a%C3%A9ronef)
df['pitch_filtered'] = savgol_filter(df['pitch'], 27, 3)
df['roll_filtered'] = savgol_filter(df['roll'], 27, 3)
df['yaw_filtered'] = savgol_filter(df['yaw'], 27, 3)




# Compute 3D Direction vector (x, y & z axis)
df['x'] = 0
df['y'] = 0
df['z'] = 0

df['speed'] = 0
for index, row in df.iterrows() :
    # Formula find on : (https://stackoverflow.com/questions/1568568/how-to-convert-euler-angles-to-directional-vector)
    df.loc[index, 'x'] = math.cos(row['yaw_filtered']) * math.cos(row['pitch_filtered'])
    df.loc[index, 'y'] = math.sin(row['yaw_filtered']) * math.cos(row['pitch_filtered'])
    df.loc[index, 'z'] = math.sin(row['pitch_filtered'])


df.to_csv('./output/filter_preprocess_dataset_1.csv', index=None, sep=',')