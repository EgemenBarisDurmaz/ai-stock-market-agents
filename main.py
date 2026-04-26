import threading
import uvicorn
from db.database import init_db
from scheduler import run_analysis_all, start_scheduler


if __name__ == "__main__":
    init_db()

    thread = threading.Thread(target=run_analysis_all)
    thread.start()

    start_scheduler()

    uvicorn.run("api.dashboard:app", host="0.0.0.0", port=8000, reload=False)