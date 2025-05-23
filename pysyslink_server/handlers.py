import time
from jsonrpcserver import Result, InvalidParams
from .utils import send_notification

def run_simulation(duration: float = 5.0, steps: int = 10) -> Result:
    """
    JSON-RPC method:
      name: 'runSimulation'
      params: { duration: float, steps: int }
      returns: { status: str, output: {...} }
      notifications: 'progress'
    """
    # parameter validation
    if steps <= 0:
        raise InvalidParams("`steps` must be > 0")
    if duration < 0:
        raise InvalidParams("`duration` must be >= 0")

    # initial progress
    send_notification("progress", { "progress": 0 })

    for i in range(1, steps + 1):
        time.sleep(duration / steps)
        pct = int((i / steps) * 100)
        send_notification("progress", { "progress": pct })

    # finalize
    result = {
        "status": "completed",
        "output": {
            "dummyValue": 42,
            "message": f"Simulated for {duration}s in {steps} steps."
        }
    }
    return result
