import subprocess
import os
import threading

def run_subprocess(script_name):
    script_path = os.path.join("", script_name)
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
        print(f"Error Output of {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    # Cria threads para rodar os scripts simultaneamente
    thread_client = threading.Thread(target=run_subprocess, args=('client.py',))
    thread_client_arthur = threading.Thread(target=run_subprocess, args=('clientArthur.py',))

    # Inicia as threads
    thread_client.start()
    thread_client_arthur.start()

    # Aguarda as threads terminarem
    thread_client.join()
    thread_client_arthur.join()
