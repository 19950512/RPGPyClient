import pygame
import sys
import grpc
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'protos'))
import game_pb2, game_pb2_grpc

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
                    return email, senha
                elif btn_criar.collidepoint(event.pos):
                    focus = 3
                    # Aqui pode chamar tela de cadastro futuramente
                    error_msg = 'Funcionalidade de cadastro ainda não implementada.'
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
                        return email, senha
                elif focus == 3:
                    if event.key == pygame.K_RETURN:
                        error_msg = 'Funcionalidade de cadastro ainda não implementada.'
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

def show_character_screen(screen, char_resp):

    """Exibe a tela de informações do personagem."""
    print("[CLIENT] Exibindo tela de informações do personagem")
    print(f"[DEBUG] Dados do personagem: {char_resp}")
    if not char_resp:
        print("[CLIENT] Nenhum dado de personagem encontrado.")
        return

    font = pygame.font.Font(None, 32)
    width, height = screen.get_size()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((20, 20, 40))
        y = 60
        screen.blit(font.render('Dados do Personagem', True, (255,255,0)), (width//2-120, 20))
        screen.blit(font.render(f'Nome: {getattr(char_resp, "player_name", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'Classe: {getattr(char_resp, "vocation_name", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'Nível: {getattr(char_resp, "level", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'HP: {getattr(char_resp, "current_hp", "-")}/{getattr(char_resp, "max_hp", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'Ataque: {getattr(char_resp, "total_attack", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'Defesa: {getattr(char_resp, "total_defense", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'XP: {getattr(char_resp, "experience", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render(f'Ouro: {getattr(char_resp, "coins", "-")}', True, (200,200,200)), (80, y))
        y += 40
        screen.blit(font.render('Pressione ENTER para continuar', True, (180,180,180)), (80, y+40))
        pygame.display.flip()

def main():
    import game_screen
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    channel = grpc.insecure_channel(os.getenv("GRPC_SERVER"))
    stub = game_pb2_grpc.GameServiceStub(channel)
    while True:
        email, senha = login_screen(screen)
        try:
            print(f"[CLIENT] Enviando login para o servidor: email={email}")
            req = game_pb2.LoginRequest(email=email, password=senha)
            resp = stub.Login(req)
            print(f"[CLIENT] Resposta do servidor: success={getattr(resp, 'success', None)}, message={getattr(resp, 'message', '')}")
            if resp.success:
                print("[CLIENT] Login bem-sucedido. Solicitando dados do personagem...")
                char_req = game_pb2.GetPlayerStatusRequest(email=email)
                char_resp = stub.GetPlayerStatus(char_req)
                print("[CLIENT] Resposta completa do servidor ao buscar status do jogador:")
                print(f"  success={getattr(char_resp, 'success', None)}")
                print(f"  message={getattr(char_resp, 'message', '')}")
                print(f"  player_name={getattr(char_resp, 'player_name', '')}")
                print(f"  vocation_name={getattr(char_resp, 'vocation_name', '')}")
                print(f"  level={getattr(char_resp, 'level', None)}")
                print(f"  current_hp={getattr(char_resp, 'current_hp', None)}")
                print(f"  max_hp={getattr(char_resp, 'max_hp', None)}")
                print(f"  total_attack={getattr(char_resp, 'total_attack', None)}")
                print(f"  total_defense={getattr(char_resp, 'total_defense', None)}")
                print(f"  experience={getattr(char_resp, 'experience', None)}")
                print(f"  coins={getattr(char_resp, 'coins', None)}")
                print(f"  inventory={getattr(char_resp, 'inventory', [])}")
                show_character_screen(screen, char_resp)
                game_screen.game_screen(screen, email, stub)
                break
            else:
                print(f"[CLIENT] Falha no login: {getattr(resp, 'message', '')}")
                font = pygame.font.Font(None, 28)
                screen.fill((30,30,30))
                err = font.render('Login ou senha inválidos.', True, (255,80,80))
                screen.blit(err, (100, 200))
                pygame.display.flip()
                pygame.time.wait(2000)
        except Exception as e:
            print(f"[CLIENT] Erro ao comunicar com o servidor: {e}")
            font = pygame.font.Font(None, 28)
            screen.fill((30,30,30))
            err = font.render(f'Erro: {e}', True, (255,80,80))
            screen.blit(err, (100, 200))
            pygame.display.flip()
            pygame.time.wait(2000)

if __name__ == "__main__":
    main()
