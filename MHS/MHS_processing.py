from datasets import load_dataset
import csv

def data_process():
    ds = load_dataset("ucberkeley-dlab/measuring-hate-speech")
    print(111)
    OUTPUT_CSV_PATH = r"dataset_MHS.csv"

    rows = []
    seen_ids = set()  # 新增：用来记录已经见过的 comment_id
    for index, data in enumerate(ds['train']):
        print(f"index:{index}")
        comment_id = data['comment_id']

        # 新增：如果这个 id 已经被处理过了，直接跳过
        if comment_id in seen_ids:
            continue

        text = data['text']
        score = data['hate_speech_score']

        if score > 0.5: label = 'hate'
        elif score < -1: label = 'not_hate'
        else: continue # 模糊不清的要跳过
        rows.append((comment_id, text, label))
        seen_ids.add(comment_id)  # 新增：把刚才处理的 id 扔进集合里

    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["comment_id", "text", "label"])
        writer.writerows(rows)

    print(f"处理完毕！去重后共保留了 {len(rows)} 条有效数据。")
if __name__ == "__main__":
    # 模糊不清的样本要跳过，且保证 comment_id 不重复
    data_process()