class RiskScoringEngine:
    """
    Computes weighted investment risk score.
    Outputs:
    - financial_health_score
    - growth_stability_score
    - capital_efficiency_score
    - governance_score
    - final_weighted_score
    - investment_decision
    """

    def __init__(
        self,
        financial_metrics: dict,
        stability_metrics: dict,
        efficiency_metrics: dict,
        founder_equity: float = 60.0
    ):
        self.financial = financial_metrics
        self.stability = stability_metrics
        self.efficiency = efficiency_metrics
        self.founder_equity = founder_equity

    def clamp(self, value, min_val=0, max_val=100):
        return max(min_val, min(value, max_val))

    def compute_financial_health_score(self):
        runway = self.financial.get("deterministic_runway_months", 0)
        burn = self.financial.get("average_burn", 0)

        score = 50

        # Runway evaluation
        if runway >= 24:
            score += 30
        elif runway >= 12:
            score += 15
        elif runway >= 6:
            score += 0
        else:
            score -= 25

        # Burn penalty
        if burn > 100000:
            score -= 20
        elif burn > 50000:
            score -= 10

        return self.clamp(score)

    def compute_growth_stability_score(self):
        revenue_growth = self.stability.get("revenue_growth_mean", 0)
        expense_growth = self.stability.get("expense_growth_mean", 0)
        revenue_vol = self.stability.get("revenue_volatility_adjusted", 0)

        score = 50

        # Growth quality spread
        growth_spread = revenue_growth - expense_growth

        if growth_spread > 0.10:
            score += 30
        elif growth_spread > 0:
            score += 15
        else:
            score -= 35  # strong penalty for negative spread

        # Volatility penalty
        if revenue_vol > 0.20:
            score -= 15
        elif revenue_vol > 0.10:
            score -= 5

        return self.clamp(score)

    def compute_capital_efficiency_score(self):
        burn_multiple = self.efficiency.get("burn_multiple", 0)
        revenue_expense_ratio = self.efficiency.get("revenue_expense_ratio", 0)

        score = 50

        # Burn multiple scoring
        if burn_multiple <= 1:
            score += 30
        elif burn_multiple <= 2:
            score += 15
        elif burn_multiple <= 5:
            score -= 10
        else:
            score -= 30

        # Revenue dominance
        if revenue_expense_ratio >= 1:
            score += 15
        elif revenue_expense_ratio < 0.5:
            score -= 15

        return self.clamp(score)

    def compute_governance_score(self):
        score = 50

        # Founder equity healthy range: 50–80%
        if 50 <= self.founder_equity <= 80:
            score += 30
        elif self.founder_equity < 30:
            score -= 20

        return self.clamp(score)

    def classify_investment(self, final_score):
        if final_score >= 75:
            return "INVEST"
        elif final_score >= 50:
            return "CAUTION"
        else:
            return "AVOID"

    def compute_final_score(self):

        financial_score = self.compute_financial_health_score()
        growth_score = self.compute_growth_stability_score()
        efficiency_score = self.compute_capital_efficiency_score()
        governance_score = self.compute_governance_score()

        # Weighted model
        final_score = (
            financial_score * 0.30 +
            growth_score * 0.30 +
            efficiency_score * 0.25 +
            governance_score * 0.15
        )

        final_score = round(self.clamp(final_score), 2)

        decision = self.classify_investment(final_score)

        return {
            "financial_health_score": financial_score,
            "growth_stability_score": growth_score,
            "capital_efficiency_score": efficiency_score,
            "governance_score": governance_score,
            "final_weighted_score": final_score,
            "investment_decision": decision
        }
