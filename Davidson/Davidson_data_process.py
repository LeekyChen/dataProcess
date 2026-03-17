import pandas as pd

def data_process():
    dataset_path = r"./labeled_data.csv"
    output_path = "./dataset_Davidson.csv"

    df = pd.read_csv(dataset_path)
    rows = []
    for index, row in df.iterrows():
        _id = row['id']
        text = row['tweet']
        class_ = row['class']
        if class_ == 0: label = 'hate'
        elif class_ == 1 or class_ == 2: label = "not_hate"
        # if class_ == 0: label = 'hate speech'
        # elif class_ == 1: label = 'offensive language'
        # elif class_ == 2: label = "neither"
        else:
            print(f"异常，文本为：{text}")
            continue
        rows.append((_id, text, label))

    out_df = pd.DataFrame(rows, columns=["id", "text", "label"])
    out_df.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == '__main__':
    data_process()