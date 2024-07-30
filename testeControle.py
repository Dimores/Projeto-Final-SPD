import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configura a tela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Teste Visual de Inputs do Controle')

# Inicializa os joysticks
pygame.joystick.init()

# Verifica se há joysticks conectados
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Nenhum joystick conectado.")
    sys.exit()

# Pega o primeiro joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick: {joystick.get_name()}")

# Define algumas cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Loop principal
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha os eixos
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        pygame.draw.rect(screen, RED, (50, 50 + i * 50, 600, 30))
        pygame.draw.rect(screen, GREEN, (50, 50 + i * 50, 300 + axis * 300, 30))
        font = pygame.font.Font(None, 36)
        text = font.render(f'Eixo {i}: {axis:.2f}', True, BLACK)
        screen.blit(text, (660, 50 + i * 50))

    # Desenha os botões
    for i in range(joystick.get_numbuttons()):
        button = joystick.get_button(i)
        color = GREEN if button else RED
        pygame.draw.circle(screen, color, (50 + i * 50, 500), 20)
        font = pygame.font.Font(None, 36)
        text = font.render(f'B{i}', True, BLACK)
        screen.blit(text, (50 + i * 50 - 10, 530))

    # Desenha os hats (D-pads)
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        pygame.draw.rect(screen, BLUE, (50 + i * 100, 400, 30, 30))
        font = pygame.font.Font(None, 36)
        text = font.render(f'Hat {i}: {hat}', True, BLACK)
        screen.blit(text, (90 + i * 100, 400))
        
    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()
