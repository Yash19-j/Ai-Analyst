import numpy as np
import pandas as pd
from typing import Dict


class MonteCarloSimulation:
    """
    Monte Carlo Runway Simulation
    - Log-normal revenue growth
    - Normal expense growth
    - 5000 simulation runs
    """

    def __init__(
        self,
        df: pd.DataFrame,
        revenue_mean: float,
        revenue_vol: float,
        expense_mean: float,
        expense_vol: float,
        runs: int = 5000,
        max_months: int = 60
    ):
        self.df = df.copy()
        self.revenue_mean = revenue_mean
        self.revenue_vol = revenue_vol
        self.expense_mean = expense_mean
        self.expense_vol = expense_vol
        self.runs = runs
        self.max_months = max_months

        self.initial_cash = self.df["Cash"].iloc[-1]
        self.initial_revenue = self.df["Revenue"].iloc[-1]
        self.initial_expense = self.df["Expenses"].iloc[-1]

    def run_simulation(self) -> Dict[str, float]:

        survival_months = []

        for _ in range(self.runs):

            cash = self.initial_cash
            revenue = self.initial_revenue
            expense = self.initial_expense

            months_survived = 0

            for _ in range(self.max_months):

                # Log-normal revenue growth
                revenue_growth = np.random.normal(
                    self.revenue_mean,
                    self.revenue_vol
                )

                revenue = revenue * np.exp(
                    revenue_growth - 0.5 * self.revenue_vol**2
                )

                # Normal expense growth
                expense_growth = np.random.normal(
                    self.expense_mean,
                    self.expense_vol
                )

                expense = expense * (1 + expense_growth)

                net_burn = expense - revenue
                cash -= net_burn

                months_survived += 1

                if cash <= 0:
                    break

            survival_months.append(months_survived)

        survival_months = np.array(survival_months)

        return {
            "mean_survival_months": float(np.mean(survival_months)),
            "median_survival_months": float(np.median(survival_months)),
            "prob_survive_12m": float(
                np.mean(survival_months >= 12)
            ),
            "prob_survive_18m": float(
                np.mean(survival_months >= 18)
            ),
            "prob_survive_24m": float(
                np.mean(survival_months >= 24)
            )
        }
