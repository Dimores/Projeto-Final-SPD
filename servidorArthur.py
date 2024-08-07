import socket
import threading
import pickle
import vgamepad
import pygame

# Configuração do servidor
HOST = '0.0.0.0'
PORT = 9091

# Inicializa o Pygame (necessário para usar constantes como JOYAXISMOTION)
pygame.init()

# Inicializa o vgamepad
gamepad = vgamepad.VX360Gamepad()

# Variáveis para armazenar os valores dos eixos do analógico esquerdo
left_analog_x = 0
left_analog_y = 0

# Variáveis para armazenar os valores dos eixos do analógico direito
right_analog_x = 0
right_analog_y = 0

# Função para tratar a comunicação com o cliente
def handle_client(conn):
    while True:
        try:
            data_length_bytes = conn.recv(10).decode().strip()
            if not data_length_bytes:
                break
            data_length = int(data_length_bytes)
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
    global left_analog_x, left_analog_y, right_analog_x, right_analog_y

    # Função auxiliar para ajustar a sensibilidade
    def adjust_sensitivity(value, threshold=0.1):
        return value if abs(value) > threshold else 0

    if joystick_data["type"] == pygame.JOYAXISMOTION:
        axis = joystick_data["axis"]
        value = joystick_data["value"]
        adjusted_value = adjust_sensitivity(value)

        if axis == 0:  # Eixo X do analógico esquerdo
            left_analog_x = adjusted_value
        elif axis == 1:  # Eixo Y do analógico esquerdo
            left_analog_y = adjusted_value * -1
        elif axis == 2:  # Eixo X do analógico direito
            right_analog_x = adjusted_value
        elif axis == 3:  # Eixo Y do analógico direito
            right_analog_y = adjusted_value * -1
        elif axis == 4:  # Trigger esquerdo (L2)
            gamepad.left_trigger(value=int(adjusted_value * 255))
        elif axis == 5:  # Trigger direito (R2)
            gamepad.right_trigger(value=int(adjusted_value * 255))
        
        # Atualize o estado do analógico esquerdo
        gamepad.left_joystick_float(x_value_float=left_analog_x, y_value_float=left_analog_y)

        # Atualize o estado do analógico direito
        gamepad.right_joystick_float(x_value_float=right_analog_x, y_value_float=right_analog_y)
        gamepad.update()

    elif joystick_data["type"] == pygame.JOYBUTTONDOWN:
        button = joystick_data["button"]
        if button == 0:  # Botão A
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif button == 1:  # Botão B
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
        elif button == 2:  # Botão X
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X)
        elif button == 3:  # Botão Y
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        elif button == 4:  # Botão Back (Select)
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        elif button == 9:  # Botão LB
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        elif button == 10:  # Botão RB
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        elif button == 6:  # Botão Start
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)
        elif button == 7:  # Analógico esquerdo (L3)
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        elif button == 8:  # Analógico direito (R3)
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        elif button == 11:  # Seta para cima
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif button == 12:  # Seta para baixo
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif button == 13:  # Seta para esquerda
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif button == 14:  # Seta para direita
            gamepad.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()
    elif joystick_data["type"] == pygame.JOYBUTTONUP:
        button = joystick_data["button"]
        if button == 0:  # Botão A
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A)
        elif button == 1:  # Botão B
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B)
        elif button == 2:  # Botão X
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X)
        elif button == 3:  # Botão Y
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        elif button == 9:  # Botão LB
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        elif button == 10:  # Botão RB
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        elif button == 4:  # Botão Back (Select)
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        elif button == 6:  # Botão Start
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START)
        elif button == 7:  # Analógico esquerdo (L3)
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        elif button == 8:  # Analógico direito (R3)
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
        elif button == 11:  # Seta para cima
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif button == 12:  # Seta para baixo
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif button == 13:  # Seta para esquerda
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif button == 14:  # Seta para direita
            gamepad.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

        gamepad.update()

# Função principal do servidor
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}")

        while True:
            conn, addr = sock.accept()
            print(f"Conexão estabelecida com {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

start_server()