import asyncio
import websockets

connected_clients = set()

async def echo(websocket, path):
    # クライアントの接続を管理
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            
            # 特定のメッセージに対する応答
            if message == "ping":
                await websocket.send("pong")
            elif message.startswith("hello"):
                name = message.split()[1] if len(message.split()) > 1 else "stranger"
                await websocket.send(f"Hello, {name}!")
            else:
                await websocket.send(f"Echo: {message}")
            
            # 受信したメッセージを他のクライアントにブロードキャスト
            for client in connected_clients:
                if client != websocket:
                    await client.send(f"Broadcast from {websocket.remote_address}: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client {websocket.remote_address} disconnected: {e}")
    finally:
        # クライアントの切断を管理
        connected_clients.remove(websocket)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_forever()