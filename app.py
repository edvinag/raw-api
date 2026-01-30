import os
import time
import threading
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

print('Starting service...')

BRIDGE = os.getenv('BRIDGE')
if not BRIDGE:
    raise RuntimeError('BRIDGE environment variable is not set')

TARGET_URL = f'{BRIDGE}/sim/all'
print(f'Polling target URL: {TARGET_URL}')

app = FastAPI()

latest_data = None
latest_error = None


def poll_bridge():
    global latest_data, latest_error

    print('Poller thread started')

    while True:
        try:
            print('Fetching data from BRIDGE...')
            r = requests.get(TARGET_URL, timeout=5)
            print(f'Response status: {r.status_code}')

            r.raise_for_status()
            latest_data = r.json()
            latest_error = None

            print('Successfully updated latest_data')

        except Exception as e:
            latest_error = str(e)
            print(f'Polling error: {latest_error}')

        time.sleep(1)


@app.get('/latest')
def latest():
    print('GET /latest called')

    if latest_data is None:
        print('No data available yet')
        return JSONResponse(
            status_code=503,
            content={'status': 'no_data', 'error': latest_error}
        )

    print('Returning latest data')
    return {'status': 'ok', 'data': latest_data}


threading.Thread(target=poll_bridge, daemon=True).start()
