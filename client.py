import socket
import pygame
import pickle
import threading
import numpy as np
import zlib
import ssl

# Configuração do cliente
HOST = '192.168.0.5'  # IP do servidor (verifique se este é o IP correto)
PORT = 9090

# Inicializa o Pygame
pygame.init()
pygame.joystick.init()

# Conecta ao servidor com SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = context.wrap_socket(client, server_hostname=HOST)

try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")
    exit()

# Recebe a resolução do servidor
resolution_data = client.recv(1024)
resolution = pickle.loads(resolution_data)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Cliente de Controle")
clock = pygame.time.Clock()

# Variável global para a imagem recebida
received_frame = None
frame_lock = threading.Lock()

# Função para receber a tela do servidor em uma thread separada
def receive_screen():
    global received_frame
    while True:
        try:
            # Recebe o tamanho dos dados primeiro
            data_size = int.from_bytes(client.recv(4), 'big')
            data = b""
            while len(data) < data_size:
                packet = client.recv(min(data_size - len(data), 4096))
                if not packet:
                    return
                data += packet
            if len(data) == data_size:
                decompressed_data = zlib.decompress(data)
                frame = pickle.loads(decompressed_data)
                if isinstance(frame, np.ndarray):
                    with frame_lock:
                        received_frame = frame
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            break

# Função para enviar comandos de joystick ao servidor
def send_joystick_commands():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                client.close()
                return
            if event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                joystick_data = {
                    "type": event.type,
                    "axis": event.axis if event.type == pygame.JOYAXISMOTION else None,
                    "value": event.value if event.type == pygame.JOYAXISMOTION else None,
                    "button": event.button if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP] else None
                }
                client.sendall(pickle.dumps(joystick_data))

# Inicia a thread de recebimento de tela
receive_thread = threading.Thread(target=receive_screen, daemon=True)
receive_thread.start()

# Inicia a thread de envio de comandos de joystick
joystick_thread = threading.Thread(target=send_joystick_commands, daemon=True)
joystick_thread.start()

# Loop principal do Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza a tela com a imagem recebida
    with frame_lock:
        if received_frame is not None:
            try:
                frame = pygame.surfarray.make_surface(received_frame.swapaxes(0, 1))
                screen.blit(frame, (0, 0))
                pygame.display.flip()
            except Exception as e:
                print(f"Erro ao atualizar a tela: {e}")

    clock.tick(60)

# Fecha a conexão e o Pygame
client.close()
pygame.quit()
