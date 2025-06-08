import os

from dotenv import load_dotenv
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo, AccountLines

# Load environment variables
load_dotenv()

# Get wallet information from .env
ISSUER_ADDR = os.getenv("ISSUER_ADDR")
ISSUER_SEED = os.getenv("ISSUER_SEED")
LENDER_ADDR = os.getenv("LENDER_ADDR")
LENDER_SEED = os.getenv("LENDER_SEED")
BORROWER_ADDR = os.getenv("BORROWER_ADDR")
BORROWER_SEED = os.getenv("BORROWER_SEED")

# Connect to testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")


def get_xrp_balance(address):
    """Get XRP balance for any address"""
    try:
        response = client.request(
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


def get_issued_currency_balance(address, currency_code="SGD", issuer=ISSUER_ADDR):
    """Get issued currency balance for any address"""
    try:
        response = client.request(
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


# Convenience functions for specific wallets


def get_issuer_balances():
    """Get all balances for issuer wallet"""
    xrp = get_xrp_balance(ISSUER_ADDR)
    return {
        "address": ISSUER_ADDR,
        "xrp": xrp,
        # Issuer doesn't hold its own currency
    }


def get_lender_balances():
    """Get all balances for lender wallet"""
    xrp = get_xrp_balance(LENDER_ADDR)
    sgd = get_issued_currency_balance(LENDER_ADDR)
    return {"address": LENDER_ADDR, "xrp": xrp, "SGD": sgd}


def get_borrower_balances():
    """Get all balances for borrower wallet"""
    xrp = get_xrp_balance(BORROWER_ADDR)
    sgd = get_issued_currency_balance(BORROWER_ADDR)
    return {"address": BORROWER_ADDR, "xrp": xrp, "SGD": sgd}


def print_all_balances():
    """Print balances for all wallets"""
    issuer = get_issuer_balances()
    lender = get_lender_balances()
    borrower = get_borrower_balances()

    print("\n=== Wallet Balances ===")
    print(f"Issuer ({ISSUER_ADDR[:8]}...):")
    print(f"  XRP: {issuer['xrp']}")

    print(f"\nLender ({LENDER_ADDR[:8]}...):")
    print(f"  XRP: {lender['xrp']}")
    print(f"  SGD: {lender['SGD']}")

    print(f"\nBorrower ({BORROWER_ADDR[:8]}...):")
    print(f"  XRP: {borrower['xrp']}")
    print(f"  SGD: {borrower['SGD']}")
    print("======================")


# Example usage
if __name__ == "__main__":
    print_all_balances()
