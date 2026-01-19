import os
import psutil
from datetime import datetime, timedelta

async def get_health():
    """
    Get system health information
    """
    process = psutil.Process()
    return {
        "status": "ok",
        "uptime": time.time() - process.create_time(),
        "timestamp": datetime.utcnow().isoformat()
    }
