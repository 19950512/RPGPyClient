from dotenv import load_dotenv

load_dotenv()

import pygame
import sys
import grpc
import os
from protos import game_pb2, game_pb2_grpc
from auth.login_screen import login_screen


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('RPG do Maydas')
    while True:
        email, senha = login_screen(screen)
        # Autenticação gRPC
        channel = grpc.insecure_channel(os.getenv('GRPC_SERVER', 'localhost:5000'))
        stub = game_pb2_grpc.GameServiceStub(channel)
        response = stub.Login(game_pb2.LoginRequest(email=email, password=senha))
        if response.success:
            print('Login realizado com sucesso!')
            # Aqui você pode chamar a próxima tela do jogo
            break
        else:
            print('Falha no login:', response.message)
            font = pygame.font.Font(None, 28)
            screen.fill((30,30,30))
            err = font.render('Login ou senha inválidos.', True, (255,80,80))
            screen.blit(err, (100, 200))
            pygame.display.flip()
            pygame.time.wait(2000)

if __name__ == '__main__':
    main()
