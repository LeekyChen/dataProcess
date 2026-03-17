import pandas as pd
import os

xlsx_path = r"./ICWSM18_SALMINEN_ET_AL.xlsx"

sheet_names = [
    "Accusations",
    "Promoting Violence",
    "Humiliation",
    "Financial Power",
    "Political Issues",
    "Racism & Xenophobia",
    "Religion",
    "Swearing",
    "Specific Nation(s)",
    "Specific Person",
    "Media",
    "Armed Forces",
    "Behavior",
    "Neutral"
]

target_columns = ["ID", "message", "Class"]

all_data = []
seen_ids = set()
duplicate_count = 0

for sheet in sheet_names:
    print(f"\n正在读取 sheet: {sheet}")

    try:
        df = pd.read_excel(
            xlsx_path,
            engine="openpyxl",
            sheet_name=sheet,
            usecols=target_columns
        )

        unique_rows = []

        for _, row in df.iterrows():
            if pd.isna(row['message']) or str(row['message']).strip() == '': continue
            id_ = row["ID"]

            if id_ in seen_ids:
                duplicate_count += 1
                print(f"[重复ID] Sheet={sheet}, ID={id_}")
                continue

            seen_ids.add(id_)

            # ✅ Class → label 映射
            raw_class = row["Class"]
            if raw_class == "Hateful":
                label = "hate"
            elif raw_class == "Neutral":
                label = "not_hate"
            else:
                label = "unknown"

            row_data = {
                "ID": row["ID"],
                "text": row["message"],
                "label": label,
                "source_sheet": sheet
            }

            unique_rows.append(row_data)

        if unique_rows:
            all_data.append(pd.DataFrame(unique_rows))

        print(f"{sheet}：原始 {len(df)} 条 → 保留 {len(unique_rows)} 条")

    except Exception as e:
        print(f"读取 {sheet} 时出错：{e}")

combined_df = pd.concat(all_data, ignore_index=True)
combined_df = combined_df[["ID", "text", "label", "source_sheet"]]

output_csv = r"./dataset_YouTubeFacebook.csv"
combined_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

print("\n========== 汇总 ==========")
print(f"去重后总数据条数：{len(combined_df)}")
print(f"重复 ID 总数：{duplicate_count}")
print(f"保存路径：{os.path.abspath(output_csv)}")

final_duplicates = combined_df["ID"].duplicated().sum()
print(f"最终重复 ID 数（应为 0）：{final_duplicates}")



# 正在读取 sheet: Neutral
# Neutral：原始 858 条 → 保留 858 条
#
# ========== 汇总 ==========
# 去重后总数据条数：3228
# 重复 ID 总数：1416
# 保存路径：D:\Lab\PyCharmLab\dataset\datasetProcess\YouTubeFacebook\dataset_YouTubeFacebook.csv
# 最终重复 ID 数（应为 0）：0