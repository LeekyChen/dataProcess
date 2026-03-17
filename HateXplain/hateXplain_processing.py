import json
import csv
from pathlib import Path

DATASET_PATH = Path(r"./dataset.json")
# OUTPUT_CSV_PATH = DATASET_PATH.with_name("hatexplain_processed.csv")
OUTPUT_CSV_PATH = Path(r"./HateXplain")

def _label_decision(annotators_list):
    """
    annotators_list: a list of dicts, each like {'label': 'hate/offensive/normal'}
    returns: 'hate', 'not_hate', or 'undecided'
    """

    hate_count = 0
    offensive_count = 0
    normal_count = 0

    for annotator in annotators_list:
        label = annotator["label"].lower()

        if label == "hate" or label == "hatespeech":
            hate_count += 1
        elif label == "offensive":
            offensive_count += 1
        elif label == "normal":
            normal_count += 1
        else:
            print(f"----异常 label：{label}-----")

    # 🧠 论文中的 undecided：hate/offensive/normal 各一票 -> 无多数意见
    if hate_count == offensive_count == normal_count:
        return "undecided"

    # 🧠 多数投票：决定最终类别
    # hate 多数 -> hate
    if offensive_count + normal_count > hate_count: return "not_hate"
    if offensive_count + normal_count < hate_count: return "hate"

    # 🧩 其他情况（理论上不会出现，但为了安全）
    # 例如 ties: (hate=2, offensive=2), (offensive=1, normal=1)
    print("--------异常---------")
    return "exception"


def process_dataset(input_path: Path = DATASET_PATH, output_csv_path: Path = OUTPUT_CSV_PATH) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for item in data.values():
        post_id = item['post_id']
        text = ' '.join(item['post_tokens'])
        label = _label_decision(item['annotators'])
        if label == 'undecided': continue
        rows.append((post_id, text, label))
    with open(output_csv_path.with_name('dataset_HateXplain.csv'), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["post_id", "text", "label"])
        writer.writerows(rows)

if __name__ == "__main__":

    # 按照原文的逻辑，二分类时 normal和 offensive都归为 not_hate
    # 如果三类各有一票，归为 undecided 共有919个 undecided的
    # 可生成两个数据集： GAB Twitter
    process_dataset()
