import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_histogram_map(input_file, item):
    
    filename = os.path.basename(input_file)
    save_to_path = os.path.dirname(input_file)
    # Load the CSV file
    data = pd.read_csv(input_file, skiprows=70)

    # Calculate low_limit and high_limit dynamically
    low_limit = data[item].quantile(0.05)  # 5th percentile
    high_limit = data[item].quantile(0.95) # 95th percentile

    print(f"Automatically calculated limits: low_limit = {low_limit}, high_limit = {high_limit}")

    # Filter data based on the limits
    filtered_data = data[(data[item] >= low_limit) & (data[item] <= high_limit)]

    # Automatically calculate number of bins using Freedman-Diaconis rule
    bins = calculate_bins(filtered_data[item])
    print(f"Automatically calculated bins: {bins}")

    w = data['PosX'].max() - data['PosX'].min() + 1    
    h = data[' PosY'].max() - data[' PosY'].min() + 1
    filename = f'{filename}_{item}_{w}x{h}'

    # Plot a histogram
    plt.figure(figsize=(10, 6))
    plt.hist(filtered_data[item], bins=bins, color='blue', edgecolor='black')
    plt.xlabel(item)
    plt.ylabel('LED count')
    plt.title(filename + '_Histogram')
    output_file = os.path.join(save_to_path, f'{filename}_{item}_Histogram.png')
    plt.savefig(output_file)

    # Pivot the data to prepare it for a heatmap
    heatmap_data = data.pivot_table(values=item, index=' PosY', columns='PosX', fill_value=0)
    
    if(w*h > 2000):
        show_value = False
    else:
        show_value = True

    # Create the heatmap        
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        heatmap_data, 
        cmap='viridis', 
        vmin=low_limit, 
        vmax=high_limit, 
        annot=show_value,           # Show values in each cell
        fmt=".1f",            # Format for the displayed values (e.g., one decimal place)
        cbar_kws={'label': item}
    )
    # Set plot labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(filename + '_Map')

    # Show and save the plot
    output_file = os.path.join(save_to_path, f'{filename}_{item}_Map.png')
    plt.savefig(output_file)
    
def calculate_bins(data_column):
    q25, q75 = np.percentile(data_column, [25, 75])  # Calculate the interquartile range
    iqr = q75 - q25
    bin_width = 2 * iqr / len(data_column) ** (1 / 3)  # Freedman-Diaconis formula
    bin_count = int((data_column.max() - data_column.min()) / bin_width)
    return max(10, bin_count)  # Ensure a reasonable minimum number of bins


if __name__ == '__main__':
        # Load the CSV file containing coordinates
    input_file = '/Users/galong/RayleighVision/EL/KK/EL/B-JG7L08810-100ea.csv'
    item = 'WLD1'
    plot_histogram_map(input_file, item)