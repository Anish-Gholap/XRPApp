from app.services.wallet import TurnkeyService,WalletService
import dotenv
import os
import pytest

dotenv.load_dotenv()

turnkey_api_key = os.getenv("TURNKEY_PRIVATE_KEY")
turnkey_name = os.getenv("TURNKEY_PUBLIC_KEY")
turnkey_url = os.getenv("TURNKEY_URL")
turnkey_organization = os.getenv("TURNKEY_ORGANIZATION_ID")
testnet = os.getenv("RIPPLE_TESTNET_URL")




# @pytest.mark.anyio
# def test_create_account():
#     result = TurnkeyService(url=turnkey_url,api_public_key=turnkey_name,api_private_key=turnkey_api_key,organization_id=turnkey_organization,ripple_url=testnet).create_account("recieving") 

#     assert result == "fail"

def test_sign_transaction():
    transaction = {
        "TransactionType": "Payment",
        "Account": "rayJTJWwHVo6aGKusiebLr6ozQeZemTxPe",
        "Amount": "2000000",
        "Destination": "rNa2Hz5dTwuXofTfL8weNrwzTahLfF53he",
        "Fee": "12",  # Required
    }
    signed_transaction = TurnkeyService(url=turnkey_url,api_public_key=turnkey_name,api_private_key=turnkey_api_key,organization_id=turnkey_organization,ripple_url=testnet).sign_transaction(transaction,"sending")
    
    assert signed_transaction == "fail"





