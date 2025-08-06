
# login.py
# Tela de login do cliente PyGame

import pygame
import sys
import grpc
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'protos'))
import game_pb2, game_pb2_grpc

def login_screen(screen):
    font = pygame.font.Font(None, 36)
    input_box_email = pygame.Rect(200, 180, 240, 40)
    input_box_senha = pygame.Rect(200, 240, 240, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_email = color_inactive
    color_senha = color_inactive
    active_email = True
    active_senha = False
    email = ''
    senha = ''
    done = False
    error_msg = ''
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_email.collidepoint(event.pos):
                    active_email = True
                    active_senha = False
                elif input_box_senha.collidepoint(event.pos):
                    active_email = False
                    active_senha = True
                else:
                    active_email = False
                    active_senha = False
                color_email = color_active if active_email else color_inactive
                color_senha = color_active if active_senha else color_inactive
            if event.type == pygame.KEYDOWN:
                if active_email:
                    if event.key == pygame.K_RETURN:
                        active_email = False
                        active_senha = True
                        color_email = color_inactive
                        color_senha = color_active
                    elif event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        email += event.unicode
                elif active_senha:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        senha = senha[:-1]
                    else:
                        senha += event.unicode
        screen.fill((30, 30, 30))
        font_label = pygame.font.Font(None, 28)
        label_email = font_label.render('Email:', True, (200,200,200))
        label_senha = font_label.render('Senha:', True, (200,200,200))
        screen.blit(label_email, (100, 190))
        screen.blit(label_senha, (100, 250))
        txt_email = font.render(email, True, color_email)
        txt_senha = font.render('*'*len(senha), True, color_senha)
        input_box_email.w = max(240, txt_email.get_width()+10)
        input_box_senha.w = max(240, txt_senha.get_width()+10)
        screen.blit(txt_email, (input_box_email.x+5, input_box_email.y+5))
        screen.blit(txt_senha, (input_box_senha.x+5, input_box_senha.y+5))
        pygame.draw.rect(screen, color_email, input_box_email, 2)
        pygame.draw.rect(screen, color_senha, input_box_senha, 2)
        if error_msg:
            err = font_label.render(error_msg, True, (255,80,80))
            screen.blit(err, (200, 300))
        pygame.display.flip()
    return email, senha

def autenticar(email, senha):
    try:
        channel = grpc.insecure_channel('localhost:5000')
        stub = game_pb2_grpc.GameServiceStub(channel)
        response = stub.Login(game_pb2.LoginRequest(email=email, password=senha))
        return response.success, response.message
    except Exception as e:
        return False, str(e)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('RPG Multiplayer Login')
    import game_screen
    while True:
        email, senha = login_screen(screen)
        try:
            channel = grpc.insecure_channel('localhost:5000')
            stub = game_pb2_grpc.GameServiceStub(channel)
            response = stub.Login(game_pb2.LoginRequest(email=email, password=senha))
            if response.success:
                game_screen.game_screen(screen, email, stub)
                break
            else:
                font = pygame.font.Font(None, 28)
                screen.fill((30,30,30))
                err = font.render(f'Erro: {response.message}', True, (255,80,80))
                screen.blit(err, (100, 200))
                pygame.display.flip()
                pygame.time.wait(2000)
        except Exception as e:
            font = pygame.font.Font(None, 28)
            screen.fill((30,30,30))
            err = font.render(f'Erro: {e}', True, (255,80,80))
            screen.blit(err, (100, 200))
            pygame.display.flip()
            pygame.time.wait(2000)

if __name__ == '__main__':
    main()
