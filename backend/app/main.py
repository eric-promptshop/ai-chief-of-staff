from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

app = FastAPI(
    title="AI Chief of Staff API",
    description="Backend API for the AI Chief of Staff application",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Chief of Staff API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 