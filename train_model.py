import os
import pandas as pd
from ml_model import ScamMLModel


def load_data_from_csv(csv_path: str, limit: int = 200):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path, encoding="latin-1")

    # Normalize column names
    df.columns = [col.lower().strip() for col in df.columns]

    # Auto-detect label and message columns
    if "label" in df.columns and "message" in df.columns:
        label_col = "label"
        text_col = "message"
    elif "v1" in df.columns and "v2" in df.columns:
        label_col = "v1"
        text_col = "v2"
    elif "category" in df.columns and "message" in df.columns:
        label_col = "category"
        text_col = "message"
    else:
        raise ValueError(f"Unsupported CSV format. Found columns: {df.columns}")

    scam_df = df[df[label_col] == "spam"].head(limit)
    legit_df = df[df[label_col] == "ham"].head(limit)

    if len(scam_df) < limit or len(legit_df) < limit:
        raise ValueError("Not enough spam/ham samples in dataset")

    return scam_df[text_col].tolist(), legit_df[text_col].tolist()


def main():
    scam_texts, legit_texts = load_data_from_csv(
        "data/sms_spam.csv", limit=200
    )

    texts = scam_texts + legit_texts
    labels = [1] * len(scam_texts) + [0] * len(legit_texts)

    model = ScamMLModel()
    model.train(texts, labels)
    model.save()

    print("✅ Model trained successfully")
    print(f"Scam samples: {len(scam_texts)}")
    print(f"Legit samples: {len(legit_texts)}")


if __name__ == "__main__":
    main()
