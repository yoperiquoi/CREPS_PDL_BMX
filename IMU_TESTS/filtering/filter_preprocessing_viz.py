# External Imports
import pandas as pd
import matplotlib.pyplot as plt


# Consts
DATASET_PATH = './output/filter_preprocess_dataset_1.csv'
COL_INDEX_NAME = 'index'
COL_VIZ = 'roll'
SUFFIX_COL_VIZ = '_filtered'


# Load dataset
df : pd.DataFrame = pd.read_csv(DATASET_PATH)


plt.plot(df[COL_INDEX_NAME], df[COL_VIZ])
plt.plot(df[COL_INDEX_NAME], df[f'{COL_VIZ}{SUFFIX_COL_VIZ}'], color='green')
plt.show()






