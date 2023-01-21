from pywebio.input import *
from pywebio.output import *
import os
import pandas as pd

def FileInput():
    method = radio("Choose one", options=['Local files', 'Files from website'])
    
    if method == 'Local files':
        controls = file_upload("Please upload files for the control group:", accept=".csv",  multiple = True,  placeholder='Choose files (in csv)')
        contrasts = file_upload("Please upload files for the contrast group:", accept=".csv",  multiple = True,  placeholder='Choose files (in csv)')
        metadata = file_upload("Please upload the metadata file:", accept=".csv",  multiple = False,  placeholder='Choose files (in csv)')
        
        list_control = []  # a list to hold all the individual pandas DataFrames
        for csvfile in controls:
            open(csvfile["filename"], "wb").write(csvfile["content"])
            df = pd.read_csv(csvfile["filename"])
            list_control.append(df)
            
        list_contrast = []  # a list to hold all the individual pandas DataFrames
        for csvfile in contrasts:
            open(csvfile["filename"], "wb").write(csvfile["content"])
            df = pd.read_csv(csvfile["filename"])
            list_contrast.append(df)
            
        result = pd.concat(list_control, ignore_index=True)
        
        
        result2 = pd.concat([result.head(10),result.tail(10)])
        
        put_text(result2)
        
    if method == 'Files from website':
        img = file_upload("Select a image:", accept="image/*")
if __name__ == '__main__':
    FileInput()
