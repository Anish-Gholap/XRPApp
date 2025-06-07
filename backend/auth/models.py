from pydantic import BaseModel, Field
from typing import Optional

class DIDDocument(BaseModel):
    id: str = Field(..., description="Full DID URI, e.g. did:xrpl:test:<classic_address>")
    verificationMethod: list
    authentication: list
    service: list = Field(default_factory=list)

class DIDCreateRequest(BaseModel):
    seed: Optional[str] = None


class ChallengeRequest(BaseModel):
    did: str

class AuthPayload(BaseModel):
    did: str
    challenge: str
    signature: str

class LoginRequest(BaseModel):
    did: str
    signature: str  # hex-encoded signature over the nonce