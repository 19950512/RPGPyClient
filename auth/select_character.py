import pygame
import sys

def select_character_screen(screen, characters):
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    width, height = screen.get_size()
    selected = 0
    running = True
    while running:
        screen.fill((30,30,30))
        titulo = font.render('Selecione seu personagem', True, (0,255,255))
        screen.blit(titulo, (width//2-titulo.get_width()//2, 60))
        for idx, char in enumerate(characters):
            y = 140 + idx*60
            color = (255,255,0) if idx == selected else (200,200,200)
            nome = char.get('name', 'Sem nome')
            voc = char.get('vocation', '-')
            level = char.get('level', 1)
            label = font_small.render(f"{nome} | {voc} | Lv {level}", True, color)
            screen.blit(label, (width//2-label.get_width()//2, y))
        instr = font_small.render('Setas para navegar, Enter para selecionar', True, (180,180,180))
        screen.blit(instr, (width//2-instr.get_width()//2, height-60))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(characters)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    return characters[selected]
