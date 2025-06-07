from fastapi import APIRouter, HTTPException, status
from auth.models import CreateDIDRequest, DIDResponse, KYCRequest, KYCResponse
import uuid
from db.db import supabase_client

did_router = r = APIRouter()

# Helper Functions
def generate_xrpl_address():
    """Mock function to generate XRPL address"""
    return f"rUser{str(uuid.uuid4())[:8]}..."

def submit_to_kyc_provider(data: dict, provider: str):
    """Mock KYC submission to external provider"""
    # In production, call Fractal ID/Onfido API here
    return {"status": "verified", "tx_hash": f"KYC_{str(uuid.uuid4())[:8]}"}

@r.post("/did", response_model=DIDResponse, status_code=status.HTTP_201_CREATED)
async def create_did(request: CreateDIDRequest):
    """Create a new Decentralized Identity (DID) on XRPL"""
    did = f"did:xrpl:{str(uuid.uuid4())}"
    xrpl_address = generate_xrpl_address()
    
    try:
        # Insert into Supabase
        result = supabase_client.table("dids").insert({
            "did": did,
            "xrpl_address": xrpl_address,
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "status": "active"
        }).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create DID"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    return {
        "did": did,
        "xrpl_address": xrpl_address,
        "attestation_tx_hash": f"ATTEST_{str(uuid.uuid4())[:8]}"
    }

@r.post("/kyc", response_model=KYCResponse)
async def verify_kyc(request: KYCRequest):
    """Submit KYC documents for verification"""
    # Check if DID exists
    did_exists = supabase_client.table("dids").select("did").eq("did", request.did).execute()
    if not did_exists.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DID not found"
        )
    
    # Submit to KYC provider
    kyc_result = submit_to_kyc_provider(
        {
            "did": request.did,
            "document_type": request.document_type,
            "document_hash": request.document_ipfs_hash
        },
        provider=request.provider
    )
    
    try:
        # Store KYC request
        kyc_data = {
            "did": request.did,
            "document_type": request.document_type,
            "document_ipfs_hash": request.document_ipfs_hash,
            "provider": request.provider,
            "status": kyc_result["status"],
            "tx_hash": kyc_result["tx_hash"]
        }
        
        supabase_client.table("kyc_requests").insert(kyc_data).execute()
        
        # Update DID status if verified
        if kyc_result["status"] == "verified":
            supabase_client.table("dids").update({"kyc_status": "verified"}).eq("did", request.did).execute()
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process KYC: {str(e)}"
        )
    
    return {
        "status": kyc_result["status"],
        "kyc_tx_hash": kyc_result["tx_hash"]
    }

@r.get("/dids/{did}/status")
async def check_did_status(did: str):
    """Check DID and KYC status"""
    try:
        # Get DID info
        did_info = supabase_client.table("dids").select("*").eq("did", did).execute()
        if not did_info.data:
            raise HTTPException(status_code=404, detail="DID not found")
        
        # Get latest KYC status
        kyc_status = supabase_client.table("kyc_requests")\
            .select("status")\
            .eq("did", did)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        return {
            "did": did,
            "status": did_info.data[0]["status"],
            "kyc_status": kyc_status.data[0]["status"] if kyc_status.data else "pending"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )