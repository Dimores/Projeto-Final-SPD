import subprocess
import os
import threading

def run_subprocess(script_name):
    script_path = os.path.join("C:\\Users\\diego\\OneDrive\\Documentos\\SPD\\Projeto final\\Projeto-Final-SPD", script_name)
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")
        print(f"Error Output of {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    # Cria threads para rodar os scripts simultaneamente
    thread_servidor_arthur = threading.Thread(target=run_subprocess, args=('servidorArthur.py',))
    thread_servidor = threading.Thread(target=run_subprocess, args=('servidor.py',))

    # Inicia as threads
    thread_servidor_arthur.start()
    thread_servidor.start()

    # Aguarda as threads terminarem
    thread_servidor_arthur.join()
    thread_servidor.join()
