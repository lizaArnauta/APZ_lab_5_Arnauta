class LoggingService:
    def __init__(self):
        self.hazelcast_map = {} 
        print(" LoggingService started in mock mode")

    def save_message(self, msg_uuid: str, text: str):
        self.hazelcast_map[msg_uuid] = text
        print(f"[LOG] Saved locally: {text} with ID: {msg_uuid}")

    def get_all_messages(self):
        values = list(self.hazelcast_map.values())
        return "".join(values) if values else ""

logging_logic = LoggingService()