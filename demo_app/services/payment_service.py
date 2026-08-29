from demo_app.core.interest import get_monthly_rate, calculate_emi
from demo_app.services.loan_service import LoanService

class PaymentService:
    def __init__(self, loan_service: LoanService = None):
        self.loan_service = loan_service or LoanService()

    def calculate_balance(self, loan_id: str, payments_made: int) -> dict:
        """
        Calculate remaining balance after a given number of monthly payments.
        This is a read-only calculation, not actually saving the payments.
        """
        loan = self.loan_service.get_loan(loan_id)
        if not loan:
            return None
            
        principal = loan["principal"]
        annual_rate = loan["rate"]
        tenure_months = loan["tenure_months"]
        
        if payments_made < 0:
            payments_made = 0
        if payments_made > tenure_months:
            payments_made = tenure_months
            
        emi = calculate_emi(principal, annual_rate, tenure_months)
        monthly_rate = get_monthly_rate(annual_rate)
        
        balance = principal
        total_paid = 0.0
        
        # Calculate amortization schedule up to the payments_made point
        for _ in range(payments_made):
            interest_payment = balance * monthly_rate
            principal_payment = emi - interest_payment
            balance -= principal_payment
            total_paid += emi
            
            if balance < 0:
                balance = 0
                
        return {
            "loan_id": loan_id,
            "principal": principal,
            "payments_made": payments_made,
            "total_installments": tenure_months,
            "emi": emi,
            "total_paid": round(total_paid, 2),
            "remaining_balance": round(balance, 2)
        }
