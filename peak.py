import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.spatial.distance import cdist

# Load your data
test_data = pd.read_csv('./test_data.csv')
test = pd.read_csv('./test.csv')

# Define a function to segment data using peaks
def segment_by_peaks(data, feature_column, num_segments=27):
    """
    Segment data using peaks of the specified feature column.
    Args:
        data (DataFrame): Input data.
        feature_column (str): Column name to detect peaks.
        num_segments (int): Desired number of segments.
    Returns:
        List of DataFrames, each corresponding to a segment.
    """
    segments = []
    
    # Detect peaks in the specified feature column
    peaks, _ = find_peaks(data[feature_column], distance=len(data) // num_segments)
    
    # Ensure we have the desired number of segments by interpolating if necessary
    if len(peaks) < num_segments:
        peaks = np.linspace(0, len(data) - 1, num_segments, dtype=int)
    
    # Split the data based on detected peaks
    for i in range(len(peaks) - 1):
        segment = data.iloc[peaks[i]:peaks[i + 1]]
        segments.append(segment)
    
    # Add any remaining data as the last segment
    if len(peaks) > 0:
        segments.append(data.iloc[peaks[-1]:])
    
    return segments[:num_segments]

# Segment the test_data using peaks
segmented_means_by_peaks = []

for data_id, group in test_data.groupby('data_id'):
    # Segment data by peaks in a selected feature (e.g., Ax)
    segments = segment_by_peaks(group, feature_column='Ax', num_segments=27)
    
    # Compute mean for each segment
    for i, segment in enumerate(segments):
        segment_mean = segment[['Ax', 'Ay', 'Az', 'Gx', 'Gy']].mean()
        segment_mean['data_id'] = data_id
        segment_mean['swing_number'] = i + 1
        segmented_means_by_peaks.append(segment_mean)

# Convert segmented means to DataFrame
segmented_means_by_peaks_df = pd.DataFrame(segmented_means_by_peaks)

# Calculate Euclidean distances based on peak-segmented data
euclidean_results_peaks = []

# Extract test.csv values for comparison
test_values = test[['ax_mean', 'ay_mean', 'az_mean', 'gx_mean', 'gy_mean']].values


# Iterate through segmented data grouped by data_id
for data_id, group in segmented_means_by_peaks_df.groupby('data_id'):
    # Extract the values for the current data_id
    segment_values = group[['Ax', 'Ay', 'Az', 'Gx', 'Gy']].values

    # Compute Euclidean distances for all segments against test.csv
    distances = cdist(segment_values, test_values, metric='euclidean')

    # Find the minimum distance for each segment
    min_indices = distances.argmin(axis=1)
    min_distances = distances.min(axis=1)

    # Append results for the closest match of each segment
    for i, (closest_idx, closest_distance) in enumerate(zip(min_indices, min_distances)):
        euclidean_results_peaks.append({
            'data_id': data_id,
            'swing_number': i + 1,
            'closest_test_data_ID': test.iloc[closest_idx]['data_ID'],
            'distance': closest_distance
        })

# Convert results to DataFrame and filter by minimum distance per data_id
euclidean_results_peaks_df = pd.DataFrame(euclidean_results_peaks)
filtered_euclidean_results_peaks_df = euclidean_results_peaks_df.loc[
    euclidean_results_peaks_df.groupby('data_id')['distance'].idxmin()]

# Save or display the results
filtered_euclidean_results_peaks_df.to_csv('peakp16.csv', index=False)
