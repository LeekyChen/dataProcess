import pandas as pd


def data_process():
    df = pd.read_csv(r"test_suite_cases.csv")
    rows = []
    for index, row in df.iterrows():
        case_id = row['case_id']
        text = row['test_case']
        label_gold = row['label_gold']
        if label_gold == 'hateful': label = 'hate'
        elif label_gold == 'non-hateful': label = 'not_hate'
        rows.append((case_id, text, label))
    out_df = pd.DataFrame(rows, columns=["case_id", "text", "label"])
    out_df.to_csv(r"dataset_HateCheck.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    data_process()

