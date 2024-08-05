import socket
import pickle
import pygame

# Configuração do cliente
HOST = '192.168.0.5'
PORT = 9090

# Inicializa o Pygame
pygame.init()

# Configura o joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Conecta ao servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Função para enviar comandos do joystick ao servidor
def send_joystick_data():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = round(event.value, 4)
                data = {
                    "type": pygame.JOYAXISMOTION,
                    "axis": axis,
                    "value": value
                }
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                data = {
                    "type": pygame.JOYBUTTONDOWN,
                    "button": button
                }
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                data = {
                    "type": pygame.JOYBUTTONUP,
                    "button": button
                }
            else:
                continue
            
            serialized_data = pickle.dumps(data)
            sock.sendall(f"{len(serialized_data):<10}".encode())  # Envia comprimento fixo de 10 caracteres
            sock.sendall(serialized_data)

if __name__ == "__main__":
    send_joystick_data()
