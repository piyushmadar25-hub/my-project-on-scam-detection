from typing import Dict, List
from rule_engine import ScamRuleEngine
from ml_predictor import get_ml_score


class ScamRiskEngine:
    """
    Combines rule-based detection and ML-based prediction
    to generate a final scam risk score and explanation.
    """

    def __init__(self):
        self.rule_engine = ScamRuleEngine()

    def analyze(self, text: str) -> Dict:
        """
        Perform full scam risk analysis.
        Returns final score, risk level, and explanations.
        """

        # 1️⃣ Rule-based analysis (0–50)
        rule_result = self.rule_engine.analyze(text)
        rule_score = rule_result["rule_score"]
        rule_reasons = rule_result["reasons"]

        # 2️⃣ ML-based analysis (0–50)
        ml_score = get_ml_score(text)

        # 3️⃣ Final score fusion
        final_score = min(rule_score + ml_score, 100)

        # 4️⃣ Risk level classification
        risk_level = self._classify_risk(final_score)

        # 5️⃣ Build explanation
        explanations = self._build_explanation(
            rule_reasons, ml_score
        )

        return {
            "final_score": final_score,
            "risk_level": risk_level,
            "explanations": explanations
        }

    @staticmethod
    def _classify_risk(score: int) -> str:
        if score >= 70:
            return "High"
        elif score >= 35:
            return "Medium"
        return "Low"

    @staticmethod
    def _build_explanation(
        rule_reasons: List[str], ml_score: int
    ) -> List[str]:
        explanations = []

        # Rule-based explanations
        explanations.extend(rule_reasons)

        # ML explanation (simple & jury-friendly)
        if ml_score >= 25:
            explanations.append(
                "Message pattern closely matches known scam messages"
            )
        elif ml_score >= 10:
            explanations.append(
                "Message shows partial similarity to scam patterns"
            )
        else:
            explanations.append(
                "Message does not strongly match known scam patterns"
            )

        return explanations
