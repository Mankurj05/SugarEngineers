from demo_app.core.interest import calculate_emi

class EMIService:
    @staticmethod
    def compute_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
        """
        Compute EMI for given loan parameters.
        """
        return calculate_emi(principal, annual_rate, tenure_months)
