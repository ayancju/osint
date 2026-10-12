"""Direct entry point to launch the OSINT Fusion Workbench Web Server."""

import sys
import uvicorn

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    print(f"============================================================")
    print(f"  OSINT Fusion Workbench — Multilingual Analysis Agent      ")
    print(f"  Server URL: http://127.0.0.1:{port}                         ")
    print(f"  API Docs:   http://127.0.0.1:{port}/docs                    ")
    print(f"============================================================")
    uvicorn.run("osint_fusion.api.app:app", host="127.0.0.1", port=port, log_level="info")
