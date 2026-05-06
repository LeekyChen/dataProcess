import pandas as pd

def process_hate_speech_data(input_file, output_file):
    # 1. 读取 TSV 文件
    # sep='\t' 表示按制表符分割
    # quoting=3 (csv.QUOTE_NONE) 有助于处理原始文本中复杂的引号
    df = pd.read_csv(input_file, sep='\t', quoting=0)

    # 2. 定义映射和过滤逻辑
    # 如果 class 是 explicit_hate 则跳过
    df = df[df['class'] != 'explicit_hate'].copy()

    # 3. 转换标签
    # implicit_hate -> hate, not_hate -> not_hate
    label_map = {
        'implicit_hate': 'hate',
        'not_hate': 'not_hate'
    }
    df['label'] = df['class'].map(label_map)

    # 4. 准备最终的格式
    # 重命名 post 为 text
    df = df.rename(columns={'post': 'text'})

    # 5. 生成 ID (使用 iterrows 风格的 index)
    # 重置索引并将其命名为 id
    df.index.name = 'id'
    df = df.reset_index()

    # 6. 只保留要求的字段
    final_df = df[['id', 'text', 'label']]

    # 7. 保存为 CSV
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"处理完成！文件已保存至: {output_file}")
    print(f"统计信息:\n{final_df['label'].value_counts()}")

if __name__ == "__main__":
    # 请确保文件名与你实际的文件名一致
    input_tsv = r"./implicit_hate_v1_stg1_posts.tsv"
    output_csv = "dataset_implicit.csv"
    
    process_hate_speech_data(input_tsv, output_csv)