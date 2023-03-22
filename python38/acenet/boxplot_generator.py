import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import laspy


#used to load .las data into a laspy object.
def load_laspy(las_location):
      input_las = laspy.read(las_location)
      
      return input_las


# Convert a .LAS file into a pandas object.
def convert_laspy_pandas(input_las):
    # Convert data into pandas DataFrame
    df = pd.DataFrame({"X":input_las.X,"Y":input_las.Y,"Z":input_las.Z,
      "x":np.array(input_las.x),"y":np.array(input_las.y),"z":np.array(input_las.z),
     'intensity': input_las.intensity,
      'classification': input_las.classification,
      'return_number': np.array(input_las.return_number),
      'number_of_returns':np.array(input_las.number_of_returns),
      'synthetic':np.array(input_las.synthetic),
      'key_point':np.array(input_las.key_point),
      'withheld':np.array(input_las.withheld),
      'overlap':np.array(input_las.overlap),
      'scanner_channel':np.array(input_las.scanner_channel),
      'scan_direction_flag':np.array(input_las.scan_direction_flag),
      'user_data':input_las.user_data,
      'scan_angle':input_las.scan_angle,
      'point_source_id':input_las.point_source_id,
      'gps_time':input_las.gps_time    
      })

    return df


def export_boxplot(df,sub_dir,column = "X",by = "classification"):
    #Select which spatial dimension you wish to create a boxplot for
    if column == "X":
        column = "X"
    elif column == "Y":
        column = "Y"
    elif column == "Z":
        column = "Z"
    else:
        raise ValueError("column must be either X,Y, or Z.")
    
    df.boxplot(column=column, by='classification')
    plt.title("Boxplot of Classification Values for Dimension: " +str(column))
    
    #Create filename and save
    plot_file = os.path.join(sub_dir,'boxplot_{}.png'.format(str(column)))
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')



new_dir_path = 'Classification_Distribution_Boxplots'
os.makedirs(new_dir_path, exist_ok=True)

input_dir = "./"
output_dir = new_dir_path

for filename in os.listdir(input_dir):
    if filename.endswith(".las"):
        try:
            #os.makedirs(new_dir_path+ )
            las_path = os.path.join(input_dir, str(filename))
            output_path = os.path.join(output_dir, filename)

            numbers = re.findall("\d+", filename)
            words = re.findall('[a-zA-Z]+', filename)
            sub_dir = os.path.join(new_dir_path,words[0]+"_"+words[1]+"_"+numbers[0]+"-"+numbers[1])
            os.makedirs(sub_dir, exist_ok=True)
            print("Creating laspy object")
            print(input_dir)
            print(filename)
            print(las_path)

            input_las = load_laspy(las_location=las_path)
            print("create a pandas object")
            #create a pandas object
            df = convert_laspy_pandas(input_las)
            print("created df")
            #export the boxplots
            export_boxplot(df=df,sub_dir=sub_dir, column="X",by="classification")
            export_boxplot(df=df,sub_dir=sub_dir, column="Y",by="classification")
            export_boxplot(df=df,sub_dir=sub_dir, column="Z",by="classification")
            
            print(output_path)
        except:
            print("Could not process file: " + str(las_path))