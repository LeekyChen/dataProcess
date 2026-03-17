from datasets import load_dataset
import csv

def data_process():
    ds = load_dataset("ucberkeley-dlab/measuring-hate-speech")
    print(111)
    OUTPUT_CSV_PATH = r"./dataset_MHS.csv"

    rows = []
    for index, data in enumerate(ds['train']):
        comment_id = data['comment_id']
        text = data['text']
        score = data['hate_speech_score']

        if score > 0.5: label = 'hate'
        elif score < -1: label = 'not_hate'
        else: continue # 模糊不清的要跳过
        rows.append((comment_id, text, label))

    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["comment_id", "text", "label"])
        writer.writerows(rows)

if __name__ == "__main__":
    # 模糊不清的样本要跳过
    data_process()


