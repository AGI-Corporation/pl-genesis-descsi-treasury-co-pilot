"""
pl-genesis-descsi-treasury-co-pilot
AI-driven treasury co-pilot for decentralized science (DeSci) projects.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PL Genesis DeSci Treasury Co-Pilot",
    description="AI treasury co-pilot for DeSci resource allocation",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"service": "pl-genesis-descsi-treasury-co-pilot", "status": "online"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
