import pandas as pd
from typing import Dict

from .financial_engine import FinancialEngine
from .stability_metrics import StabilityMetrics
from .efficiency_metrics import EfficiencyMetrics
from .simulation import MonteCarloSimulation
from .risk_scoring import RiskScoringEngine


class AnalysisPipeline:
    """
    Orchestrates full financial analysis workflow.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        founder_equity: float = 60.0,
        simulation_runs: int = 5000
    ):
        self.df = df
        self.founder_equity = founder_equity
        self.simulation_runs = simulation_runs

    def run_full_analysis(self) -> Dict:

        # Step 1: Financial Metrics
        financial_engine = FinancialEngine(self.df)
        financial_metrics = financial_engine.compute_basic_metrics()

        # Step 2: Stability Metrics
        stability_engine = StabilityMetrics(financial_engine.df)
        stability_metrics = stability_engine.compute_stability_metrics()

        # Step 3: Efficiency Metrics
        efficiency_engine = EfficiencyMetrics(self.df)
        efficiency_metrics = efficiency_engine.compute_efficiency_metrics()

        # Step 4: Monte Carlo Simulation
        simulation_engine = MonteCarloSimulation(
            df=self.df,
            revenue_mean=stability_metrics["revenue_growth_mean"],
            revenue_vol=stability_metrics["revenue_volatility_adjusted"],
            expense_mean=stability_metrics["expense_growth_mean"],
            expense_vol=stability_metrics["expense_volatility_adjusted"],
            runs=self.simulation_runs
        )

        simulation_results = simulation_engine.run_simulation()

        # Step 5: Risk Scoring
        scoring_engine = RiskScoringEngine(
            financial_metrics = financial_metrics,
            stability_metrics=stability_metrics,
            efficiency_metrics=efficiency_metrics,
            founder_equity=self.founder_equity
        )

        risk_scores = scoring_engine.compute_final_score()

        # Combine everything
        return {
            "financial_metrics": financial_metrics,
            "stability_metrics": stability_metrics,
            "efficiency_metrics": efficiency_metrics,
            "simulation_results": simulation_results,
            "risk_scores": risk_scores
        }
