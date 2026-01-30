import os
import time
import threading
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

print('App starting up')

BRIDGE = os.getenv('BRIDGE')
if not BRIDGE:
    raise RuntimeError('BRIDGE environment variable is not set')

TARGET_URL = f'{BRIDGE}/sim/all'
print(f'Polling {TARGET_URL}')

app = FastAPI()

latest_data = None
latest_error = 'poller not run yet'


def poll_bridge():
    global latest_data, latest_error

    print('Poller thread started')

    while True:
        try:
            r = requests.get(TARGET_URL, timeout=5)
            r.raise_for_status()

            latest_data = r.json()
            latest_error = None

            print('Poll ok, data updated')
        except Exception as e:
            latest_error = str(e)
            print(f'Poll error: {latest_error}')

        time.sleep(1)


@app.get('/latest')
def latest():
    if latest_data is None:
        return JSONResponse(
            status_code=503,
            content={'status': 'no_data', 'error': latest_error}
        )

    return {'status': 'ok', 'data': latest_data}


threading.Thread(target=poll_bridge, daemon=True).start()
