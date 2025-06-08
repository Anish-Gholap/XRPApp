from typing import Dict, Optional

from pydantic import BaseModel


class LoanRequest(BaseModel):
    lender_address: str
    lender_seed: str
    borrower_address: str
    amount: str
    currency_code: str = "SGD"


class RepaymentRequest(BaseModel):
    borrower_address: str
    borrower_seed: str
    lender_address: str
    amount: str
    currency_code: str = "SGD"


class WalletBalance(BaseModel):
    address: str
    xrp: Optional[float] = None
    issued_currencies: Optional[Dict[str, float]] = None


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None
    error: Optional[str] = None
