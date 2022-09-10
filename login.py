import pygame, os, sys, menu
import mysql.connector as msc

pygame.init()
width, height = 700,1000
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('hot air balloon')
rec_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 40)
log_font = pygame.font.Font(os.path.join('assets', 'retro.ttf'), 60)
back = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'back.png')), (50, 50))
box = (209, 243, 197)
box_width = 575


def draw(user_rect, passw_rect, login_rect, user_box, passw_box, username, password, menu_rect):
    global box
    pygame.draw.rect(window, (255, 255, 245), pygame.Rect(0, 0, 1200, 1000))
    name = passw = box
    if user_box:
        name = (0, 0, 0)
    elif passw_box:
        passw = (0, 0, 0)

    pygame.draw.rect(window, name, user_rect, 4, 3)
    pygame.draw.rect(window, passw, passw_rect, 4, 3)
    pygame.draw.rect(window, box, login_rect, 0, 4)

    username_text = rec_font.render(username, 1, (0, 0, 0))
    window.blit(username_text, (63, 250))

    password_text = rec_font.render(password, 1, (0, 0, 0))
    window.blit(password_text, (63, 400))

    login_text = rec_font.render('LOGIN', 1, (0, 0, 0))
    window.blit(login_text, (275, 610))

    window.blit(back, (menu_rect.x, menu_rect.y))
    pygame.display.update()


def draw_logged_in(login_rect, menu_rect):
    global box
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute(f'select *  from log;')
    log_record = cursor.fetchall()
    db.close()

    pygame.draw.rect(window, (255, 255, 245), pygame.Rect(0, 0, 1200, 1000))
    pygame.draw.rect(window, (209, 243, 197), login_rect, 0, 4)

    login_text = rec_font.render('LOGOUT', 1, (0, 0, 0))
    window.blit(login_text, (265, 610))

    account_text = log_font.render(f'{log_record[0][0]} LOGGED IN', 1, (0, 0, 0))
    account_rec = account_text.get_rect(center=(width // 2, 300))
    window.blit(account_text, account_rec)

    window.blit(back, (menu_rect.x, menu_rect.y))

    pygame.time.delay(500)
    pygame.display.update()


def login_verify(username, password):
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute(f'SELECT PASSWORD FROM PLAYERS WHERE USERNAME = "{username}";')
    rec = cursor.fetchall()
    db.close()
    if len(rec) == 0:
        print('no such username')
    else:
        if rec[0][0] == password:
            print('valid')
            return True
        else:
            print('invalid')


def user_log(username):
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute(f'insert into log values("{username}");')
    db.commit()
    db.close()


def logged_in():
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute(f'select *  from log;')
    log_record = cursor.fetchall()
    db.close()
    if len(log_record) > 0:
        return True
    else:
        return False



def logged_out():
    db = msc.connect(host='localhost',
                     user='your_user_name',
                     password='your_password',
                     database='hotairballoon')
    cursor = db.cursor()
    cursor.execute('delete from log')
    db.commit()
    db.close()


def main():
    global box
    run = True
    user_rect = pygame.Rect((width - box_width) // 2, 250, box_width, 75)
    passw_rect = pygame.Rect((width - box_width) // 2, 400, box_width, 75)
    login_rect = pygame.Rect(200, 600, 300, 75)
    menu_rect = pygame.Rect(width - 50, 0, 50, 50)

    user_box = False
    passw_box = False

    username = ''
    password = ''

    while run:
        mx, my = pygame.mouse.get_pos()

        if not logged_in():

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_rect.collidepoint(mx, my) or passw_rect.collidepoint(mx, my):
                        if user_rect.collidepoint(mx, my):
                            user_box = True
                            passw_box = False
                        if passw_rect.collidepoint(mx, my):
                            passw_box = True
                            user_box = False

                    else:

                        user_box = False
                        passw_box = False

                    if login_rect.collidepoint(mx, my):
                        if login_verify(username, password):
                            user_log(username)
                        else:
                            main()
                    if menu_rect.collidepoint(mx, my):
                        menu.menu_main()

                if event.type == pygame.KEYDOWN:
                    if user_box:
                        if event.key != pygame.K_BACKSPACE:  # backspace
                            username += event.unicode
                        else:
                            username = username[:-1]

                    if passw_box:
                        if event.key != pygame.K_BACKSPACE:  # backspace
                            password += event.unicode
                        else:
                            password = password[:-1]
            draw(user_rect, passw_rect, login_rect, user_box, passw_box, username, password, menu_rect)

        else:  # LOGGED IN ALREADY
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if login_rect.collidepoint(mx, my):
                        logged_out()
                        main()
                    if menu_rect.collidepoint(mx, my):
                        menu.menu_main()

            draw_logged_in(login_rect, menu_rect)


if __name__ == '__main__':
    main()
