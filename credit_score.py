from enum import Enum


class CreditTier(Enum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


def calculate_credit_score(company):
    leverage_ratio = company.total_liabilities / company.total_assets if company.total_assets > 0 else float('inf')

    # Basic credit score calculation based on leverage ratio
    if leverage_ratio < 0.1:
        return CreditTier.S
    elif leverage_ratio < 0.3:
        return CreditTier.A
    elif leverage_ratio < 0.5:
        return CreditTier.B
    elif leverage_ratio < 0.7:
        return CreditTier.C
    else:
        return CreditTier.D
