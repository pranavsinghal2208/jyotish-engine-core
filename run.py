import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))

try:
    import uvicorn
    from src.main import app
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
except Exception:
    traceback.print_exc()
    sys.exit(1)
