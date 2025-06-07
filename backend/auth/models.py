from pydantic import BaseModel
from typing import Optional

class CreateDIDRequest(BaseModel):
    name: str
    email: str
    phone: str

class DIDResponse(BaseModel):
    did: str
    xrpl_address: str
    attestation_tx_hash: str

class KYCRequest(BaseModel):
    did: str
    document_type: str  # "passport", "national_id", etc.
    document_ipfs_hash: str
    provider: str = "fractal"  # Default KYC provider

class KYCResponse(BaseModel):
    status: str  # "pending", "verified", "rejected"
    kyc_tx_hash: Optional[str] = None