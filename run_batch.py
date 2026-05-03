import subprocess
import time
import sys
import os

def run_service(path, port):
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.dirname(os.path.dirname(path))
    
    cmd = [sys.executable, path]
    print(f"starting service on port {port} from {path}")
    return subprocess.Popen(cmd, shell=False, env=env)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    services = [
        (os.path.join(base_dir, "lisalogging", "api", "logging_controller.py"), 8081),
        (os.path.join(base_dir, "counter_service", "api", "counter_controller.py"), 8082),
        (os.path.join(base_dir, "facade", "api", "facade_controller.py"), 8000)
    ]

    processes = []
    
    try:
        for script, port in services:
            if not os.path.exists(script):
                print(f"file not found in {script}")
                continue
                
            p = run_service(script, port)
            processes.append(p)
            time.sleep(1)

        print("\n⊹₊˚‧︵‿₊୨ᰔ system is running! ᰔ୧₊‿︵‧˚₊⊹\n")
        print("url: http://127.0.0.1:8000/docs")
        print("ctrl c to end work ₍^. .^₎⟆ \n")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n stopping all services ₍^. .^₎⟆ ")
        for p in processes:
            p.terminate()
        print("\n⊹₊˚‧︵‿₊୨ᰔ system stopped! ᰔ୧₊‿︵‧˚₊⊹\n")