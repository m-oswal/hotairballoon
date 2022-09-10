import pygame, sys, random, os
import mysql.connector as msc
import menu

pygame.init()

width, height = 700,1000
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption('hot air balloon')

# game mechanics
score = 0
gravity = 3.5
accelerate = pygame.USEREVENT + 1
survive = pygame.USEREVENT + 2

# game designs
balloon = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'hotballoon.png')), (100, 100))
coin = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'coin.png')), (30, 30))
back = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'back.png')), (50, 50))
# game colours
bg = (255, 255, 245)
# game texts
score_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 40)
game_over_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 100)
game_score_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 75)


def draw(task, line, point, menu_rect):
    pygame.draw.rect(WIN, bg, pygame.Rect(0, 0, 1200, 1000))

    saber = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'saber.png')), (line.width, 30))
    stext = score_font.render(str(score), 1, (0, 0, 0))
    # user character
    WIN.blit(balloon, (task.x - 15, task.y))
    # point
    WIN.blit(coin, (point.x, point.y))
    # obstacle
    WIN.blit(saber, (line.x, line.y))
    # score
    WIN.blit(stext, (25, 15))
    WIN.blit(back, (menu_rect.x, menu_rect.y))
    pygame.display.update()


def game_over():
    pygame.draw.rect(WIN, (255, 255, 245), pygame.Rect(0, 0, 1200, 1000))
    gotext = game_over_font.render('GAME OVER', 1, (255, 0, 0))
    stext = game_score_font.render('SCORE :' + str(score), 1, (0, 0, 0))
    s_rect = stext.get_rect(center=(width // 2, height // 2))

    WIN.blit(gotext, (20, 150))
    WIN.blit(stext, s_rect)
    pygame.display.update()
    pygame.time.delay(2500)


def main():
    global score, gravity, accelerate
    clock = pygame.time.Clock()
    run = True
    # character position
    mx = width // 2
    # obstacle position
    lx = random.randint(0, width - 100)
    ly = -30
    # points position
    px = random.randint(100, width - 30)
    py = 0
    # obstacle size
    sizex = random.randint(150, 250)
    active = False
    # level increment timer
    pygame.time.set_timer(accelerate, 1000)
    # survival time to point timer
    pygame.time.set_timer(survive, 200)
    menu_rect = pygame.Rect(width - 50, 0, 50, 50)

    while run:
        clock.tick(120)
        # to keep user object inside the frame
        if mx >= 36 and mx <= width - 36:
            task = pygame.Rect(mx - 36, 500, 72, 100)
        elif mx > 0:
            mx = 0
        elif mx < width - 100:
            mx = width
        # obstacle and points rect
        line = pygame.Rect(lx, ly, sizex, 30)
        point = pygame.Rect(px, py, 30, 30)
        # to activate on click

        if active:
            mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == accelerate and active:
                gravity += 0.1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(pygame.mouse.get_pos()) and not active:

                    menu.menu_main()
                else:
                    active = True
            if event.type == survive and active:
                score += 1

        # to add points
        if point.colliderect(task):
            score += 20

            px = random.randint(100, width - 30)
            py = 0

        # to add gravity to obstacle
        if ly < 980 and active:
            ly += gravity
        if ly >= 980:
            ly = 0
            sizex = random.randint(150, 300)
            lx = random.randint(0, width - 100)
        # to add gravity to coins
        if py <= 980 and active:
            py += gravity
        if py >= 980:
            py = 0
            px = random.randint(100, width - 30)

        # game over
        if line.colliderect(task):
            run = False

            db = msc.connect(host='localhost',
                             user='root',
                             password='your_username',
                             database='your_password')
            cursor = db.cursor()
            cursor.execute('select * from log;')
            rec = cursor.fetchall()
            if len(rec) > 0:
                username = rec[0][0]
            else:
                username = 'guest'

            cursor.execute(f'UPDATE PLAYERS SET SCORE = {score} WHERE USERNAME = "{username}" AND SCORE < {score};')
            db.commit()
            db.close()


            pygame.time.delay(500)
            game_over()
            gravity = 3.5
            score = 0

        draw(task, line, point, menu_rect)
    main()


if __name__ == '__main__':
    main()
