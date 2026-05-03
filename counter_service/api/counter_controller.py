from fastapi import FastAPI
import sys
import threading
import time
import os
import socket
import consul
from counter_service.services.counter_service_logic import counter_logic

app = FastAPI()
PORT = 8000
for i, arg in enumerate(sys.argv):
    if arg == "--port" and i + 1 < len(sys.argv):
        PORT = int(sys.argv[i + 1])

CONSUL_HOST = os.getenv('CONSUL_HOST', 'consul')
CONSUL_PORT = int(os.getenv('CONSUL_PORT', 8500))
SERVICE_NAME = 'counter-service'

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
        print(f"registred in {SERVICE_NAME} consul")
    except Exception as e:
        print(f"error {e}")

def mq_consumer_loop():
    queue_path = "queue.txt"
    while True:
        if os.path.exists(queue_path) and os.path.getsize(queue_path) > 0:
            with open(queue_path, "r") as f:
                lines = f.readlines()
            
            open(queue_path, "w").close()

            for line in lines:
                val = line.strip()
                if val:
                    print(f"consumed: {val}")
                    counter_logic.update_balance(val)
        time.sleep(2)

@app.on_event("startup")
def startup_event():
    register_to_consul()
    threading.Thread(target=mq_consumer_loop, daemon=True).start()

@app.get("/")
async def get_balance():
    return {"status": "ok", "message": str(counter_logic.get_balance())}