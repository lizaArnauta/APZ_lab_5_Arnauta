from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import socket
import consul

from lisalogging.services.logging_service import logging_logic

app = FastAPI()
class MessageRequest(BaseModel):
    msg_uuid: str
    text: str

PORT = 8000 
for i, arg in enumerate(sys.argv):
    if arg == "--port" and i + 1 < len(sys.argv):
        PORT = int(sys.argv[i + 1])

CONSUL_HOST = os.getenv('CONSUL_HOST', 'consul')
CONSUL_PORT = int(os.getenv('CONSUL_PORT', 8500))
SERVICE_NAME = 'logging-service'

def register_to_consul():
    try:
        c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
        service_address = socket.gethostbyname(socket.gethostname())
        service_id = f"{SERVICE_NAME}-{service_address}-{PORT}"

        c.agent.service.register(
            name=SERVICE_NAME,
            service_id=service_id,
            address=service_address,
            port=PORT,
            check=consul.Check.tcp(service_address, PORT, "10s")
        )
        print(f"regictred in {SERVICE_NAME} {service_id}) consul")
    except Exception as e:
        print(f"error {e}")

@app.on_event("startup")
def startup_event():
    register_to_consul()

@app.get("/")
def read_root():
    return {"message": "message from logging"}

@app.post("/save-msg")
def saveMsg(request: MessageRequest):
    print(f"entered save msg controller for port {PORT}")
    logging_logic.save_message(request.msg_uuid, request.text)
    return {"status": "ok"}

@app.get("/get-msg")
def getMsg():
    values = logging_logic.get_all_messages()
    if values != "":
        return {"status": "success", "message": values}
    else:
        return {"status": "fail", "message": "dictionary is empty"}