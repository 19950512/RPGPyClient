
# game_screen.py
# Tela principal do jogo PyGame

import pygame
import sys
import threading
import game_pb2


PLAYER_SIZE = 32
BG_COLOR = (30, 30, 30)

import os
IMG_DIR = os.path.join(os.path.dirname(__file__), 'imagens')
PLAYER_SPRITE = pygame.image.load(os.path.join(IMG_DIR, '1.png'))
PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE, (PLAYER_SIZE, PLAYER_SIZE))
OTHER_SPRITES = [pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, f'{i}.png')), (PLAYER_SIZE, PLAYER_SIZE)) for i in range(2, 12)]

# Atualiza a posição do player no servidor periodicamente
class PositionUpdater(threading.Thread):
    def __init__(self, stub, email, status, get_pos):
        super().__init__()
        self.stub = stub
        self.email = email
        self.status = status
        self.get_pos = get_pos
        self.running = True
    def run(self):
        while self.running:
            x, y = self.get_pos()
            req = game_pb2.UpdatePlayerStatusRequest(email=self.email, status=self.status, x=x, y=y)
            try:
                self.stub.UpdatePlayerStatus(req)
            except Exception:
                pass
    def stop(self):
        self.running = False

def game_screen(screen, email, stub):
    pygame.font.init()
    font = pygame.font.Font(None, 28)
    width, height = screen.get_size()
    x, y = width//2, height//2
    speed = 5
    status = "online"
    clock = pygame.time.Clock()
    running = True
    players = []
    
    def get_pos():
        return x, y
    updater = PositionUpdater(stub, email, status, get_pos)
    updater.start()

    def fetch_players():
        try:
            resp = stub.GetOnlinePlayers(game_pb2.GetOnlinePlayersRequest())
            print("[DEBUG] Jogadores online recebidos:")
            for p in resp.players:
                print(f"  - {getattr(p, 'player_name', '?')} | email={getattr(p, 'email', '?')} | x={getattr(p, 'x', '?')} | y={getattr(p, 'y', '?')}")
            return resp.players
        except Exception as e:
            print(f"[DEBUG] Erro ao buscar jogadores: {e}")
            return []

    fetch_timer = 0
    FETCH_INTERVAL = 100  # ms (atualiza a cada 0.1s)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                updater.stop()
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    updater.stop()
                    return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= speed
        if keys[pygame.K_RIGHT]: x += speed
        if keys[pygame.K_UP]: y -= speed
        if keys[pygame.K_DOWN]: y += speed
        # Limites da tela
        x = max(0, min(width-PLAYER_SIZE, x))
        y = max(0, min(height-PLAYER_SIZE, y))
        # Atualiza lista de players a cada 0.1s
        fetch_timer += clock.get_time()
        if fetch_timer > FETCH_INTERVAL:
            players = fetch_players()
            fetch_timer = 0
        screen.fill(BG_COLOR)
        # Desenha outros jogadores
        for idx, p in enumerate(players):

            if getattr(p, 'email', None) == email:
                continue

            px, py = getattr(p, 'x', 0), getattr(p, 'y', 0)
            sprite = OTHER_SPRITES[idx % len(OTHER_SPRITES)]
            screen.blit(sprite, (px, py))
            label = font.render(p.player_name, True, (200,200,200))
            screen.blit(label, (px, py-20))

        # Desenha o próprio jogador
        screen.blit(PLAYER_SPRITE, (x, y))
        label = font.render(email, True, (255,255,255))
        screen.blit(label, (x, y-20))
        pygame.display.flip()
        clock.tick(60)
    updater.stop()
