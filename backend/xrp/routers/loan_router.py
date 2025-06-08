from typing import Dict, List

from fastapi import APIRouter

from ..models.loan import ApiResponse, LoanRequest, RepaymentRequest, WalletBalance
from ..services.xrpl_service import (
    BORROWER_ADDR,
    ISSUER_ADDR,
    LENDER_ADDR,
    create_trust_line,
    get_issued_currency_balance,
    get_wallet_balances,
    issue_currency,
    send_loan,
    send_repayment,
    setup_default_ripple,
)

loan_router = APIRouter()


@loan_router.post("/fund-loan", response_model=ApiResponse)
async def fund_loan(loan_req: LoanRequest):
    """
    Fund a loan from lender to borrower.
    This sets up all necessary components including:
    - DefaultRipple on issuer
    - Trust lines for lender and borrower
    - The actual loan payment
    """
    # 1. Set up DefaultRipple on issuer (if not done already)
    success, message = await setup_default_ripple()
    if not success:
        return ApiResponse(
            success=False, message="Failed to set up issuer", error=message
        )

    # 2. Create trust line for lender
    success, message = await create_trust_line(
        loan_req.lender_address, loan_req.lender_seed, loan_req.currency_code
    )
    if not success:
        return ApiResponse(
            success=False, message="Failed to create lender trust line", error=message
        )

    # 3. Create trust line for borrower (borrower seed would be needed in a real implementation)
    # Using a sample borrower seed or getting it from somewhere else would be required
    # For now, we'll assume the borrower trust line is already established

    # 4. Issue currency to lender if needed (optional)
    lender_balance = await get_issued_currency_balance(
        loan_req.lender_address, loan_req.currency_code
    )
    loan_amount = float(loan_req.amount)

    if lender_balance < loan_amount:
        # Lender needs more funds
        amount_needed = str(loan_amount - lender_balance + 10)  # Add a buffer
        success, message = await issue_currency(
            loan_req.lender_address, amount_needed, loan_req.currency_code
        )
        if not success:
            return ApiResponse(
                success=False,
                message="Failed to issue currency to lender",
                error=message,
            )

    # 5. Send the loan
    success, message, data = await send_loan(
        loan_req.lender_address,
        loan_req.lender_seed,
        loan_req.borrower_address,
        loan_req.amount,
        loan_req.currency_code,
    )

    if not success:
        return ApiResponse(success=False, message="Failed to send loan", error=message)

    # 6. Get updated balances
    lender_balance_after = await get_issued_currency_balance(
        loan_req.lender_address, loan_req.currency_code
    )
    borrower_balance_after = await get_issued_currency_balance(
        loan_req.borrower_address, loan_req.currency_code
    )

    response_data = {
        "transaction_hash": data.get("hash", "unknown"),
        "lender_balance": lender_balance_after,
        "borrower_balance": borrower_balance_after,
        "currency": loan_req.currency_code,
    }

    return ApiResponse(
        success=True,
        message=f"Successfully sent {loan_req.amount} {loan_req.currency_code} from lender to borrower",
        data=response_data,
    )


@loan_router.post("/repay-loan", response_model=ApiResponse)
async def repay_loan(repayment_req: RepaymentRequest):
    """Send a repayment from borrower to lender"""
    # Send the repayment
    success, message, data = await send_repayment(
        repayment_req.borrower_address,
        repayment_req.borrower_seed,
        repayment_req.lender_address,
        repayment_req.amount,
        repayment_req.currency_code,
    )

    if not success:
        return ApiResponse(
            success=False, message="Failed to send repayment", error=message
        )

    # Get updated balances
    lender_balance_after = await get_issued_currency_balance(
        repayment_req.lender_address, repayment_req.currency_code
    )
    borrower_balance_after = await get_issued_currency_balance(
        repayment_req.borrower_address, repayment_req.currency_code
    )

    response_data = {
        "transaction_hash": data.get("hash", "unknown"),
        "lender_balance": lender_balance_after,
        "borrower_balance": borrower_balance_after,
        "currency": repayment_req.currency_code,
    }

    return ApiResponse(
        success=True,
        message=f"Successfully sent {repayment_req.amount} {repayment_req.currency_code} from borrower to lender",
        data=response_data,
    )


@loan_router.get("/balance/{address}", response_model=WalletBalance)
async def get_balance(address: str):
    """Get balances for a specific wallet address"""
    balances = await get_wallet_balances(address)
    return WalletBalance(**balances)


@loan_router.get("/balances/issuer", response_model=WalletBalance)
async def get_issuer_balance():
    """Get balances for the issuer wallet"""
    balances = await get_wallet_balances(ISSUER_ADDR)
    return WalletBalance(**balances)


@loan_router.get("/balances/lender", response_model=WalletBalance)
async def get_lender_balance():
    """Get balances for the lender wallet"""
    balances = await get_wallet_balances(LENDER_ADDR)
    return WalletBalance(**balances)


@loan_router.get("/balances/borrower", response_model=WalletBalance)
async def get_borrower_balance():
    """Get balances for the borrower wallet"""
    balances = await get_wallet_balances(BORROWER_ADDR)
    return WalletBalance(**balances)


@loan_router.post("/all-balances", response_model=Dict[str, WalletBalance])
async def get_all_balances(addresses: List[str]):
    """Get balances for multiple wallet addresses"""
    results = {}
    for address in addresses:
        balances = await get_wallet_balances(address)
        results[address] = WalletBalance(**balances)
    return results
