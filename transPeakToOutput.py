import pandas as pd

# 讀取 CSV 檔案
filtered_matches_path = './peakp12.csv'
answer_path = './answer099.csv'

filtered_matches = pd.read_csv(filtered_matches_path)
answer = pd.read_csv(answer_path)

# 透過 closest_test_data_ID 與 answer 的 data_ID 進行合併
merged_data = filtered_matches.merge(answer, left_on='closest_test_data_ID', right_on='data_ID', suffixes=('', '_answer'))

# 選取需要的欄位
selected_columns = ['data_id', 'gender', 'hold racket handed', 'play years_0', 'play years_1', 
                    'play years_2', 'level_0', 'level_1', 'level_2']

# 確保 data_id 與 Filtered_Closest_Matches_with_Minimum_Distance_per_data_id.csv 的一致
final_output = filtered_matches[['data_id']].merge(
    merged_data[selected_columns], on='data_id', how='left'
)

# 將結果輸出為新的 CSV 檔案
corrected_output_path = 'p206.csv'
final_output.to_csv(corrected_output_path, index=False)

print(f"結果已儲存至 {corrected_output_path}")
