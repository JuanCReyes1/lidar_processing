import laspy
import numpy as np
import os

def filter_point_cloud(las_path, output_path, quarter_size=1000):
    # Load the LAS file
    las = laspy.read(las_path)

    # Compute the x, y, and z quartiles
    x_quarter = np.percentile(las.x, [25, 50, 75])
    y_quarter = np.percentile(las.y, [25, 50, 75])
    z_quarter = np.percentile(las.z, [25, 50, 75])

    # Filter out points outside the inner quartile range
    x_mask = np.logical_and(las.x >= x_quarter[0] - quarter_size, las.x <= x_quarter[2] + quarter_size)
    y_mask = np.logical_and(las.y >= y_quarter[0] - quarter_size, las.y <= y_quarter[2] + quarter_size)
    z_mask = np.logical_and(las.z >= z_quarter[0] - quarter_size, las.z <= z_quarter[2] + quarter_size)
    mask = np.logical_and(np.logical_and(x_mask, y_mask), z_mask)
    las_filtered = las[mask]

    # Write the filtered point cloud to a new LAS file
    las_filtered.write(output_path)

new_dir_path = './Cleaned_Data_Quarterlies'
os.makedirs(new_dir_path, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".las"):
        las_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        filter_point_cloud(las_path, output_path)
        print("File processed and cleaned: " + output_path)