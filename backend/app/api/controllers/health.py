import os
import psutil
from datetime import datetime, timedelta

async def get_health():
    """
    Get system health information
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_usage": {
                "rss_mb": memory_info.rss / (1024 * 1024),  # Convert to MB
                "vms_mb": memory_info.vms / (1024 * 1024),  # Convert to MB
                "percent": process.memory_percent()
            },
            "disk_usage": {
                "free_gb": psutil.disk_usage('/').free / (1024 ** 3),  # Convert to GB
                "total_gb": psutil.disk_usage('/').total / (1024 ** 3),  # Convert to GB
                "percent": psutil.disk_usage('/').percent
            },
            "uptime_seconds": psutil.boot_time()
        },
        "process": {
            "pid": os.getpid(),
            "create_time": datetime.fromtimestamp(process.create_time()).isoformat(),
            "cpu_times": process.cpu_times()._asdict(),
            "threads": process.num_threads()
        }
    }
