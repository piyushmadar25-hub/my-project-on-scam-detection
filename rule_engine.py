import re
from typing import List, Dict


class ScamRuleEngine:
    """
    Rule-based engine to detect scam indicators in text content.
    """

    def __init__(self):
        self.urgency_keywords = [
            "urgent", "immediately", "act now", "last chance",
            "limited time", "verify now"
        ]

        self.payment_keywords = [
            "upi", "processing fee", "gift card",
            "crypto", "bitcoin", "pay now"
        ]

        self.sensitive_keywords = [
            "otp", "pin", "password", "cvv",
            "aadhaar", "pan", "account number"
        ]

        self.guarantee_keywords = [
            "100% guaranteed", "no risk",
            "instant approval", "guaranteed income"
        ]

        self.impersonation_keywords = [
            "bank", "government", "income tax",
            "customs", "police", "official notice"
        ]

    def analyze(self, text: str) -> Dict:
        text = text.lower()
        score = 0
        reasons = []

        if self._match(text, self.urgency_keywords):
            score += 15
            reasons.append("Uses urgent or pressuring language")

        if self._match(text, self.payment_keywords):
            score += 20
            reasons.append("Requests immediate payment")

        if self._match(text, self.sensitive_keywords):
            score += 25
            reasons.append("Asks for sensitive personal information")

        if self._match(text, self.guarantee_keywords):
            score += 10
            reasons.append("Makes unrealistic guaranteed claims")

        if self._match(text, self.impersonation_keywords):
            score += 15
            reasons.append("Impersonates a trusted authority")

        if self._has_suspicious_link(text):
            score += 15
            reasons.append("Contains suspicious or shortened URLs")

        return {
            "rule_score": min(score, 50),
            "reasons": reasons
        }

    @staticmethod
    def _match(text: str, keywords: List[str]) -> bool:
        return any(word in text for word in keywords)

    @staticmethod
    def _has_suspicious_link(text: str) -> bool:
        return bool(re.search(r"(bit\.ly|tinyurl|t\.co|http://)", text))
