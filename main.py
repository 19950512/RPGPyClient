
from dotenv import load_dotenv
load_dotenv()

import pygame
import sys
import grpc
import os
from protos import game_pb2, game_pb2_grpc
from auth.login_screen import login_screen
from game_screen import game_screen

import contextlib


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('RPG do Maydas')

    # Suprimir logs se --quiet
    quiet = '--quiet' in sys.argv or '-q' in sys.argv
    if quiet:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    # O login_screen já faz login e seleção de personagem
    email, senha, character = login_screen(screen)
    if not quiet:
        print(f'Login realizado com sucesso! Personagem selecionado: {character}')

    # Conecta ao servidor gRPC para o jogo
    server_addr = os.getenv("GRPC_SERVER", "localhost:50051")
    channel = grpc.insecure_channel(server_addr)
    stub = game_pb2_grpc.GameServiceStub(channel)

    # Chama a tela principal do jogo, passando email e stub (e character se necessário)
    game_screen(screen, email, stub)

if __name__ == '__main__':
    main()
