class ReportGenerator:
    """
    Converts raw analysis output into structured
    investor-style financial narrative.
    """

    def __init__(self, results: dict):
        self.results = results

    def generate_summary(self):

        financial = self.results["financial_metrics"]
        stability = self.results["stability_metrics"]
        efficiency = self.results["efficiency_metrics"]
        simulation = self.results["simulation_results"]
        risk = self.results["risk_scores"]

        summary = []

        # ---- Financial Health ----
        runway = financial["deterministic_runway_months"]
        burn = financial["average_burn"]

        if runway < 6:
            summary.append(
                f"The company has critically low runway of {runway:.1f} months "
                f"with an average monthly burn of ₹ {burn:,.0f} , indicating urgent capital requirements."
            )
        elif runway < 12:
            summary.append(
                f"The company has moderate runway of {runway:.1f} months, "
                f"but burn levels remain elevated."
            )
        else:
            summary.append(
                f"The company demonstrates healthy runway of {runway:.1f} months "
                f"with controlled burn dynamics."
            )

        # ---- Growth Dynamics ----
        rev_growth = stability["revenue_growth_mean"]
        exp_growth = stability["expense_growth_mean"]
        spread = rev_growth - exp_growth

        if spread > 0:
            summary.append(
                f"Revenue growth ({rev_growth*100:.2f}%) exceeds expense growth "
                f"({exp_growth*100:.2f}%), reflecting improving operating leverage."
            )
        else:
            summary.append(
                f"Expense growth ({exp_growth*100:.2f}%) significantly outpaces "
                f"revenue growth ({rev_growth*100:.2f}%), indicating deteriorating unit economics."
            )

        # ---- Capital Efficiency ----
        burn_multiple = efficiency["burn_multiple"]

        if burn_multiple <= 2:
            summary.append(
                f"The burn multiple of {burn_multiple:.2f} suggests efficient capital deployment."
            )
        elif burn_multiple <= 5:
            summary.append(
                f"The burn multiple of {burn_multiple:.2f} indicates moderate inefficiency in capital usage."
            )
        else:
            summary.append(
                f"A burn multiple of {burn_multiple:.2f} signals severe capital inefficiency and scaling risk."
            )

        # ---- Survival Analysis ----
        survival_12m = simulation["prob_survive_12m"]

        if survival_12m > 0.75:
            summary.append(
                f"Monte Carlo simulations indicate strong resilience with "
                f"{survival_12m*100:.0f}% probability of surviving 12 months."
            )
        elif survival_12m > 0.40:
            summary.append(
                f"Survival probability of {survival_12m*100:.0f}% over 12 months "
                f"reflects moderate financial risk exposure."
            )
        else:
            summary.append(
                f"Simulation indicates critical risk with only "
                f"{survival_12m*100:.0f}% probability of 12-month survival."
            )

        # ---- Final Investment View ----
        final_score = risk["final_weighted_score"]
        decision = risk["investment_decision"]

        summary.append(
            f"Overall : \n Investment Health score: {final_score}/100 \n "
            f"Risk Level : {100 - final_score}/100 \n "
            f"Investment classification: {decision} ."
        )

        return "\n\n".join(summary)
