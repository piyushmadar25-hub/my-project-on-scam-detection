from ml_model import ScamMLModel

ml_model = ScamMLModel()
ml_model.load()


def get_ml_score(text: str) -> int:
    """
    Convert ML probability into a 0–50 risk score.
    """
    probability = ml_model.predict_probability(text)
    return int(probability * 50)
