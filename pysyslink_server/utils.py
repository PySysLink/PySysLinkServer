import sys
import json

def send_notification(method: str, params: dict):
    """Send a JSON-RPC notification via stdout."""
    msg = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
    }
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()
