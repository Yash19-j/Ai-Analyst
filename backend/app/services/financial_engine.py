import pandas as pd
import numpy as np
from typing import Dict


class FinancialEngine:
    """
    Core Financial Engine for startup financial analysis.

    Computes:
    - Average burn
    - Deterministic runway
    - Revenue CAGR
    - Revenue volatility
    - Expense volatility
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._validate_data()
        self._prepare_growth_columns()

    def _validate_data(self) -> None:
        required_columns = {"Revenue", "Expenses", "Cash"}

        if not required_columns.issubset(self.df.columns):
            raise ValueError(
                f"CSV must contain columns: {required_columns}"
            )

        if len(self.df) < 2:
            raise ValueError(
                "At least 2 months of financial data required."
            )

        # Ensure numeric
        self.df["Revenue"] = pd.to_numeric(self.df["Revenue"])
        self.df["Expenses"] = pd.to_numeric(self.df["Expenses"])
        self.df["Cash"] = pd.to_numeric(self.df["Cash"])

        # Sort chronologically if Month column exists
        if "Month" in self.df.columns:
            self.df = self.df.sort_values("Month")

    def _prepare_growth_columns(self) -> None:
        self.df["Revenue_Growth"] = self.df["Revenue"].pct_change()
        self.df["Expense_Growth"] = self.df["Expenses"].pct_change()

    def compute_basic_metrics(self) -> Dict[str, float]:
        avg_burn = (self.df["Expenses"] - self.df["Revenue"]).mean()
        current_cash = self.df["Cash"].iloc[-1]

        if avg_burn > 0:
            deterministic_runway = current_cash / avg_burn
        else:
            deterministic_runway = np.inf

        revenue_cagr = (
            (self.df["Revenue"].iloc[-1] /
             self.df["Revenue"].iloc[0]) **
            (1 / len(self.df)) - 1
        )

        revenue_volatility = self.df["Revenue_Growth"].std()
        expense_volatility = self.df["Expense_Growth"].std()

        return {
            "data_points": len(self.df),
            "average_burn": float(avg_burn),
            "current_cash": float(current_cash),
            "deterministic_runway_months": float(deterministic_runway),
            "revenue_cagr": float(revenue_cagr),
            "revenue_volatility": float(revenue_volatility),
            "expense_volatility": float(expense_volatility)
        }
