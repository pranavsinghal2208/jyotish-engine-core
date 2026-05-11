import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from src.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
