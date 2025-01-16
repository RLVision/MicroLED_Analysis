import os
import PL_EL_Histogram_Map as his_map


def PL_EL_Histogram_Map_batch_from_path(path):
    # List all files in the directory
    all_files = os.listdir(path)
    
    # Filter for CSV files
    csv_files = [f for f in all_files if f.endswith('.csv')]
    
    # Iterate through CSV files
    for csv_file in csv_files:
        file_path = os.path.join(path, csv_file)
        print(f"Reading file: {csv_file}")
        
        # Read CSV into a DataFrame
        try:
            his_map.plot_histogram_map(file_path, 'WLD1')

            print(f"File {csv_file} processed successfully.")

        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            

    

if __name__ == '__main__':
    PL_EL_Histogram_Map_batch_from_path('/Users/galong/RayleighVision/EL/KK/EL')