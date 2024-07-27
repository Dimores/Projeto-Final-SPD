import socket
import threading
import pickle
import mss
import numpy as np
import zlib
import cv2
import vgamepad
import pygame

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 9090
REDUCE_SCALE = 0.4

# Inicializa o Pygame (necessário para usar constantes como JOYAXISMOTION)
pygame.init()

# Inicializa o vgamepad
gamepad = vgamepad.VX360Gamepad()

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
    while True:
        try:
            data_length_bytes = conn.recv(4)
            if not data_length_bytes:
                break
            data_length = int.from_bytes(data_length_bytes, 'big')
            data = b''
            while len(data) < data_length:
                packet = conn.recv(data_length - len(data))
                if not packet:
                    break
                data += packet
            joystick_data = pickle.loads(data)
            process_joystick_data(joystick_data)
        except Exception as e:
            print(f"Erro ao receber comando: {e}")
            break

# Função para processar dados do joystick
def process_joystick_data(joystick_data):
    if joystick_data["type"] == pygame.JOYAXISMOTION:
        axis = joystick_data["axis"]
        value = joystick_data["value"]
        # Comentar os logs dos comandos do joystick
        # print(f"Recebido comando do joystick: EIXO - Axis: {axis}, Value: {value}")
        # Lógica para manipular os dados do eixo do joystick
        if axis == 0:  # Eixo X
            gamepad.left_joystick_float(x_value_float=value, y_value_float=0)
        elif axis == 1:  # Eixo Y
            gamepad.left_joystick_float(x_value_float=0, y_value_float=value)
    elif joystick_data["type"] == pygame.JOYBUTTONDOWN:
        button = joystick_data["button"]
        # Comentar os logs dos comandos do joystick
        # print(f"Recebido comando do joystick: BOTÃO PRESSIONADO - Button: {button}")
        # Lógica para manipular os dados dos botões do joystick
        if button == 0:  # Botão A
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif button == 1:  # Botão B
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
    elif joystick_data["type"] == pygame.JOYBUTTONUP:
        button = joystick_data["button"]
        # Comentar os logs dos comandos do joystick
        # print(f"Recebido comando do joystick: BOTÃO SOLTO - Button: {button}")
        if button == 0:  # Botão A
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif button == 1:  # Botão B
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()

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
