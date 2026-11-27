from time import time
from datetime import datetime
from starlette.concurrency import run_in_threadpool

from app.database.connection import api_log_collection


def _write_api_log(doc: dict):
    try:
        api_log_collection.insert_one(doc)
    except Exception as exc:
        print(f"[LOGGER WARNING] Could not write API log to MongoDB: {exc}")


async def log_requests(request, call_next):
    start_time = time()
    response = await call_next(request)
    end_time = time()

    if request.method == "OPTIONS":
        return response

    execution_time = round((end_time - start_time) * 1000, 2)
    log_doc = {
        "endpoint": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "response_time_ms": execution_time,
        "status": "Success" if response.status_code < 400 else "Failed",
        "timestamp": datetime.now(),
    }

    await run_in_threadpool(_write_api_log, log_doc)
    return response