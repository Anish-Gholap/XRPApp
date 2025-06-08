import os
from typing import Dict, Optional, Tuple

import xrpl
from dotenv import load_dotenv
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import AccountInfo, AccountLines
from xrpl.models.transactions import AccountSet, Payment, TrustSet
from xrpl.wallet import Wallet

# Load environment variables
load_dotenv()

# Get wallet information from .env
ISSUER_ADDR = os.getenv("ISSUER_ADDR")
ISSUER_SEED = os.getenv("ISSUER_SEED")
LENDER_ADDR = os.getenv("LENDER_ADDR")
LENDER_SEED = os.getenv("LENDER_SEED")
BORROWER_ADDR = os.getenv("BORROWER_ADDR")
BORROWER_SEED = os.getenv("BORROWER_SEED")

# Connect to testnet with async client
client = AsyncJsonRpcClient("https://s.altnet.rippletest.net:51234")

# Create issuer wallet object
issuer_wallet = Wallet.from_seed(ISSUER_SEED) if ISSUER_SEED else None


async def get_xrp_balance(address: str) -> Optional[float]:
    """Get XRP balance for any address"""
    try:
        response = await client.request(
            AccountInfo(account=address, ledger_index="validated")
        )

        if response.is_successful():
            # XRP balance is stored in drops (1 XRP = 1,000,000 drops)
            drops = int(response.result["account_data"]["Balance"])
            xrp = drops / 1000000
            return xrp
        return None
    except Exception as e:
        print(f"Error getting XRP balance: {e}")
        return None


async def get_issued_currency_balance(
    address: str, currency_code: str = "SGD", issuer: str = ISSUER_ADDR
) -> float:
    """Get issued currency balance for any address"""
    try:
        response = await client.request(
            AccountLines(account=address, ledger_index="validated")
        )

        if response.is_successful() and "lines" in response.result:
            for line in response.result["lines"]:
                if line["currency"] == currency_code and line["account"] == issuer:
                    return float(line["balance"])
        return 0.0
    except Exception as e:
        print(f"Error getting {currency_code} balance: {e}")
        return 0.0


async def get_wallet_balances(address: str) -> Dict:
    """Get all balances for a wallet"""
    xrp = await get_xrp_balance(address)

    # Get issued currencies
    issued_currencies = {}
    try:
        response = await client.request(
            AccountLines(account=address, ledger_index="validated")
        )

        if response.is_successful() and "lines" in response.result:
            for line in response.result["lines"]:
                currency = line["currency"]
                issued_currencies[currency] = float(line["balance"])
    except Exception as e:
        print(f"Error getting issued currencies: {e}")

    return {"address": address, "xrp": xrp, "issued_currencies": issued_currencies}


async def setup_default_ripple() -> Tuple[bool, str]:
    """Configure issuer with DefaultRipple flag"""
    if not issuer_wallet:
        return False, "Issuer wallet not available"

    try:
        default_ripple_tx = AccountSet(
            account=ISSUER_ADDR,
            set_flag=xrpl.models.transactions.AccountSetAsfFlag.ASF_DEFAULT_RIPPLE,
        )
        dr_result = await submit_and_wait(default_ripple_tx, client, issuer_wallet)

        if dr_result.is_successful():
            return True, "DefaultRipple set successfully"
        else:
            return (
                False,
                f"DefaultRipple setting failed: {dr_result.result.get('engine_result_message', 'Unknown error')}",
            )
    except Exception as e:
        return False, f"Error setting DefaultRipple: {str(e)}"


async def create_trust_line(
    account_addr: str,
    account_seed: str,
    currency_code: str = "SGD",
    limit: str = "1000",
) -> Tuple[bool, str]:
    """Create trust line from account to issuer"""
    try:
        account_wallet = Wallet.from_seed(account_seed)
        trust_set = TrustSet(
            account=account_addr,
            limit_amount=IssuedCurrencyAmount(
                currency=currency_code, issuer=ISSUER_ADDR, value=limit
            ),
        )
        trust_result = await submit_and_wait(trust_set, client, account_wallet)

        if trust_result.is_successful():
            return True, f"Trust line created successfully for {account_addr}"
        else:
            return (
                False,
                f"Trust line failed: {trust_result.result.get('engine_result_message', 'Unknown error')}",
            )
    except Exception as e:
        return False, f"Error creating trust line: {str(e)}"


async def issue_currency(
    destination: str, amount: str, currency_code: str = "SGD"
) -> Tuple[bool, str]:
    """Issue currency from issuer to destination"""
    if not issuer_wallet:
        return False, "Issuer wallet not available"

    try:
        issue_payment = Payment(
            account=ISSUER_ADDR,
            destination=destination,
            amount=IssuedCurrencyAmount(
                currency=currency_code, issuer=ISSUER_ADDR, value=amount
            ),
        )
        issue_result = await submit_and_wait(issue_payment, client, issuer_wallet)

        if issue_result.is_successful():
            return (
                True,
                f"Successfully issued {amount} {currency_code} to {destination}",
            )
        else:
            return (
                False,
                f"Failed to issue currency: {issue_result.result.get('engine_result_message', 'Unknown error')}",
            )
    except Exception as e:
        return False, f"Error issuing currency: {str(e)}"


async def send_loan(
    lender_addr: str,
    lender_seed: str,
    borrower_addr: str,
    amount: str,
    currency_code: str = "SGD",
) -> Tuple[bool, str, Dict]:
    """Send loan from lender to borrower"""
    try:
        lender_wallet = Wallet.from_seed(lender_seed)
        loan_payment = Payment(
            account=lender_addr,
            destination=borrower_addr,
            amount=IssuedCurrencyAmount(
                currency=currency_code, issuer=ISSUER_ADDR, value=amount
            ),
            send_max=IssuedCurrencyAmount(
                currency=currency_code,
                issuer=ISSUER_ADDR,
                value=str(float(amount) * 1.05),  # 5% buffer
            ),
        )
        loan_result = await submit_and_wait(loan_payment, client, lender_wallet)

        if loan_result.is_successful():
            return (
                True,
                f"Loan of {amount} {currency_code} sent successfully to {borrower_addr}",
                {"hash": loan_result.result.get("hash", "unknown")},
            )
        else:
            return (
                False,
                f"Loan payment failed: {loan_result.result.get('engine_result_message', 'Unknown error')}",
                {},
            )
    except Exception as e:
        return False, f"Error sending loan: {str(e)}", {}


async def send_repayment(
    borrower_addr: str,
    borrower_seed: str,
    lender_addr: str,
    amount: str,
    currency_code: str = "SGD",
) -> Tuple[bool, str, Dict]:
    """Send repayment from borrower to lender"""
    try:
        borrower_wallet = Wallet.from_seed(borrower_seed)
        repayment = Payment(
            account=borrower_addr,
            destination=lender_addr,
            amount=IssuedCurrencyAmount(
                currency=currency_code, issuer=ISSUER_ADDR, value=amount
            ),
            send_max=IssuedCurrencyAmount(
                currency=currency_code,
                issuer=ISSUER_ADDR,
                value=str(float(amount) * 1.05),  # 5% buffer
            ),
        )
        repayment_result = await submit_and_wait(repayment, client, borrower_wallet)

        if repayment_result.is_successful():
            return (
                True,
                f"Repayment of {amount} {currency_code} sent successfully to {lender_addr}",
                {"hash": repayment_result.result.get("hash", "unknown")},
            )
        else:
            return (
                False,
                f"Repayment failed: {repayment_result.result.get('engine_result_message', 'Unknown error')}",
                {},
            )
    except Exception as e:
        return False, f"Error sending repayment: {str(e)}", {}
