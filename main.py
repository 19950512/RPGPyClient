import pygame
import sys
import grpc
from protos import game_pb2, game_pb2_grpc

def login_screen(screen):
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(200, 200, 240, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(240, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
    return text

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('RPG Multiplayer Login')
    email = login_screen(screen)
    # Aqui você pode chamar o servidor gRPC para autenticar
    # Exemplo:
    # channel = grpc.insecure_channel('localhost:5000')
    # stub = game_pb2_grpc.GameServiceStub(channel)
    # response = stub.Login(game_pb2.LoginRequest(email=email, password='123'))
    # if response.success:
    #     # Entrar no jogo
    # else:
    #     # Mostrar erro

# main.py
# Entry point para o cliente PyGame

if __name__ == '__main__':
    main()
