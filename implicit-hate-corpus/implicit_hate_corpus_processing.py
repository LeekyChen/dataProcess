import os

import pandas as pd


def process_hate_speech_data(input_file, output_file):
    SAMPLE_SIZE = 6000
    RANDOM_SEED = 42

    df = pd.read_csv(input_file, sep="\t")

    df = df[df["class"] != "explicit_hate"].copy()

    label_map = {
        "implicit_hate": "hate",
        "not_hate": "not_hate",
    }
    df["label"] = df["class"].map(label_map)
    df = df.dropna(subset=["label"]).copy()

    df = df.rename(columns={"post": "text"})
    df["text"] = df["text"].astype(str)
    df["text"] = df["text"].str.replace("\r", " ", regex=False)
    df["text"] = df["text"].str.replace("\n", " ", regex=False)
    df["text"] = df["text"].str.strip()
    df = df[df["text"] != ""].copy()

    not_hate_df = df[df["label"] == "not_hate"]
    hate_df = df[df["label"] == "hate"]

    sample_size = min(SAMPLE_SIZE, len(df))
    not_hate_sample_num = round(sample_size * len(not_hate_df) / len(df))
    hate_sample_num = sample_size - not_hate_sample_num

    not_hate_sample = not_hate_df.sample(n=not_hate_sample_num, random_state=RANDOM_SEED)
    hate_sample = hate_df.sample(n=hate_sample_num, random_state=RANDOM_SEED)
    sampled_df = pd.concat([not_hate_sample, hate_sample])
    sampled_df = sampled_df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

    final_df = sampled_df[["text", "label"]].copy()
    final_df.insert(0, "id", range(1, len(final_df) + 1))

    final_df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"Original labels:\n{df['label'].value_counts()}")
    print(f"Sampled labels:\n{final_df['label'].value_counts()}")
    print(f"Done. Saved {len(final_df)} rows to {output_file}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    input_tsv = os.path.join(BASE_DIR, "implicit_hate_v1_stg1_posts.tsv")
    output_csv = os.path.join(BASE_DIR, "dataset_implicit.csv")

    process_hate_speech_data(input_tsv, output_csv)
