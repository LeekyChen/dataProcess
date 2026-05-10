import csv
import os
import random


def data_process():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_CSV_PATH = os.path.join(BASE_DIR, "train.csv")
    OUTPUT_CSV_PATH = os.path.join(BASE_DIR, "dataset_CHSD.csv")

    SAMPLE_SIZE = 6000
    RANDOM_SEED = 42

    rows = []
    with open(INPUT_CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for data in reader:
            text = data["text"].replace("\r", " ").replace("\n", " ").strip()
            label_id = data["label"]

            if label_id == "0":
                label = "not_hate"
            elif label_id == "1":
                label = "hate"
            else:
                continue

            if text == "":
                continue

            rows.append((text, label))

    not_hate_rows = [row for row in rows if row[1] == "not_hate"]
    hate_rows = [row for row in rows if row[1] == "hate"]

    sample_size = min(SAMPLE_SIZE, len(rows))
    not_hate_sample_num = round(sample_size * len(not_hate_rows) / len(rows))
    hate_sample_num = sample_size - not_hate_sample_num

    random.seed(RANDOM_SEED)
    sampled_rows = random.sample(not_hate_rows, not_hate_sample_num)
    sampled_rows += random.sample(hate_rows, hate_sample_num)
    random.shuffle(sampled_rows)

    output_rows = []
    for index, row in enumerate(sampled_rows):
        text, label = row
        output_rows.append((index + 1, text, label))

    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "label"])
        writer.writerows(output_rows)

    print(f"原始数据：not_hate={len(not_hate_rows)}，hate={len(hate_rows)}，总数={len(rows)}")
    print(f"抽样数据：not_hate={not_hate_sample_num}，hate={hate_sample_num}，总数={len(output_rows)}")
    print(f"处理完毕！共保留了 {len(output_rows)} 条有效数据。")


if __name__ == "__main__":
    data_process()
