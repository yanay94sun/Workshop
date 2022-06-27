from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


async def send_ws_message(msg: str, ws: WebSocket):
    print("trying to send msg to client")
    try:
        await ws.send_text(msg)
        return True
    except WebSocketDisconnect:
        return False
