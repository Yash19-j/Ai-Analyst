import numpy as np
import pandas as pd
from typing import Dict


class StabilityMetrics:
    """
    Computes growth stability and volatility metrics.
    Includes volatility adjustment for small datasets.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._validate()

    def _validate(self):
        if "Revenue_Growth" not in self.df.columns or \
           "Expense_Growth" not in self.df.columns:
            raise ValueError(
                "Growth columns missing. Run FinancialEngine first."
            )

    def _adjust_volatility(self, volatility: float, n: int) -> float:
        """
        Apply shrinkage adjustment for small datasets.
        If data points < 6, reduce volatility inflation.
        """
        if n >= 6:
            return volatility
        elif 3 <= n < 6:
            return volatility * 0.85
        else:
            return volatility * 0.7

    def compute_stability_metrics(self) -> Dict[str, float]:
        revenue_growth = self.df["Revenue_Growth"].dropna()
        expense_growth = self.df["Expense_Growth"].dropna()

        n = len(revenue_growth)

        revenue_mean = revenue_growth.mean()
        expense_mean = expense_growth.mean()

        revenue_vol = revenue_growth.std()
        expense_vol = expense_growth.std()

        revenue_vol_adj = self._adjust_volatility(revenue_vol, n)
        expense_vol_adj = self._adjust_volatility(expense_vol, n)

        confidence_level = self._data_confidence(n)

        return {
            "revenue_growth_mean": float(revenue_mean),
            "expense_growth_mean": float(expense_mean),
            "revenue_volatility_raw": float(revenue_vol),
            "expense_volatility_raw": float(expense_vol),
            "revenue_volatility_adjusted": float(revenue_vol_adj),
            "expense_volatility_adjusted": float(expense_vol_adj),
            "data_points_used": n,
            "data_confidence": confidence_level
        }

    def _data_confidence(self, n: int) -> str:
        if n >= 9:
            return "HIGH"
        elif 5 <= n < 9:
            return "MEDIUM"
        else:
            return "LOW"
