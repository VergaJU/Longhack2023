from pywebio.input import *
from pywebio.output import *
import os
import pandas as pd

def FileInput():
    put_image(open('./network_viz/assets/logo_horizontal.png', 'rb').read()) 
    method = radio("Choose one", options=['Local files', 'Files from website'])


    put_table([
    [span('Example of FASTQ file', col=4),'',span('Example of experiment design file', col=2)],
    ['SampleName', 'FASTQ1', 'FASTQ2', 'strandness','','SampleName','Condition'],
    ['YourControl1', '/path/to/file.fastq', '/path/to/file.fastq', 'unknown','','YourControl1','0'],
    ['YourControl2', '/path/to/file.fastq', '/path/to/file.fastq', 'unknown','','YourControl2','0'],
    ['YourContrast1', '/path/to/file.fastq', '/path/to/file.fastq', 'unknown','','YourContrast1','1'],
    ['YourContrast2', '/path/to/file.fastq', '/path/to/file.fastq', 'unknown','','YourContrast2','1'],
    ])
    
    csv_file = file_upload("Please a list of FASTQ file in csv format", accept=".csv",  multiple = True,  placeholder='Choose a file')
    exp_design = file_upload("Please upload the experimental design in tab delimited format", accept=".csvcc",  multiple = True,  placeholder='Choose a file')
    
    put_text("Your files have been successfully inputed to the pipeline")
    
    list_control = []  # a list to hold all the individual pandas DataFrames
    for csvfile in csv_file:
        open(csvfile["filename"], "wb").write(csvfile["content"])
        df = pd.read_csv(csvfile["filename"])
        list_control.append(df)
        
    list_contrast = []  # a list to hold all the individual pandas DataFrames
    for csvfile in exp_design:
        open(csvfile["filename"], "wb").write(csvfile["content"])
        df = pd.read_csv(csvfile["filename"], sep = "\t")
        list_contrast.append(df)
        
    list_control[0].to_csv('./csv_file.csv', index = False)
    list_contrast[0].to_csv('./exp_design.txt',  sep='\t', index = False)
    
    file = open("FASTQ_check.txt","w")
    L = ["FASTQ"]
    file.writelines(L)
    file.close()

    if method == 'Files from website':
        img = file_upload("Select a image:", accept="image/*")

    



if __name__ == '__main__':
    FileInput()
