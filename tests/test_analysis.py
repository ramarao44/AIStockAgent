import sys
import unittest
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOT = PROJECT_ROOT / "Python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from analysis.techincal_analysis import TechnicalAnalysis
from analysis.fundamental_analysis import FundamentalAnalysis
from analysis.decision_engine import DecisionEngine


class AnalysisTests(unittest.TestCase):
    def test_fundamental_score_handles_empty_data(self):
        analysis = FundamentalAnalysis()
        self.assertEqual(analysis.score_basic({}), 0)

    def test_fundamental_score_rewards_stronger_stocks(self):
        analysis = FundamentalAnalysis()
        score = analysis.score_basic({"latest_close": 150, "latest_volume": 2_000_000})
        self.assertGreater(score, 0)

    def test_technical_analysis_detects_bullish_trend(self):
        analysis = TechnicalAnalysis()
        data = pd.DataFrame({"Close": [100, 102, 104, 106, 108]})
        sma = analysis.simple_moving_average(data, window=3)
        signal = analysis.get_trend_signal(data)

        self.assertEqual(sma.iloc[-1], 106.0)
        self.assertEqual(signal["trend"], "bullish")

    def test_decision_engine_returns_structured_recommendation(self):
        engine = DecisionEngine()
        result = engine.generate_decision(
            technical={"trend": "bullish", "momentum": 0.03},
            fundamental={"score": 4},
            risk={"risk_level": "low"},
        )

        self.assertEqual(result["decision"], "BUY")
        self.assertIn("confidence", result)
        self.assertIn("reasoning", result)


if __name__ == "__main__":
    unittest.main()
