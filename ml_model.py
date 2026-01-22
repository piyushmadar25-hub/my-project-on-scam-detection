import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class ScamMLModel:
    """
    ML model for scam detection using TF-IDF + Logistic Regression.
    """

    def __init__(self):
        self.pipeline = Pipeline([
            ("vectorizer", TfidfVectorizer(
                max_features=3000,
                ngram_range=(1, 2),
                stop_words="english"
            )),
            ("classifier", LogisticRegression(
                solver="liblinear",
                class_weight="balanced"
            ))
        ])

    def train(self, texts, labels):
        self.pipeline.fit(texts, labels)

    def predict_probability(self, text):
        return self.pipeline.predict_proba([text])[0][1]

    def save(self, path="scam_model.pkl"):
        joblib.dump(self.pipeline, path)

    def load(self, path="scam_model.pkl"):
        self.pipeline = joblib.load(path)
