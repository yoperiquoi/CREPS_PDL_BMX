# External Imports
import pandas as pd
import matplotlib.pyplot as plt

# Consts
CSV_PATH = './output/filter_preprocess_dataset_1.csv'
COLS_TO_PLOT = [
    'x',
    'y',
    'z'
]
COL_INDEX_NAME = 'index'


# Read csv
df : pd.DataFrame = pd.read_csv(CSV_PATH)



for col in COLS_TO_PLOT :
    plt.plot(df[COL_INDEX_NAME], df[col])
plt.show()
