import socket
import pickle
import zlib
import pygame
import sys
import threading
import cv2  # Adicionar OpenCV para manipulação da imagem

# Configuração do cliente
HOST = '192.168.0.12'
PORT = 9090


# Inicializa o Pygame
pygame.init()

# Função para receber e exibir a tela
def receive_and_display_screen(conn):
    resolution_data = conn.recv(1024)
    resolution = pickle.loads(resolution_data)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Client")

    try:
        while True:
            # Recebe o comprimento dos dados
            data_length_bytes = conn.recv(4)
            if not data_length_bytes:
                break
            data_length = int.from_bytes(data_length_bytes, 'big')
            
            # Recebe os dados da tela comprimidos
            compressed_data = b''
            while len(compressed_data) < data_length:
                packet = conn.recv(data_length - len(compressed_data))
                if not packet:
                    break
                compressed_data += packet

            # Descomprime os dados
            data = zlib.decompress(compressed_data)
            img_array = pickle.loads(data)

            # Rotaciona a imagem
            img_array = cv2.rotate(img_array, cv2.ROTATE_90_CLOCKWISE)

            # Converte o array para uma superfície do Pygame
            img_surface = pygame.surfarray.make_surface(img_array)

            # Exibe a tela
            screen.blit(img_surface, (0, 0))
            pygame.display.update()
    except Exception as e:
        print(f"Erro ao receber e exibir a tela: {e}")
    finally:
        conn.close()

# Função para enviar comandos do joystick
def send_joystick_commands(conn):
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                    joystick_data = {
                        "type": event.type,
                        "axis": event.axis if event.type == pygame.JOYAXISMOTION else None,
                        "value": event.value if event.type == pygame.JOYAXISMOTION else None,
                        "button": event.button if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP] else None,
                    }
                    data = pickle.dumps(joystick_data)
                    data_length = len(data)
                    conn.sendall(data_length.to_bytes(4, 'big') + data)
                    # Comentar o log dos comandos do joystick
                    # print(f"Enviado comando do joystick: {joystick_data}")
    except Exception as e:
        print(f"Erro ao enviar comando do joystick: {e}")
    finally:
        conn.close()

# Conecta ao servidor
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))

# Inicia as threads para receber a tela e enviar comandos do joystick
receive_thread = threading.Thread(target=receive_and_display_screen, args=(conn,))
send_thread = threading.Thread(target=send_joystick_commands, args=(conn,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

pygame.quit()
sys.exit()
