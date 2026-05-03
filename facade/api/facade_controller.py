from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import time
import os
import consul
import socket
from facade.services.facade_service import facade_logic

class PrivitiveRequest(BaseModel):
    text: str

app = FastAPI()
CONSUL_HOST = os.getenv('CONSUL_HOST', 'consul')
CONSUL_PORT = int(os.getenv('CONSUL_PORT', 8500))
SERVICE_NAME = 'facade-service'
SERVICE_PORT = 8000

def register_to_consul():
    try:
        c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
        service_address = socket.gethostbyname(socket.gethostname())
        service_id = f"{SERVICE_NAME}-{service_address}-{SERVICE_PORT}"

        c.agent.service.register(
            name=SERVICE_NAME,
            service_id=service_id,
            address=service_address,
            port=SERVICE_PORT,
            check=consul.Check.tcp(service_address, SERVICE_PORT, "10s")
        )
        print(f"registerd {SERVICE_NAME} in consul")
    except Exception as e:
        print(f"error {e}")

@app.on_event("startup")
def startup_event():
    register_to_consul()

@app.get("/")
def root_get():
    return {"message": "hi hi from facade"}

@app.post("/save-msg")
async def root_post(request: PrivitiveRequest):
    start_time = time.time()
    
    msg_uuid = str(uuid.uuid4())
    text = request.text

    result = await facade_logic.sendMessageToLoggingAndQueue(msg_uuid, text)

    duration = (time.time() - start_time) * 1000
    print(f"request handled in {duration:.2f} ms")
    
    result["performance_ms"] = f"{duration:.2f}"
    return result

@app.get("/get-msgs")
async def get_messages():
    return await facade_logic.getItemsFromLoggerService()