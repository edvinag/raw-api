import os
import time
import threading
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

BRIDGE = os.getenv('BRIDGE')
if not BRIDGE:
    raise RuntimeError('BRIDGE environment variable is not set')

TARGET_URL = f'{BRIDGE}/sim/all'

app = FastAPI()

latest_data = None
latest_error = None


def poll_bridge():
    global latest_data, latest_error

    while True:
        try:
            response = requests.get(TARGET_URL, timeout=5)
            response.raise_for_status()
            latest_data = response.json()
            latest_error = None
        except Exception as e:
            latest_error = str(e)
        time.sleep(1)


@app.get('/latest')
def get_latest():
    if latest_data is None:
        return JSONResponse(
            status_code=503,
            content={
                'status': 'no_data',
                'error': latest_error
            }
        )

    return {
        'status': 'ok',
        'data': latest_data
    }


threading.Thread(target=poll_bridge, daemon=True).start()
