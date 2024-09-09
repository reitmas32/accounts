import json
import time

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class WebHookDTO(BaseModel):
    resource: str
    response: dict

@app.post("/webhook")
async def webhook(request: WebHookDTO):
    # Lee el cuerpo JSON recibido
    json_body = request.model_dump()

    print(json.dumps(json_body, indent=2))

    time.sleep(2)

    # Retorna el mismo cuerpo JSON como respuesta
    return json_body
