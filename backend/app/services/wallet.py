import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from base64 import urlsafe_b64encode
from fastapi import HTTPException
from abc import ABC, abstractmethod
import httpx
import time
import requests
import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.core.binarycodec import encode, decode
from xrpl.models import Payment


class WalletService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_account(self,username: str) -> str:
        pass

    @abstractmethod
    def sign_transaction(self, transaction: dict) -> str:
        pass


class TurnkeyService(WalletService):
    def __init__(self,url:str,api_public_key :str, api_private_key: str,organization_id:str, ripple_url:str):
        self.url = url
        self.organization_id = organization_id
        self.private_key = ec.derive_private_key(int(api_private_key, 16), ec.SECP256R1())
        self.public_key = api_public_key
        self.client = JsonRpcClient(ripple_url)

    def _stamp(self,payload : dict) -> dict:
        payload_str = json.dumps(payload)
        signature = self.private_key.sign(payload_str.encode(), ec.ECDSA(hashes.SHA256()))

        stamp = {
            "publicKey": self.public_key,
            "scheme": "SIGNATURE_SCHEME_TK_API_P256",
            "signature": signature.hex(),
        }
        encoded_stamp = urlsafe_b64encode(json.dumps(stamp).encode()).decode().rstrip("=")
        return encoded_stamp


    def _create_suborg(self, username: str) -> str:

       
        data = {
            "type": "ACTIVITY_TYPE_CREATE_SUB_ORGANIZATION_V4",
            "timestampMs": str(int(time.time() * 1000)),
            "organizationId": self.organization_id,
            "parameters": {
            "subOrganizationName": f"{username}-sub-org",
            "rootUsers": [
                {
                "userName": username,
                "userEmail": "",
                "authenticators": [],
                "apiKeys": [
                    {
                    "apiKeyName": "organization-api-key",
                    "publicKey": self.public_key
                    }
                ]
                }
            ],
            "rootQuorumThreshold": 1,
            "wallet": {
                "walletName": f"{username}-xrp-wallet",
                "accounts": [
                {
                    "curve": "CURVE_SECP256K1",
                    "pathFormat": "PATH_FORMAT_BIP32",
                    "path": "m/44'/144'/0'/0/0",
                    "addressFormat": "ADDRESS_FORMAT_XRP"
                }
                ]
            }
            }
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Stamp": self._stamp(data)
        }

        # async with httpx.AsyncClient() as client:
        #     response = await client.post(f"{self.url}/submit/create_sub_organization", headers=headers, json=data)
        #     if response.status_code != 200:
        #         print(response.text)
        #         raise HTTPException(status_code=500,detail="unable to create wallet")
        #     data = response.json()
        #     return data["activity"]["result"]["result"]["createSubOrganizationResultV7"]["wallet"]["addresses"]
        
        response = requests.post(f"{self.url}/submit/create_sub_organization", headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=500,detail="unable to create wallet")
        data = response.json()
        return data
    
    def _get_suborg(self, username: str) -> str | None:
        data = {
            "organizationId": self.organization_id,
            "filterType": "NAME",
            "filterValue": f"{username}-sub-org",
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Stamp': self._stamp(data),
        }

        resp = requests.post(f"{self.url}/query/list_suborgs", headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["organizationIds"]
        else:
            print(resp.text)
            raise HTTPException(status_code=404,detail="bad request params")
        
    def _whoami(self):
        payload = {
            "organizationId": self.organization_id
        }

        headers = {
            'Content-Type': 'application/json',
            'X-Stamp': self._stamp(payload),
        }

        
        resp = requests.post(f"{self.url}/query/whoami", headers=headers, json=payload)
        return resp.json()

    def _sign_raw_payload(self, sign_with: str, payload: str, sub_org:str) -> dict:
        data = {
            "type": "ACTIVITY_TYPE_SIGN_RAW_PAYLOAD_V2",
            "timestampMs": str(int(time.time() * 1000)),
            "organizationId": sub_org,
            "parameters": {
                "signWith": sign_with,
                "payload": encode(payload),
                "encoding": "PAYLOAD_ENCODING_HEXADECIMAL",
                "hashFunction": "HASH_FUNCTION_SHA256",
            }
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Stamp": self._stamp(data)
        }

        response = requests.post(f"{self.url}/submit/sign_raw_payload", headers=headers, json=data)
        if response.status_code != 200:
            print(response.text)
            raise HTTPException(status_code=500, detail="unable to sign payload")
        result = response.json()["activity"]["result"]["signRawPayloadResult"]
        r = result.get("r")
        s = result.get("s") 
        v = result.get("v")

        r_clean = r.replace('0x', '').zfill(64)
        s_clean = s.replace('0x', '').zfill(64) 
        if not all([r, s, v]):
            raise ValueError("Missing signature components in response")

        r_clean = r.replace('0x', '').zfill(64)
        s_clean = s.replace('0x', '').zfill(64)
        
        signature = r_clean + s_clean
        
        signature.upper()
                

    def create_account(self,username:str) -> str:
        result = self._get_suborg(username)
        print(result)
        if len(result) == 0:
            return self._create_suborg(username)
        else:
            return result

    
    def sign_transaction(self,address: dict,transaction:str) -> bool:
        signature = self._sign_raw_payload(address,transaction)
        signed_transaction = {
            **transaction,
            "TxnSignature": signature,
        }
        response = self.client.request(xrpl.models.requests.SubmitOnly(tx_blob=encode(signed_transaction)))
        return response