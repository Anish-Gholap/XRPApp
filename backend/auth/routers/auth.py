import secrets
import json
import base64
from fastapi import HTTPException, APIRouter
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.core.keypairs import is_valid_message
from xrpl.models.requests import AccountObjects

from db.db import supabase_client
from auth.xrpl import xrpl_client
from auth.models import ChallengeRequest, AuthPayload
from auth.services.jwt import create_access_token
from auth.services.ipfs import retrieve_from_ipfs



authentication_router = r = APIRouter()

@r.post("/request-challenge")
def request_challenge(req: ChallengeRequest):
    nonce = secrets.token_hex(16)
    supabase_client.table("login_nonces").insert({"did": req.did, "nonce": nonce}).execute()
    return {"challenge": nonce}


@r.post("/verify")
async def verify_auth(p: AuthPayload):
    """Verify the client-signed challenge, using their on-chain DID doc."""
    # 1. Check we issued that challenge
    expected = supabase_client.table("login_nonces").select("nonce").eq("did", p.did).limit(1).execute()
    if not expected or expected.data[0]["nonce"] != p.challenge:
        raise HTTPException(400, "Invalid or missing challenge")
    #supabase_client.table("login_nonces").delete().eq("did", p.did).execute()  # Clean up the nonce

    # 2. Resolve the DID Document on XRPL
    #    DID format: did:xrp:<classicAddress>
    classic_addr = p.did.split(":")[-1]
    resp = await xrpl_client.request(
        AccountObjects(
            account=classic_addr
        )
    )

    objs = resp.result.get("account_objects", [])
    # Filter for the XRPL DID ledger entry
    did_obj = next((o for o in objs if o["LedgerEntryType"] == "DID"), None)
    if not did_obj:
        raise HTTPException(status_code=404, detail="DID Document not found on ledger")  # :contentReference[oaicite:0]{index=0}

    # 4. Extract and parse the DIDDocument field (or fallback to implicit publicKey)
    hex_uri = did_obj.get("URI")
    ipfs_uri = bytes.fromhex(hex_uri).decode("utf-8")
    did_doc = retrieve_from_ipfs(ipfs_uri)

    # Pick the first verification method
    vm = did_doc["verificationMethod"][0]
    pubkey = vm.get("publicKeyHex") or vm.get("publicKeyBase58")
    if not pubkey:
        raise HTTPException(status_code=500, detail="No supported public key in DID Document")  # :contentReference[oaicite:1]{index=1}
    
    # 5. Verify the signature over the challenge
    message = p.challenge.encode("utf-8").hex()
    message_bytes = bytes.fromhex(message)
    
    try:
        # if hexdigest
        sig_bytes = bytes.fromhex(p.signature)
    except ValueError:
        # otherwise assume Base64
        sig_bytes = base64.b64decode(p.signature)

    valid = is_valid_message(message=message_bytes, signature=sig_bytes, public_key=pubkey)

    if not valid:
        raise HTTPException(status_code=401, detail="Signature verification failed")

    # 6. Issue a JWT for the authenticated DID
    token = create_access_token(data={"sub": p.did})
    return {"access_token": token, "token_type": "bearer"}
