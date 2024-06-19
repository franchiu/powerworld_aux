import pandas as pd
from datetime import datetime
import re
import glob

def parse_raw_load_data(input_file_path):
    file_pattern = input_file_path + '*Monthly.Auction.NetworkModel_PeakWD.raw'

    # Use glob to find the file path
    files = glob.glob(file_pattern)

    if files:
        file_path = files[0]  # Assuming you only expect one matching file
    else:
        raise FileNotFoundError(f"No matching file found in directory: {input_file_path}")

    saving_lines = False
    filtered_lines = []

    # Define the start and end markers
    start_marker = 'BEGIN LOAD DATA'
    end_marker = 'END OF LOAD DATA'

    # Read the file and filter lines
    with open(file_path, 'r') as file:
        for line in file:
            if start_marker in line:
                saving_lines = True
            elif end_marker in line:
                saving_lines = False
                break  # Stop saving lines once we reach the end marker
            elif saving_lines:
                filtered_lines.append(line.strip())

    loads_data = []
    pattern = r'\[(.*?)\]'  # Regex pattern to match text within square brackets

    for line in filtered_lines:
        match = re.search(pattern, line)
        if match:
            loads_data.append(match.group(1).strip().split())

    loads_data = pd.DataFrame(loads_data, columns = ['Bus ID', 'Load Name', 'Load ID', '_'])
    loads_data.set_index('Load Name', inplace=True)

    return loads_data