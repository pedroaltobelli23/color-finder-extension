import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run("app:app", port=5000, log_level="debug", host="0.0.0.0", workers=1, reload=True)