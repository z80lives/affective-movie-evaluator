from tabulate import tabulate
import pandas as pd

def table_print(arr_data):
    data = arr_data
    #data = list(arr_data.values())
    #keys = list(data[0].keys())
    #print(data)
    #print(tabulate(data, headers=keys))
    
    
    df = pd.DataFrame(data)
    print(df)    

