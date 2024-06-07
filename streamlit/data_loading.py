# data_loading.py
import pandas as pd
#import geopandas as gpd


def load_df(file_path):
    data = pd.read_csv(file_path)
    return data


#def load_gdf(file_path):
#    data = gpd.read_file(file_path)
#    return data

