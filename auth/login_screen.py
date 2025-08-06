import pygame
import sys
import grpc
import os
from protos import game_pb2, game_pb2_grpc
from .create_account_screen import create_account_screen
from .select_character import select_character_screen

def do_login(stub, email, senha):
    req = game_pb2.LoginRequest(email=email, password=senha)
    resp = stub.Login(req)
    return resp

def login_screen(screen):
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    width, height = screen.get_size()
    input_box_email = pygame.Rect(width//2-120, height//2-60, 240, 36)
    input_box_senha = pygame.Rect(width//2-120, height//2, 240, 36)
    btn_entrar = pygame.Rect(width//2-120, height//2+60, 110, 40)
    btn_criar = pygame.Rect(width//2+10, height//2+60, 110, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_btn = pygame.Color('gray20')
    color_btn_hover = pygame.Color('gray40')
    focus = 0  # 0=email, 1=senha, 2=entrar, 3=criar
    email = ''
    senha = ''
    error_msg = ''
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_email.collidepoint(event.pos):
                    focus = 0
                elif input_box_senha.collidepoint(event.pos):
                    focus = 1
                elif btn_entrar.collidepoint(event.pos):
                    focus = 2
                    # Autentica
                    server_addr = os.getenv("GRPC_SERVER", "localhost:50051")
                    channel = grpc.insecure_channel(server_addr)
                    stub = game_pb2_grpc.GameServiceStub(channel)
                    resp = do_login(stub, email, senha)
                    if resp.success:
                        characters = []
                        if hasattr(resp, 'characters') and resp.characters:
                            for c in resp.characters:
                                characters.append({
                                    'name': getattr(c, 'name', 'Sem nome'),
                                    'vocation': getattr(c, 'vocation', '-'),
                                    'level': getattr(c, 'level', 1)
                                })
                        else:
                            characters = [{
                                'name': getattr(resp, 'player_name', email),
                                'vocation': getattr(resp, 'vocation', '-'),
                                'level': getattr(resp, 'level', 1)
                            }]
                        selected = select_character_screen(screen, characters)
                        return email, senha, selected
                    else:
                        error_msg = resp.message or 'Login ou senha inválidos.'
                        continue
                elif btn_criar.collidepoint(event.pos):
                    focus = 3
                    # Chama tela de cadastro
                    server_addr = os.getenv("GRPC_SERVER", "localhost:50051")
                    channel = grpc.insecure_channel(server_addr)
                    stub = game_pb2_grpc.GameServiceStub(channel)
                    created = create_account_screen(screen, stub)
                    if created:
                        error_msg = 'Conta criada! Faça login.'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    focus = (focus + 1) % 4
                elif focus == 0:
                    if event.key == pygame.K_RETURN:
                        focus = 1
                    elif event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        if len(email) < 50 and event.unicode.isprintable():
                            email += event.unicode
                elif focus == 1:
                    if event.key == pygame.K_RETURN:
                        focus = 2
                    elif event.key == pygame.K_BACKSPACE:
                        senha = senha[:-1]
                    else:
                        if len(senha) < 32 and event.unicode.isprintable():
                            senha += event.unicode
                elif focus == 2:
                    if event.key == pygame.K_RETURN:
                        # Simula clique no botão entrar
                        focus = 2
                        server_addr = os.getenv("GRPC_SERVER", "localhost:50051")
                        channel = grpc.insecure_channel(server_addr)
                        stub = game_pb2_grpc.GameServiceStub(channel)
                        resp = do_login(stub, email, senha)
                        if resp.success:
                            characters = []
                            if hasattr(resp, 'characters') and resp.characters:
                                for c in resp.characters:
                                    characters.append({
                                        'name': getattr(c, 'name', 'Sem nome'),
                                        'vocation': getattr(c, 'vocation', '-'),
                                        'level': getattr(c, 'level', 1)
                                    })
                            else:
                                characters = [{
                                    'name': getattr(resp, 'player_name', email),
                                    'vocation': getattr(resp, 'vocation', '-'),
                                    'level': getattr(resp, 'level', 1)
                                }]
                            selected = select_character_screen(screen, characters)
                            return email, senha, selected
                        else:
                            error_msg = resp.message or 'Login ou senha inválidos.'
                            continue
        screen.fill((30,30,30))
        # Título
        titulo = font.render('RPG do Maydas - Entrar', True, (255,255,0))
        screen.blit(titulo, (width//2-titulo.get_width()//2, height//2-120))
        # Email
        label_email = font_small.render('Email:', True, (200,200,200))
        screen.blit(label_email, (input_box_email.x, input_box_email.y-28))
        pygame.draw.rect(screen, color_active if focus==0 else color_inactive, input_box_email, 2)
        txt_email_val = font_small.render(email, True, (255,255,255))
        screen.blit(txt_email_val, (input_box_email.x+5, input_box_email.y+5))
        # Senha
        label_senha = font_small.render('Senha:', True, (200,200,200))
        screen.blit(label_senha, (input_box_senha.x, input_box_senha.y-28))
        pygame.draw.rect(screen, color_active if focus==1 else color_inactive, input_box_senha, 2)
        txt_senha_val = font_small.render('*'*len(senha), True, (255,255,255))
        screen.blit(txt_senha_val, (input_box_senha.x+5, input_box_senha.y+5))
        # Botão Entrar
        btn_color = color_btn_hover if btn_entrar.collidepoint(mouse_pos) or focus==2 else color_btn
        pygame.draw.rect(screen, btn_color, btn_entrar, border_radius=6)
        txt_entrar = font_small.render('Entrar', True, (255,255,255))
        screen.blit(txt_entrar, (btn_entrar.x+btn_entrar.w//2-txt_entrar.get_width()//2, btn_entrar.y+8))
        # Botão Criar Conta
        btn_color2 = color_btn_hover if btn_criar.collidepoint(mouse_pos) or focus==3 else color_btn
        pygame.draw.rect(screen, btn_color2, btn_criar, border_radius=6)
        txt_criar = font_small.render('Criar Conta', True, (255,255,255))
        screen.blit(txt_criar, (btn_criar.x+btn_criar.w//2-txt_criar.get_width()//2, btn_criar.y+8))
        # Mensagem de erro
        if error_msg:
            txt_error = font_small.render(error_msg, True, (255,80,80))
            screen.blit(txt_error, (width//2-txt_error.get_width()//2, btn_criar.y+60))
        pygame.display.flip()
