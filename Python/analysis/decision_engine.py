"""
Decision engine for final BUY/SELL/HOLD recommendations.

This module is the decision layer from the high-level design. It combines the
signals from the technical and fundamental modules into a simple, explainable
recommendation.
"""


class DecisionEngine:
    def generate_decision(self, technical: dict, fundamental: dict, risk: dict):
        """Create a simple recommendation with confidence and reasoning."""
        score = 0
        reasoning = []

        trend = technical.get("trend", "neutral")
        momentum = float(technical.get("momentum", 0.0) or 0.0)
        fundamental_score = int(fundamental.get("score", 0) or 0)
        risk_level = risk.get("risk_level", "medium")

        # Favor bullish behavior and penalize bearish conditions.
        if trend == "bullish":
            score += 2
            reasoning.append("Bullish short-term trend")
        elif trend == "bearish":
            score -= 2
            reasoning.append("Bearish short-term trend")
        else:
            reasoning.append("Mixed trend signal")

        if momentum > 0.01:
            score += 1
            reasoning.append("Positive momentum")
        elif momentum < -0.01:
            score -= 1
            reasoning.append("Negative momentum")

        if fundamental_score >= 3:
            score += 1
            reasoning.append("Solid fundamental support")
        elif fundamental_score <= 1:
            score -= 1
            reasoning.append("Weak fundamental support")

        if risk_level == "low":
            score += 1
            reasoning.append("Low risk environment")
        elif risk_level == "high":
            score -= 1
            reasoning.append("High risk environment")

        if score >= 3:
            decision = "BUY"
        elif score <= 1:
            decision = "SELL"
        else:
            decision = "HOLD"

        confidence = min(0.95, max(0.55, 0.6 + 0.05 * abs(score)))

        return {
            "decision": decision,
            "confidence": round(confidence, 2),
            "time_horizon": "short_term",
            "reasoning": reasoning,
        }
