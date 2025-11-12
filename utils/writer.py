import pandas as pd

def write_list_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)