from fastapi import FastAPI

app = FastAPI(
    title="AI Smart Assistant Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "AI Smart Assistant Backend Running"}