import pandas as pd


def init_record_df() :
    return pd.DataFrame(columns=['K_CAPTEUR', 'F_LAT', 'F_LONG', 'F_GYRX', 'F_GYRY', 'F_GYRZ', 'F_ACCX', 'F_ACCY', 'F_ACCZ', 'F_MAGX', 'F_MAGY', 'F_MAGZ', 'F_TIME']) 