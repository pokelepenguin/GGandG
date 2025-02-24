from credit_score import CreditTier
def calculate_interest_rate(company, loan_amount, term):
    base_rates = {
        CreditTier.S: 0.04,
        CreditTier.A: 0.06,
        CreditTier.B: 0.08,
        CreditTier.C: 0.10,
        CreditTier.D: 0.12
    }

    credit_score = company.credit_score
    base_rate = base_rates[credit_score]

    # Adjust interest rate based on loan amount
    max_loan_amount = company.get_max_loan_amount()
    amount_ratio = loan_amount / max_loan_amount
    interest_rate = base_rate + (amount_ratio * 0.10)  # 1% increase per 10% of max loan amount

    # Adjust interest rate based on loan term
    if term == 10:
        interest_rate += 0.005
    elif term == 25:
        interest_rate += 0.01

    return interest_rate
