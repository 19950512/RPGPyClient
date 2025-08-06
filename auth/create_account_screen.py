import pygame
import sys
from protos import game_pb2

def do_create_account(stub, email, senha, nome, vocacao):
    req = game_pb2.CreatePlayerRequest(email=email, player_name=nome, vocation_name=vocacao)
    # O backend atual não usa senha, mas já deixo o parâmetro para futura extensão
    resp = stub.CreatePlayer(req)
    return resp

def create_account_screen(screen, stub):
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    width, height = screen.get_size()
    input_box_email = pygame.Rect(width//2-120, height//2-120, 240, 36)
    input_box_senha = pygame.Rect(width//2-120, height//2-60, 240, 36)
    input_box_nome = pygame.Rect(width//2-120, height//2, 240, 36)
    input_box_voc = pygame.Rect(width//2-120, height//2+60, 240, 36)
    btn_criar = pygame.Rect(width//2-120, height//2+120, 110, 40)
    btn_voltar = pygame.Rect(width//2+10, height//2+120, 110, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_btn = pygame.Color('gray20')
    color_btn_hover = pygame.Color('gray40')
    focus = 0  # 0=email, 1=senha, 2=nome, 3=vocacao, 4=criar, 5=voltar
    email = ''
    senha = ''
    nome = ''
    vocacao = ''
    error_msg = ''
    success_msg = ''
    running = True
    created = False
    criando = False
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
                elif input_box_nome.collidepoint(event.pos):
                    focus = 2
                elif input_box_voc.collidepoint(event.pos):
                    focus = 3
                elif btn_criar.collidepoint(event.pos):
                    focus = 4
                    criando = True
                    error_msg = ''
                    success_msg = ''
                elif btn_voltar.collidepoint(event.pos):
                    running = False
                    return created  # Volta para o login
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    focus = (focus + 1) % 6
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
                        focus = 3
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        if len(nome) < 32 and event.unicode.isprintable():
                            nome += event.unicode
                elif focus == 3:
                    if event.key == pygame.K_RETURN:
                        focus = 4
                    elif event.key == pygame.K_BACKSPACE:
                        vocacao = vocacao[:-1]
                    else:
                        if len(vocacao) < 32 and event.unicode.isprintable():
                            vocacao += event.unicode
                elif focus == 4:
                    if event.key == pygame.K_RETURN:
                        criando = True
                        error_msg = ''
                        success_msg = ''
                    elif event.key == pygame.K_TAB:
                        focus = 5
                elif focus == 5:
                    if event.key == pygame.K_RETURN:
                        running = False
        # Se estiver criando conta, mostra feedback e processa request
        if criando:
            screen.fill((30,30,30))
            msg = font_small.render('Criando conta...', True, (200,200,0))
            screen.blit(msg, (width//2-msg.get_width()//2, height//2))
            pygame.display.flip()
            try:
                print(f"[DEBUG] Enviando request de criação de conta: email={email}, nome={nome}, vocacao={vocacao}")
                resp = do_create_account(stub, email, senha, nome, vocacao)
                print(f"[DEBUG] Resposta do servidor: {resp}")
                if hasattr(resp, 'success') and resp.success:
                    success_msg = 'Conta criada com sucesso!'
                    error_msg = ''
                    created = True
                    criando = False
                    running = False
                    return created
                else:
                    error_msg = getattr(resp, 'message', None) or 'Erro ao criar conta.'
                    success_msg = ''
                    print(f"[DEBUG] Falha ao criar conta: {error_msg}")
            except Exception as e:
                error_msg = f'Erro: {e}'
                success_msg = ''
                print(f"[DEBUG] Exceção ao criar conta: {e}")
            criando = False
            continue
        screen.fill((30,30,30))
        # Título
        titulo = font.render('Criar Conta', True, (0,255,255))
        screen.blit(titulo, (width//2-titulo.get_width()//2, height//2-180))
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
        # Nome do personagem
        label_nome = font_small.render('Nome do personagem:', True, (200,200,200))
        screen.blit(label_nome, (input_box_nome.x, input_box_nome.y-28))
        pygame.draw.rect(screen, color_active if focus==2 else color_inactive, input_box_nome, 2)
        txt_nome_val = font_small.render(nome, True, (255,255,255))
        screen.blit(txt_nome_val, (input_box_nome.x+5, input_box_nome.y+5))
        # Vocação
        label_voc = font_small.render('Vocação:', True, (200,200,200))
        screen.blit(label_voc, (input_box_voc.x, input_box_voc.y-28))
        pygame.draw.rect(screen, color_active if focus==3 else color_inactive, input_box_voc, 2)
        txt_voc_val = font_small.render(vocacao, True, (255,255,255))
        screen.blit(txt_voc_val, (input_box_voc.x+5, input_box_voc.y+5))
        # Botão Criar
        btn_color = color_btn_hover if btn_criar.collidepoint(mouse_pos) or focus==4 else color_btn
        pygame.draw.rect(screen, btn_color, btn_criar, border_radius=6)
        txt_criar = font_small.render('Criar', True, (255,255,255))
        screen.blit(txt_criar, (btn_criar.x+btn_criar.w//2-txt_criar.get_width()//2, btn_criar.y+8))
        # Botão Voltar
        btn_color2 = color_btn_hover if btn_voltar.collidepoint(mouse_pos) or focus==5 else color_btn
        pygame.draw.rect(screen, btn_color2, btn_voltar, border_radius=6)
        txt_voltar = font_small.render('Voltar', True, (255,255,255))
        screen.blit(txt_voltar, (btn_voltar.x+btn_voltar.w//2-txt_voltar.get_width()//2, btn_voltar.y+8))
        # Mensagem de erro/sucesso
        if error_msg:
            txt_error = font_small.render(error_msg, True, (255,80,80))
            screen.blit(txt_error, (width//2-txt_error.get_width()//2, btn_voltar.y+60))
        if success_msg:
            txt_success = font_small.render(success_msg, True, (80,255,80))
            screen.blit(txt_success, (width//2-txt_success.get_width()//2, btn_voltar.y+60))
        pygame.display.flip()
