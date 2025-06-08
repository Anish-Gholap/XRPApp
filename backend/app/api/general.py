from fastapi import APIRouter

general_router = r = APIRouter()

@r.get("/loans")
async def get_loans():
    return  [
            {
                "id": 1,
                "borrower": "Maria Santos",
                "avatar": "/placeholder.svg?height=40&width=40",
                "location": "Philippines → USA",
                "amount": 2500,
                "purpose": "Family medical emergency",
                "credit_score": 785,
                "interest_rate": 8.5,
                "term": "6 months",
                "remittance_history": 24,
                "total_remittances": 45000,
                "rating": 4.8,
            },
            {
                "id": 2,
                "borrower": "Ahmed Hassan",
                "avatar": "/placeholder.svg?height=40&width=40",
                "location": "Egypt → UAE",
                "amount": 1800,
                "purpose": "Business expansion",
                "credit_score": 720,
                "interest_rate": 9.2,
                "term": "12 months",
                "remittance_history": 18,
                "total_remittances": 32000,
                "rating": 4.6,
            },
            {
                "id": 3,
                "borrower": "Rosa Martinez",
                "avatar": "/placeholder.svg?height=40&width=40",
                "location": "Mexico → USA",
                "amount": 3200,
                "purpose": "Home renovation",
                "credit_score": 650,
                "interest_rate": 11.8,
                "term": "9 months",
                "remittance_history": 12,
                "total_remittances": 28000,
                "rating": 4.3,
            },
        ],



@r.get("/remittances")
async def get_remittances():
    return  [
            {"id": 1, "recipient": "Maria Santos", "amount": 500, "date": "2024-01-15", "status": "Completed"},
            {"id": 2, "recipient": "Juan Rodriguez", "amount": 750, "date": "2024-01-10", "status": "Completed"},
            {"id": 3, "recipient": "Ana Garcia", "amount": 300, "date": "2024-01-05", "status": "Pending"},
        ]
    

@r.get("/200OK")
async def get_200OK():
    return {"message": "200 OK"}