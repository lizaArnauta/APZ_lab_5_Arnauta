import subprocess
import time
import sys
import os

def run_service(path, port):
    cmd = [sys.executable, path]
    print(f"starting service on port {port} from {path}")
    return subprocess.Popen(cmd, shell=False)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    services = [
        (os.path.join(base_dir, "logging", "main.py"), 8002),
        (os.path.join(base_dir, "message", "main.py"), 8003),
        (os.path.join(base_dir, "facade", "main.py"), 8001)
    ]

    processes = []
    
    try:
        for script, port in services:
            p = run_service(script, port)
            processes.append(p)
            time.sleep(1)

        print("\n⊹₊˚‧︵‿₊୨ᰔ system is running! ᰔ୧₊‿︵‧˚₊⊹\n")
        print("url: http://127.0.0.1:8001/docs")
        print("ctrl c to end work ₍^. .^₎⟆ \n")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n stopping all services ₍^. .^₎⟆ ")
        for p in processes:
            p.terminate()
        print("\n⊹₊˚‧︵‿₊୨ᰔ system stopped! ᰔ୧₊‿︵‧˚₊⊹\n")