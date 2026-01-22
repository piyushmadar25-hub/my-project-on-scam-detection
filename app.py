from flask import Flask, request, jsonify
from flask_cors import CORS
from risk_engine import ScamRiskEngine

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, origins=["http://localhost:5173"])

# Initialize risk engine once
risk_engine = ScamRiskEngine()


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for monitoring & demo confidence.
    """
    return jsonify({"status": "OK"}), 200


@app.route("/analyze", methods=["POST"])
def analyze_message():
    """
    Analyze input text and return scam risk assessment.
    """
    data = request.get_json()

    # Input validation
    if not data or "text" not in data:
        return jsonify({
            "error": "Invalid request. 'text' field is required."
        }), 400

    text = data["text"].strip()

    if not text:
        return jsonify({
            "error": "Text input cannot be empty."
        }), 400

    # Perform full scam risk analysis
    result = risk_engine.analyze(text)

    response = {
        "risk_score": result["final_score"],
        "risk_level": result["risk_level"],
        "explanations": result["explanations"]
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
