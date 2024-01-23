import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# TODO
# ADD CUSTOMIZABILITY FOR COLORS AND LINESTYLE/WIDTHS
# ALSO ADD THE FUNCTIONALITY FOR NOTES BUT THAT NEED THE csv_importer.cpp to be updated
# CHANGE LINEWIDTH BASED ON OVERALL VOLUME PERCENTILE e.g. a level with 6K volume has more "weight" than 2K volume

'''
FORMAT FOR CSVs ->
Price | Color | LineStyle | LineWidth | TextAlignment | DateTime
'''

def plot_vol_and_delta(file_path: str, symbol: str) -> None:
    """
    Parameters:
    - input_file_path (str): File path for the input .csv with data
    - symbol (str): What the symbol being plotted is

    Returns:
    - None: Just writes to a file
    """
        
    # Read the CSV file
    dataset = pd.read_csv(file_path)

    # Extract data columns
    volume = dataset.iloc[:, 6:7].values
    askVolume = dataset.iloc[:, 8:9].values
    bidVolume = dataset.iloc[:, 9:10].values

    # Create subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    # Plot Volume distribution
    if (symbol != "ES"):
        axes[0].hist(volume, range=[0, 5000], color='blue', edgecolor='black', bins=250)
    else:
        axes[0].hist(volume, range=[0, 25000], color='blue', edgecolor='black', bins=500)
    axes[0].set_title('Histogram of Bar Volume')
    axes[0].set_xlabel('Volume')
    axes[0].set_ylabel('# of occurrences')

    # Plot Delta distribution
    if (symbol != "ES"):
        axes[1].hist(askVolume - bidVolume, range=[-1000, 1000], color='blue', edgecolor='black', bins=1000)
    else:
        axes[1].hist(askVolume - bidVolume, range=[-2500, 2500], color='blue', edgecolor='black', bins=2500)
    
    axes[1].set_title('Histogram of Delta (Ask Volume - Bid Volume)')
    axes[1].set_xlabel('Delta')
    axes[1].set_ylabel('# of occurrences')

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Show the plots
    plt.show()

def get_volume_levels(input_file_path: str, output_file_path: str, threshold: int, dynamic_linewidth: bool=True) -> None:
    """
    Parameters:
    - input_file_path (str): File path for the input .csv with data
    - output_file_path (str): File path for the destination csv
    - threshold (int) : Volume needed to trigger a level
    - dynamic_linewidth (bool) : Use percentiles for dynamic line widths (1-3)

    Returns:
    - None: Just writes to a file
    """
    percentiles = [33,66]
    
    # handling the opening and data filtering conditions
    data = pd.read_csv(input_file_path)
    data.columns = [col.strip() for col in data.columns]
    filtered_df = data[data["Volume"] > threshold]

    # Calculate percentiles for Volume
    volume_percentiles = filtered_df["Volume"].quantile([p / 100 for p in percentiles])
    # Create dynamic line widths based on percentiles
    line_widths = filtered_df["Volume"].apply(lambda x: sum(x >= volume_percentiles) + 1)


    # parsing and combining the date times to let the csv_importer study work properly
    date_time_array = []
    for i, time in enumerate(filtered_df["Time"]):
        temp_arr = time.split(":")
        date_time_array.append(filtered_df["Date"].iloc[i] + '/' + temp_arr[0].strip() + '/' + temp_arr[1] + '/' + temp_arr[2][0:2])

    # creating the final dataframe to push to the csv
    final_df = pd.DataFrame({
        "Price" : (filtered_df["Open"] + filtered_df["Low"]) / 2,
        "Color" : ["white"] * len(date_time_array),
        "LineStyle" : [1] * len(date_time_array),
        "LineWidth" : [1] * len(date_time_array) if not dynamic_linewidth else line_widths.tolist(),
        "TextAlignment" : [1] * len(date_time_array),
        "DateTime" : date_time_array,
        })
    
    # clearing the csv to write fresh values
    with open(output_file_path, 'w', newline='') as file:
        pass
    
    final_df.to_csv(output_file_path, index=False)

def get_delta_levels(input_file_path: str, output_file_path: str, threshold: int, dynamic_linewidth: bool=True) -> None:
    """
    Parameters:
    - input_file_path (str): File path for the input .csv with data
    - output_file_path (str): File path for the destination csv.
    - threshold (int) : Absolute value of delta needed for a level to trigger
    - dynamic_linewidth (bool) : Use percentiles for dynamic line widths (1-3)

    Returns:
    - None: Just writes to a file
    """
    percentiles = [33, 66]

    # handling the opening and data filtering conditions
    data = pd.read_csv(input_file_path)
    data.columns = [col.strip() for col in data.columns]
    delta_condition = abs(data["AskVolume"] - data["BidVolume"]) > threshold
    filtered_df = data[delta_condition]
    color_array = np.where((data["AskVolume"].loc[delta_condition] - data["BidVolume"].loc[delta_condition] > 0), "cyan", "red")

     # Calculate percentiles for Delta
    delta_percentiles = filtered_df["AskVolume"].sub(filtered_df["BidVolume"]).quantile([p / 100 for p in percentiles])
    # Create dynamic line widths based on percentiles
    line_widths = (filtered_df["AskVolume"] - filtered_df["BidVolume"]).apply(lambda x: sum(x >= delta_percentiles) + 1)

    # parsing and combining the date times to let the csv_importer study work properly
    date_time_array = []
    for i, time in enumerate(filtered_df["Time"]):
        temp_arr = time.split(":")
        date_time_array.append(filtered_df["Date"].iloc[i] + '/' + temp_arr[0].strip() + '/' + temp_arr[1] + '/' + temp_arr[2][0:2])
    
    # creating the final dataframe to push to the csv
    final_df = pd.DataFrame({
        "Price" : (filtered_df["Open"] + filtered_df["Low"]) / 2,
        "Color" : color_array,
        "LineStyle" : [1] * len(date_time_array),
        "LineWidth" : [1] * len(date_time_array) if not dynamic_linewidth else line_widths,
        "TextAlignment" : [1] * len(date_time_array),
        "DateTime" : date_time_array,
        })
    
    # clearing the csv to write fresh values
    with open(output_file_path, 'w', newline='') as file:
        pass
    
    final_df.to_csv(output_file_path, index=False)
