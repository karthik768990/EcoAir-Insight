import os
from dotenv import load_dotenv
import uvicorn

# Load env variables
load_dotenv()

PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=PORT, reload=True)