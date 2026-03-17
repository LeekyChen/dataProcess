import pandas as pd

df = pd.read_csv(r"olid-training-v1.0.tsv", sep="\t")
post_id_list = []
tweet_list = []
label_list = []
for index, row in df.iterrows():
    tweet_list.append(row['tweet'])
    flag = row['subtask_a']
    post_id_list.append(row['id'])
    if flag == "OFF": label_list.append("hate")
    else: label_list.append("not_hate")
ansDf = pd.DataFrame({
    "post_id": post_id_list,
    "text": tweet_list,
    "label": label_list
})
ansDf.to_csv("dataset_OLID.csv", encoding="utf-8", index=False)