import websockets
import json

async def generate_image(prompt, width, height, workflow_id, model):
    uri = "ws://localhost:9000"
    async with websockets.connect(uri) as websocket:
        request = {
            "type": "generate_image",
            "params": json.dumps({
                "prompt": prompt,
                "width": width,
                "height": height,
                "workflow_id": workflow_id,
                "model": model
            })
        }
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        return json.loads(response)
