import { useState, useEffect } from "react";
import "./App.css";

function RiskMeter({ score, level }) {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;

  return (
    <div className="meter">
      <svg width="150" height="150">
        <circle
          cx="75"
          cy="75"
          r={radius}
          stroke="#e5e7eb"
          strokeWidth="10"
          fill="none"
        />
        <circle
          cx="75"
          cy="75"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeWidth="10"
          fill="none"
          className={`progress ${level.toLowerCase()}`}
        />
      </svg>
      <div className="meter-text">
        <strong>{score}</strong>
        <span>/100</span>
      </div>
    </div>
  );
}

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [animatedScore, setAnimatedScore] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!result?.risk_score) return;

    let start = 0;
    const end = result.risk_score;
    const step = () => {
      start += 1;
      setAnimatedScore(start);
      if (start < end) requestAnimationFrame(step);
    };
    step();
  }, [result]);

  const analyzeMessage = async () => {
    if (!text.trim()) {
      alert("Please enter a message");
      return;
    }

    setLoading(true);
    setResult(null);
    setAnimatedScore(0);

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setResult(data);
    } catch {
      alert("Backend not running");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="card">
        <h1>TrustGuard AI</h1>
        <p className="subtitle">Real-time, explainable scam detection</p>

        <textarea
          placeholder="Paste a message to check for scam risk..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={analyzeMessage} disabled={loading}>
          {loading ? "Analyzing..." : "Check Scam Risk"}
        </button>

        {result && (
          <div className="result">
            <RiskMeter
              score={animatedScore}
              level={result.risk_level}
            />

            <div className={`badge ${result.risk_level.toLowerCase()}`}>
              {result.risk_level} Risk
            </div>

            {Array.isArray(result.explanations) && (
              <ul>
                {result.explanations.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
