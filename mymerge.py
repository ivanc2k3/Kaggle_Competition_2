import pandas as pd

# 文件路徑
main_csv = "99v.csv"
gender_csv = "gender_mul.csv"
hand_csv = "hand_mul.csv"
pyll_csv = "pyll.csv"
output_csv = "p1016.csv"
p200 = "p206.csv"

# 讀取主檔
main_df = pd.read_csv(main_csv)

# 將 data_id 設為索引，方便後續處理
main_df.set_index("data_id", inplace=True)

# 讀取其他資料並設為索引
gender_df = pd.read_csv(pyll_csv).set_index("data_id")
hand_df = pd.read_csv(pyll_csv).set_index("data_id")
pyll_df = pd.read_csv(p200).set_index("data_id")

# 檢查 data_id 是否連續
all_ids = pd.RangeIndex(start=main_df.index.min(), stop=main_df.index.max() + 1)
missing_ids = all_ids.difference(main_df.index)

# 如果有缺失的 data_id，從其他資料補充
if not missing_ids.empty:
    print(f"發現缺失的 data_id：{missing_ids.tolist()}")
    # 建立缺失資料的 dataframe
    missing_data = pd.DataFrame(index=missing_ids)
    missing_data.index.name = 'data_id'  # 確保索引名稱為 data_id

    # 從 gender_df 補充
    if 'gender' in main_df.columns:
        missing_data['gender'] = gender_df.reindex(missing_ids)['gender']

    # 從 hand_df 補充
    if 'hold racket handed' in main_df.columns:
        missing_data['hold racket handed'] = hand_df.reindex(missing_ids)['hold racket handed']

    # 從 pyll_df 補充
    pyll_columns = ["play years_0", "play years_1", "play years_2", "level_0", "level_1", "level_2"]
    for col in pyll_columns:
        if col in main_df.columns:
            missing_data[col] = pyll_df.reindex(missing_ids)[col]

    # 將補充的資料與主檔合併
    main_df = pd.concat([main_df, missing_data])

# 合併後可能會使索引名稱丟失，故再次指定索引名稱
main_df.index.name = 'data_id'

# 重置索引為欄位
main_df.reset_index(inplace=True)

# 按 data_id 排序
main_df.sort_values(by="data_id", inplace=True)

# 保存結果
main_df.to_csv(output_csv, index=False)

print(f"補全完成，結果已存至：{output_csv}")
