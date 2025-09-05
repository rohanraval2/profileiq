from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import linkedin_profiles

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "ProfileIQ API running"}

@app.get("/health")
def health():
    return {"ok": True}

class QueryRequest(BaseModel):
    query: str

@app.post("/api/search")
async def search_profiles(request: QueryRequest):
    results = linkedin_profiles(request.query)
    return {"results": results} 
