from fastapi import APIRouter, HTTPException, status
from xrpl.asyncio.transaction import autofill_and_sign, submit
from xrpl.models.transactions import DIDSet
from xrpl.asyncio.wallet import generate_faucet_wallet
import os
from auth.services.ipfs import store_in_ipfs
from db.db import supabase_client
from auth.xrpl import xrpl_client 

# Load environment variables
NETWORK = os.getenv("XRPL_NETWORK")

did_router = r = APIRouter()

@r.post("", status_code=status.HTTP_201_CREATED)
async def create_did():
    wallet = await generate_faucet_wallet(xrpl_client)

    supabase_client.table("wallets").insert({
        "classic_address": wallet.classic_address,
        "public_key": wallet.public_key,
        "seed": wallet.seed
    }).execute()

    did = f"did:xrpl:{NETWORK}:{wallet.classic_address}"
    did_doc = {
        "@context": "https://www.w3.org/ns/did/v1",
        "id": did,
        "verificationMethod": [{
            "id": did + "#key-1",
            "type": "Ed25519VerificationKey2018",
            "controller": did,
            "publicKeyHex": wallet.public_key
        }]
    }

    ipfs_uri = store_in_ipfs(did_doc)
    uri_hex  = ipfs_uri.encode("utf-8").hex()

    # Build transaction
    tx = DIDSet(
        account = wallet.classic_address,
        uri=uri_hex
    )
    # Sign and submit
    signed = await autofill_and_sign(tx, xrpl_client, wallet)
    resp = await submit(signed, xrpl_client)

    if resp.result.get("engine_result") != "tesSUCCESS":
        raise HTTPException(400, detail=resp.result)
    
    # brand new wallet—return the seed so the client can back it up
    return {"result": resp.result, "did": did, "wallet_seed": wallet.seed}