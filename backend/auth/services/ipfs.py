import os
import json
import requests

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")

def store_in_ipfs(did_doc: dict) -> str:
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_API_SECRET
    }

    body = {
        "pinataMetadata": {"name": "my-xrp-did"},
        "pinataContent": did_doc
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))
    resp.raise_for_status()

    data = resp.json()
    cid = data["IpfsHash"]
    return f"ipfs://{cid}"

def retrieve_from_ipfs(ipfs_uri: str) -> dict:
    cid = ipfs_uri.removeprefix("ipfs://")
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json()