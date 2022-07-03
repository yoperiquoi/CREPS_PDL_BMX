import pandas as pd
import plotly.express as px


df : pd.DataFrame = pd.read_csv('./new_dataset/linear_x_3.csv', delimiter=',')
print(df.head())



s = {
    'X' : 0,
    'Y' : 0,
    'Z' : 0 
}

p = {
    'X' : 0,
    'Y' : 0,
    'Z' : 0
}


history_speed = list()
history_position = list()

for i in range(1, len(df)) :
    s = {
        'X' : s['X'] + df.loc[i, 'Accelerometer X (m/s²)'] * df.loc[i, 'time']/1000,
        'Y' : s['Y'] + df.loc[i, 'Accelerometer Y (m/s²)'] * df.loc[i, 'time']/1000,
        'Z' : s['Z'] + df.loc[i, 'Accelerometer Z (m/s²)'] * df.loc[i, 'time']/1000
    }

    p = {
        'X' : p['X'] + s['X'] * df.loc[i, 'time']/1000,
        'Y' : p['Y'] + s['Y'] * df.loc[i, 'time']/1000,
        'Z' : p['Z'] + s['Z'] * df.loc[i, 'time']/1000
    }


    history_speed.append(
        s
    )

    history_position.append(
        p
    )




history_speed_df = pd.DataFrame(history_speed)
history_position_df = pd.DataFrame(history_position)

history_position_df.reset_index()
print(history_position_df.head())


fig = px.scatter_3d(history_position_df, x='X', y='Y', z='Z')
fig.show()