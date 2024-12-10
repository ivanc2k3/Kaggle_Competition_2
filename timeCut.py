import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from collections import Counter

# 載入數據
test_data = pd.read_csv('./test_data.csv')  # 替換為實際文件路徑
test = pd.read_csv('./test.csv')  # 替換為實際文件路徑
answer_data = pd.read_csv('./answer099.csv')  # 替換為實際文件路徑

# 初始化結果列表
results = []

# 獲取所有唯一的 data_id
unique_data_ids = test_data['data_id'].unique()

# 逐個處理每個 data_id
for data_id in unique_data_ids:
    # 過濾出該 data_id 的數據
    data_subset = test_data[test_data['data_id'] == data_id]
    
    
    # 將數據分成 27 等分
    num_rows = len(data_subset)
    chunk_size = num_rows // 27
    remainder = num_rows % 27

    chunks = []
    start = 0
    for i in range(27):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(data_subset.iloc[start:end])
        start = end

    # 計算每個等分的 Ax, Ay, Az, Gx, Gy, Gz 的 mean
    means = []
    for chunk in chunks:
        mean_values = chunk[['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']].mean().values
        means.append(mean_values)

    # 對每個等分與 test.csv 中的數據計算歐幾里得距離，找到最近的
    nearest_data_IDs = []
    for mean in means:
        min_distance = float('inf')
        nearest_row = None

        for _, test_row in test.iterrows():
            test_values = test_row[['ax_mean', 'ay_mean', 'az_mean', 'gx_mean', 'gy_mean', 'gz_mean']].values
            distance = euclidean(mean, test_values)

            if distance < min_distance:
                min_distance = distance
                nearest_row = test_row

        nearest_data_IDs.append(nearest_row['data_ID'])

    # 根據最近的 data_ID 對應 answer.csv 中的屬性
    attributes = []

    for nearest_id in nearest_data_IDs:
        matched_row = answer_data[answer_data['data_ID'] == nearest_id]
        attributes.append(matched_row[['gender', 'hold racket handed', 'play years_0', 'play years_1', 'play years_2', 'level_0', 'level_1', 'level_2']].values[0])

    # 統計屬性中最多的值作為該 data_id 的答案
    most_common = []
    for i in range(len(attributes[0])):
        col_values = [attr[i] for attr in attributes]
        most_common.append(Counter(col_values).most_common(1)[0][0])

    # 將結果添加到列表
    results.append([data_id] + most_common)

# 將結果存入 CSV
output_df = pd.DataFrame(results, columns=['data_id', 'gender', 'hold racket handed', 'play years_0', 'play years_1', 'play years_2', 'level_0', 'level_1', 'level_2'])
output_df.to_csv('p310.csv', index=False)
