import pygame, sys, os, game, login
import leaderboard

pygame.init()
width, height = 700,1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('hot air balloon')
bg = (255, 255, 245)
black = (0, 0, 0)
start_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 70)
balloon = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'hotballoon.png')), (100, 100))


def draw_menu(my):
    pygame.draw.rect(window, bg, pygame.Rect(0, 0, 700, 1000))
    window.blit(balloon, (300, my))
    text = start_font.render('START', 1, black)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    leader = start_font.render('LEADERBOARD', 1, black)
    lead_rect = leader.get_rect(center=(width // 2, height // 2 + 150))
    login = start_font.render('LOGIN', 1, black)
    login_rec = login.get_rect(center=(width // 2, height // 2 + 300))

    window.blit(text, text_rect)
    window.blit(leader, lead_rect)
    window.blit(login, login_rec)

    pygame.display.update()


def move(my, up, down):
    if my > 100 and down:
        my += 1
    if my < 250 and up:
        my -= 1
    if my == 100:
        my += 1
        down = True
        up = False
    if my == 250:
        my -= 1
        up = True
        down = False
    return my, up, down


def menu_main():
    run = True
    clock = pygame.time.Clock()
    start = pygame.Rect(225, 445, 270, 90)
    lead = pygame.Rect(0, 0, 587, 90)
    login_box = pygame.Rect(0, 0, 255, 90)
    login_box.center = (width // 2, height // 2 + 300)
    lead.center = (width // 2, height // 2 + 150)

    my = 100
    up = False
    down = True
    while run:
        clock.tick(120)
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.collidepoint(x, y):
                    game.main()
                if lead.collidepoint(x, y):
                    leaderboard.leaderboard_main()
                if login_box.collidepoint(x, y):
                    login.main()

        my, up, down = move(my, up, down)
        draw_menu(my)


if __name__ == '__main__':
    menu_main()
