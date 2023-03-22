import pandas as pd
import matplotlib.pyplot as plt
import re
import os
from laspy_functions import load_laspy, convert_laspy_pandas, export_boxplot

new_dir_path = 'Classification_Distribution_Boxplots'
os.makedirs(new_dir_path, exist_ok=True)

input_dir = "./"
output_dir = new_dir_path

for filename in os.listdir(input_dir):
    if filename.endswith(".las"):
        try:
            #os.makedirs(new_dir_path+ )
            las_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            numbers = re.findall("\d+", filename)
            words = re.findall('[a-zA-Z]+', filename)
            sub_dir = os.path.join(new_dir_path,words[0]+"_"+words[1]+"_"+numbers[0]+"-"+numbers[1])
            os.makedirs(sub_dir, exist_ok=False)

            input_las = load_laspy(las_location=las_path)

            #create a pandas object
            df = convert_laspy_pandas(input_las)
            #export the boxplots
            export_boxplot(df=df,sub_dir=sub_dir, column="X",by="classification")
            export_boxplot(df=df,sub_dir=sub_dir, column="Y",by="classification")
            export_boxplot(df=df,sub_dir=sub_dir, column="Z",by="classification")
            
            print(output_path)
        except:
            print("Could not process file: " + str(las_path))