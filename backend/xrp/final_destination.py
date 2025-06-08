import os
import time

import xrpl
from dotenv import load_dotenv
from xrpl.clients import JsonRpcClient
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.transactions import AccountSet, Payment, TrustSet
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet

# Load environment variables
load_dotenv()

# Connect to testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# Get wallet information from .env
issuer_addr = os.getenv("ISSUER_ADDR")
issuer_seed = os.getenv("ISSUER_SEED")
lender_addr = os.getenv("LENDER_ADDR")
lender_seed = os.getenv("LENDER_SEED")
borrower_addr = os.getenv("BORROWER_ADDR")
borrower_seed = os.getenv("BORROWER_SEED")

# Create wallet objects
issuer_wallet = Wallet.from_seed(issuer_seed)
lender_wallet = Wallet.from_seed(lender_seed)
borrower_wallet = Wallet.from_seed(borrower_seed)

# Currency details
CURRENCY_CODE = "SGD"
LOAN_AMOUNT = "50"
REPAYMENT_AMOUNT = "55"  # Loan + interest

print("=== XRP Ledger Loan System Setup ===")
print(f"Issuer: {issuer_addr}")
print(f"Lender: {lender_addr}")
print(f"Borrower: {borrower_addr}")
print(f"Currency: {CURRENCY_CODE}")
print("===================================")

# STEP 1: Configure Issuer with DefaultRipple flag
print("\n1. Setting DefaultRipple flag on issuer account...")
try:
    default_ripple_tx = AccountSet(
        account=issuer_addr,
        set_flag=xrpl.models.transactions.AccountSetAsfFlag.ASF_DEFAULT_RIPPLE,
    )
    dr_result = submit_and_wait(default_ripple_tx, client, issuer_wallet)

    if dr_result.is_successful():
        print("✅ DefaultRipple set successfully")
    else:
        print(
            f"❌ DefaultRipple setting failed: {dr_result.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error setting DefaultRipple: {e}")

time.sleep(2)  # Brief pause between transactions

# STEP 2: Create trust line from LENDER to issuer
print("\n2. Creating trust line from lender to issuer...")
try:
    lender_trust_set = TrustSet(
        account=lender_addr,
        limit_amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value="1000"
        ),
    )
    lender_trust_result = submit_and_wait(lender_trust_set, client, lender_wallet)

    if lender_trust_result.is_successful():
        print("✅ Lender trust line created successfully")
    else:
        print(
            f"❌ Lender trust line failed: {lender_trust_result.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error creating lender trust line: {e}")

time.sleep(2)  # Brief pause between transactions

# STEP 3: Create trust line from BORROWER to issuer
print("\n3. Creating trust line from borrower to issuer...")
try:
    borrower_trust_set = TrustSet(
        account=borrower_addr,
        limit_amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value="1000"
        ),
    )
    borrower_trust_result = submit_and_wait(borrower_trust_set, client, borrower_wallet)

    if borrower_trust_result.is_successful():
        print("✅ Borrower trust line created successfully")
    else:
        print(
            f"❌ Borrower trust line failed: {borrower_trust_result.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error creating borrower trust line: {e}")

time.sleep(2)  # Brief pause between transactions

# STEP 4A: Issue currency to lender (issuer → lender)
print("\n4a. Issuing SGD from issuer to lender...")
try:
    issue_payment_lender = Payment(
        account=issuer_addr,
        destination=lender_addr,
        amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value="100"
        ),
    )
    issue_result_lender = submit_and_wait(issue_payment_lender, client, issuer_wallet)

    if issue_result_lender.is_successful():
        print(f"✅ Successfully issued 100 {CURRENCY_CODE} to lender")
    else:
        print(
            f"❌ Failed to issue currency to lender: {issue_result_lender.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error issuing currency to lender: {e}")

time.sleep(2)  # Brief pause between transactions

# STEP 4B: Issue currency to borrower (issuer → borrower)
print("\n4b. Issuing SGD from issuer to borrower...")
try:
    issue_payment_borrower = Payment(
        account=issuer_addr,
        destination=borrower_addr,
        amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value="100"
        ),
    )
    issue_result_borrower = submit_and_wait(
        issue_payment_borrower, client, issuer_wallet
    )

    if issue_result_borrower.is_successful():
        print(f"✅ Successfully issued 100 {CURRENCY_CODE} to borrower")
    else:
        print(
            f"❌ Failed to issue currency to borrower: {issue_result_borrower.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error issuing currency to borrower: {e}")

time.sleep(2)  # Brief pause between transactions

# Print balances after initial funding
print("\n5. Checking balances after initial funding...")


def get_balance(wallet, currency_code, issuer):
    """Get the balance of a specific currency for a wallet"""
    from xrpl.models.requests import AccountLines

    account_lines = AccountLines(
        account=wallet.classic_address, ledger_index="validated"
    )
    response = client.request(account_lines)

    if response.is_successful() and "lines" in response.result:
        for line in response.result["lines"]:
            if line["currency"] == currency_code and line["account"] == issuer:
                return line["balance"]
    return "0"


# Get initial balances
lender_initial = get_balance(lender_wallet, CURRENCY_CODE, issuer_addr)
borrower_initial = get_balance(borrower_wallet, CURRENCY_CODE, issuer_addr)

print(f"Lender initial balance: {lender_initial} {CURRENCY_CODE}")
print(f"Borrower initial balance: {borrower_initial} {CURRENCY_CODE}")

# STEP 6: Loan from lender to borrower
print(f"\n6. Sending loan of {LOAN_AMOUNT} {CURRENCY_CODE} from lender to borrower...")
try:
    loan_payment = Payment(
        account=lender_addr,
        destination=borrower_addr,
        amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value=LOAN_AMOUNT
        ),
        send_max=IssuedCurrencyAmount(
            currency=CURRENCY_CODE,
            issuer=issuer_addr,
            value=str(float(LOAN_AMOUNT) * 1.05),  # 5% buffer
        ),
    )
    loan_result = submit_and_wait(loan_payment, client, lender_wallet)

    if loan_result.is_successful():
        print(f"✅ Loan of {LOAN_AMOUNT} {CURRENCY_CODE} sent successfully to borrower")
        print(f"   Transaction hash: {loan_result.result.get('hash', 'unknown')}")
    else:
        print(
            f"❌ Loan payment failed: {loan_result.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error sending loan: {e}")

time.sleep(2)  # Brief pause between transactions

# Check middle balances
mid_lender = get_balance(lender_wallet, CURRENCY_CODE, issuer_addr)
mid_borrower = get_balance(borrower_wallet, CURRENCY_CODE, issuer_addr)
print(f"\nLender balance after loan: {mid_lender} {CURRENCY_CODE}")
print(f"Borrower balance after loan: {mid_borrower} {CURRENCY_CODE}")

# STEP 7: Repayment from borrower to lender
print(
    f"\n7. Sending repayment of {REPAYMENT_AMOUNT} {CURRENCY_CODE} from borrower to lender..."
)
try:
    repayment = Payment(
        account=borrower_addr,
        destination=lender_addr,
        amount=IssuedCurrencyAmount(
            currency=CURRENCY_CODE, issuer=issuer_addr, value=REPAYMENT_AMOUNT
        ),
        send_max=IssuedCurrencyAmount(
            currency=CURRENCY_CODE,
            issuer=issuer_addr,
            value=str(float(REPAYMENT_AMOUNT) * 1.05),  # 5% buffer
        ),
    )
    repayment_result = submit_and_wait(repayment, client, borrower_wallet)

    if repayment_result.is_successful():
        print(
            f"✅ Repayment of {REPAYMENT_AMOUNT} {CURRENCY_CODE} sent successfully to lender"
        )
        print(f"   Transaction hash: {repayment_result.result.get('hash', 'unknown')}")
    else:
        print(
            f"❌ Repayment failed: {repayment_result.result.get('engine_result_message', 'Unknown error')}"
        )
except Exception as e:
    print(f"❌ Error sending repayment: {e}")

time.sleep(2)  # Brief pause between transactions

# STEP 8: Check final balances
print("\n8. Checking final balances...")

# Get balances
lender_balance = get_balance(lender_wallet, CURRENCY_CODE, issuer_addr)
borrower_balance = get_balance(borrower_wallet, CURRENCY_CODE, issuer_addr)

print(f"Lender final balance: {lender_balance} {CURRENCY_CODE}")
print(f"Borrower final balance: {borrower_balance} {CURRENCY_CODE}")

# Calculate and display changes
lender_change = float(lender_balance) - float(lender_initial)
borrower_change = float(borrower_balance) - float(borrower_initial)
print(f"\nLender net change: {lender_change:+.2f} {CURRENCY_CODE}")
print(f"Borrower net change: {borrower_change:+.2f} {CURRENCY_CODE}")

print("\n=== Loan System Setup Complete ===")
print("The loan system is now fully configured.")
print("• Issuer account is set up with DefaultRipple")
print("• Both lender and borrower have trust lines to the issuer")
print("• Lender and borrower were both initially funded with SGD")
print("• A sample loan and repayment have been executed")
print("===================================")
