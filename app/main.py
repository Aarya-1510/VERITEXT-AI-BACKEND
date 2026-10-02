from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routers.upload import router as upload_router


app = FastAPI(
    title="VeriText AI",
    description="AI-powered plagiarism detection system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://veritext-ai-frontend-i9fc7etnf-aarya-a26d.vercel.app/",
                   "https://veritext-ai-backend.onrender.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload_router)



@app.get("/")
def root():
    return {
        "message": "Welcome to VeriText AI API 🚀"
    }