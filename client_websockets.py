import websockets
import asyncio
from datetime import datetime

from main import HOST, WS_PORT

connections = []


def listen():
    log(f"WebSockets listening on port {WS_PORT}...")
    ws_server = websockets.serve(handle, HOST, WS_PORT)

    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()


async def handle(websocket, path):
    connections.append(websocket)
    log(f"{websocket.remote_address[0]} ws connected")

    try:
        while True:
            message = await websocket.recv()
            log(f"{websocket.remote_address[0]} ws message \"{message}\"")
    except Exception as e:
        pass
    finally:
        connections.remove(websocket)
        log(f"{websocket.remote_address[0]} ws closed")


async def broadcast(message):
    for ws in connections:
        await ws.send(message)


def log(message):
    print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] " + message))
