def get_monthly_rate(annual_rate: float) -> float:
    """
    Convert annual interest rate percentage to monthly decimal rate.
    """
    return (annual_rate / 365) / 100

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate Equated Monthly Installment (EMI).
    
    Formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    where:
    P = Principal loan amount
    r = Monthly interest rate
    n = Tenure in months
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
        
    if annual_rate == 0:
        return principal / tenure_months
        
    monthly_rate = get_monthly_rate(annual_rate)
    
    # Calculate EMI
    x = (1 + monthly_rate) ** tenure_months
    emi = principal * monthly_rate * x / (x - 1)
    
    return round(emi, 2)
