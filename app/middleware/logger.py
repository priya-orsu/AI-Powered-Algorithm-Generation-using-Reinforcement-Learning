from time import time
from datetime import datetime

from app.database.connection import api_log_collection


async def log_requests(request, call_next):

    print("🔥 MIDDLEWARE WORKING")

    start_time = time()

    response = await call_next(request)

    end_time = time()

    execution_time = round((end_time - start_time) * 1000, 2)

    api_log_collection.insert_one({

        "endpoint": request.url.path,

        "method": request.method,

        "status_code": response.status_code,

        "response_time_ms": execution_time,

        "status": "Success" if response.status_code < 400 else "Failed",

        "timestamp": datetime.now()

    })

    return response