import pygame, sys, os
import mysql.connector as msc
import menu

pygame.init()
width, height = 700,1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('hot air balloon')
rank_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 40)
leader_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 75)
back = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'back.png')), (50, 50))


def draw_leader(record, menu_rect):
    pygame.draw.rect(window, (255, 255, 245), pygame.Rect(0, 0, 1200, 1000))

    window.blit(back, (menu_rect.x, menu_rect.y))
    y = 300
    leader_text = leader_font.render('LEADERBOARD', 1, (0, 0, 0))

    window.blit(leader_text, (37, 100))
    for i in record:
        username, score = i
        user_text = rank_font.render(str(username), 1, (0, 0, 0))
        score_text = rank_font.render(str(score), 1, (0, 0, 0))
        window.blit(user_text, (80, y))
        window.blit(score_text, (450, y))
        y += 70
    pygame.display.update()


def leaderboard_main():
    run = True
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute('SELECT USERNAME,SCORE FROM PLAYERS WHERE NOT USERNAME="GUEST" ORDER BY SCORE DESC LIMIT 5 ')

    record = cursor.fetchall()
    db.commit()
    db.close()
    menu_rect = pygame.Rect(width - 50, 0, 50, 50)
    while run:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if menu_rect.collidepoint(x, y) and event.type == pygame.MOUSEBUTTONDOWN:
                menu.menu_main()

        draw_leader(record, menu_rect)


if __name__ == '__main__':
    leaderboard_main()
