import socket
import threading
import pickle
import mss
import numpy as np
import zlib
import cv2

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 9090
REDUCE_SCALE = 0.4

# Função para capturar a tela e enviar ao cliente
def capture_and_send_screen(conn):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width, height = int(monitor["width"] * REDUCE_SCALE), int(monitor["height"] * REDUCE_SCALE)
        resolution = (width, height)
        conn.sendall(pickle.dumps(resolution))
        
        try:
            while True:
                img = sct.grab(monitor)
                img_array = np.array(img)
                if img_array.ndim == 3 and img_array.shape[2] == 4:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
                    img_array = cv2.resize(img_array, resolution)
                    data = pickle.dumps(img_array)
                    compressed_data = zlib.compress(data)
                    conn.sendall(len(compressed_data).to_bytes(4, 'big'))
                    conn.sendall(compressed_data)
                else:
                    print("Frame capturado não é um array 3D com 4 canais (BGRA)")
        except Exception as e:
            print(f"Erro ao capturar e enviar dados: {e}")
        finally:
            conn.close()


# Função para tratar a comunicação com o cliente
def handle_client(conn):
    threading.Thread(target=capture_and_send_screen, args=(conn,)).start()
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
    except Exception as e:
        print(f"Erro ao tratar a comunicação com o cliente: {e}")
    finally:
        conn.close()

# Inicia o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor escutando em {HOST}:{PORT}")

# Aceita conexões de clientes
while True:
    try:
        conn, addr = server.accept()
        print(f"Conectado por {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")