import httpx
import random
import os

class FacadeService:
    def __init__(self):
        self.consul_host = os.getenv('CONSUL_HOST', 'consul')
        self.consul_port = os.getenv('CONSUL_PORT', '8500')
        self.consul_url = f"http://{self.consul_host}:{self.consul_port}"

    async def _get_random_node(self, service_name: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.consul_url}/v1/health/service/{service_name}?passing=true")
                if response.status_code == 200:
                    nodes = response.json()
                    if nodes:
                        node = random.choice(nodes)
                        address = node['Service']['Address']
                        port = node['Service']['Port']
                        return f"http://{address}:{port}"
            except Exception as e:
                print(f"error finding nodes for {service_name} in Consul: {e}")
        return None

    async def sendMessageToLoggingAndQueue(self, msg_uuid, text):
        queue_path = "queue.txt"
        
        logging_url = await self._get_random_node("logging-service")
        if logging_url:
            async with httpx.AsyncClient() as client:
                try:
                    await client.post(f'{logging_url}/save-msg', json={"msg_uuid": msg_uuid, "text": text})
                except Exception as e:
                    print(f"logging error {e}")

        try:
            with open(queue_path, "a") as f:
                f.write(f"{text}\n")
            print(f"success added {text} to queue file")
        except Exception as e:
            print(f"error writing to queue: {e}")

        return {"status": "ok"}

    async def getItemsFromLoggerService(self):
        logging_url = await self._get_random_node("logging-service")
        counter_url = await self._get_random_node("counter-service") 

        if not logging_url or not counter_url:
            return {"status": "error", "message": "services not found in Consul"}

        async with httpx.AsyncClient() as client:
            try:
                log_res = await client.get(f'{logging_url}/get-msg')
                count_res = await client.get(counter_url) 
                
                logs = log_res.json().get("message", "")
                balance = count_res.json().get("message", "0")
                
                return {"status": "ok", "message": f"logs: {logs} , balance: {balance}"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

facade_logic = FacadeService()