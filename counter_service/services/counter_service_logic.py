import time

class CounterService:
    def __init__(self):
        self.db = {"account_balance": 0}
        print(f"initial balance: {self.db['account_balance']}")

    def update_balance(self, value: str):
        try:
            number = int(value)
            time.sleep(0.5) 
            
            self.db["account_balance"] += number
            print(f"balance updated, new balance: {self.db['account_balance']}")
        except ValueError:
            print(f"received non-numeric message: {value}. balance not changed")

    def get_balance(self):
        return self.db["account_balance"]

counter_logic = CounterService()