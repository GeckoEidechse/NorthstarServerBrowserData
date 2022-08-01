# %%
"""
Sample script to extract archives and draw plot playbase plot over entire timeframe

Requires the following Python packages:
- pyunpack
- patool
- pandas
- matplotlib

Install them with:
 pip install pyunpack patool pandas matplotlib
"""

# Imports
import pandas as pd
import json
import os
from pyunpack import Archive
import pathlib

# Static global variables
ARCHIVE_DATA_DIRECTORY = "../../data/"
UNCOMPRESSED_DATA_DIRECTORY = "uncompressed-data/"

# Make folder if not exists
pathlib.Path(UNCOMPRESSED_DATA_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Extract archives into single directory
# Depending on the size of the data this takes a bit to finish
for root, subdirs, files in os.walk(ARCHIVE_DATA_DIRECTORY):
    for file in sorted(files):
        if file.endswith(".7z"):
            filepath = root + '/' + file
            print(filepath)

            # Extract current archive
            Archive(filepath).extractall(UNCOMPRESSED_DATA_DIRECTORY)

# Get list of all JSON files
files = [UNCOMPRESSED_DATA_DIRECTORY +
         elem for elem in os.listdir(UNCOMPRESSED_DATA_DIRECTORY)]
files

# %%
# Get lists of timestamps, playercounts, and gameservers
timestamp = list()
playercount = list()
servers = list()
for file in files:
    with open(file, 'rt') as f:

        # Check if valid JSON
        try:
            current_json = json.load(f)
        except json.JSONDecodeError:
            # The file was not actually JSON so we skip it
            continue

        # Get playercount by adding up playercount of individual servers
        total_players = 0
        for server in current_json:
            total_players += server['playerCount']
        playercount.append(total_players)

        # Get timestamp from filename
        timestamp.append(file.replace(
            UNCOMPRESSED_DATA_DIRECTORY, "").replace(".json", ""))

        # Get server count by number of server entries in JSON response
        servers.append(len(current_json))


# %%
# Combine lists into a pandas dataframe for processing
df = pd.DataFrame(
    zip(
        timestamp,
        playercount,
        servers
    ),
    columns=["timestamp", "players", "servers"]
)

# Convert timestamps to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
# and make it the index
df = df.set_index("timestamp")

# %%
# Filter out serverspam
# set to value that was never reached outside of server spam
PLAYERCOUNT_UPPER_LIMIT = 1000
filtered_df = df[df['players'] < 1000]

# %%
# Plot graph
plot = filtered_df.plot()
# and save the plot
fig = plot.get_figure()
fig.savefig("output.png", dpi=300)

# %%
