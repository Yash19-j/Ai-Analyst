import pandas as pd
import numpy as np
from typing import Dict


class EfficiencyMetrics:
    """
    Computes capital efficiency metrics.

    Metrics:
    - Net burn
    - Net new revenue
    - Burn multiple
    - Revenue-to-expense ratio
    - Capital efficiency ratio
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._validate()

    def _validate(self):
        required_columns = {"Revenue", "Expenses"}
        if not required_columns.issubset(self.df.columns):
            raise ValueError(
                f"Missing required columns: {required_columns}"
            )

        if len(self.df) < 2:
            raise ValueError(
                "At least 2 months of data required."
            )

    def compute_efficiency_metrics(self) -> Dict[str, float]:
        revenue = self.df["Revenue"]
        expenses = self.df["Expenses"]

        net_burn_series = expenses - revenue
        avg_net_burn = net_burn_series.mean()

        net_new_revenue = revenue.iloc[-1] - revenue.iloc[0]

        # Burn Multiple
        if net_new_revenue > 0:
            burn_multiple = avg_net_burn / net_new_revenue
        else:
            burn_multiple = np.inf

        # Revenue to Expense Ratio
        revenue_expense_ratio = (
            revenue.iloc[-1] / expenses.iloc[-1]
            if expenses.iloc[-1] > 0 else np.inf
        )

        # Capital Efficiency Ratio
        # Revenue generated per unit burn
        if avg_net_burn > 0:
            capital_efficiency_ratio = net_new_revenue / avg_net_burn
        else:
            capital_efficiency_ratio = np.inf

        return {
            "average_net_burn": float(avg_net_burn),
            "net_new_revenue": float(net_new_revenue),
            "burn_multiple": float(burn_multiple),
            "revenue_expense_ratio": float(revenue_expense_ratio),
            "capital_efficiency_ratio": float(capital_efficiency_ratio)
        }
