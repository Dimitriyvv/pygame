import sys

import pygame
import random
import pygame_widgets as pw
from threading import Timer
# from Button import ImageButton

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Падающие ящики")
background = [pygame.image.load('animations/background.jpg'), pygame.image.load('animations/fon1.png'),
              pygame.image.load('animations/fon2.png'), pygame.image.load('animations/fon3.png')]
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
hero_image = pygame.image.load("animations/pers.jpg")
box = [pygame.image.load("animations/box.png"), pygame.image.load("animations/ironbox.png"),
       pygame.image.load("animations/ironbox2.png"), pygame.image.load("animations/woodbox1.png")]

# Позиция, размеры игрока и значения разблокировки скинов
player_size_x = 50
player_size_y = 70
player_x = WIDTH // 2 - player_size_x // 2
player_y = HEIGHT - player_size_y
time = 0
savepoint = ()
background_skin = 0
box_skin = 0
unblock1, unblock2, unblock3, unblock4, unblock5, unblock6 = 0, 0, 0, 0, 0, 0

# переменные анимации персонажа при движении
hero_goto_left = [pygame.image.load('animations/pers_left0.png'), pygame.image.load('animations/pers_left1.png'),
                  pygame.image.load('animations/pers_left2.png'), pygame.image.load('animations/pers_left3.png'),
                  pygame.image.load('animations/pers_left4.png'), pygame.image.load('animations/pers_left5.png'),
                  pygame.image.load('animations/pers_left6.png'), pygame.image.load('animations/pers_left7.png')]
hero_goto_right = [pygame.image.load('animations/pers_right0.png'), pygame.image.load('animations/pers_right1.png'),
                   pygame.image.load('animations/pers_right2.png'), pygame.image.load('animations/pers_right3.png'),
                   pygame.image.load('animations/pers_right4.png'), pygame.image.load('animations/pers_right5.png'),
                   pygame.image.load('animations/pers_right6.png'), pygame.image.load('animations/pers_right7.png')]
hero_goto_num_left = 0
hero_goto_num_right = 0


class ImageButton:
    def __init__(self, x, y, width, height, image_path, hover_image_path, sound_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = pygame.image.load(hover_image_path)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, window):
        current_image = self.hover_image if self.is_hovered else self.image
        window.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


# реализация кнопок в игре через сторонний класс для создания кнопок для пайгейма
regame_button = ImageButton((WIDTH / 2 - (140 / 2)), 100, 140, 60, "buttons/regame.png",
                            "buttons/regame1.png", "audio/click.mp3")
shop_button = ImageButton((WIDTH / 2 - (140 / 2)), 200, 140, 60, "buttons/shop.png",
                          "buttons/shop1.png", "audio/click.mp3")
quit_button = ImageButton((WIDTH / 2 - (140 / 2)), 300, 140, 60, "buttons/quit.png",
                          "buttons/quit1.png", "audio/click.mp3")
game_button = ImageButton((WIDTH / 2 - (140 / 2)), 100, 140, 60, "buttons/game.png",
                          "buttons/game1.png", "audio/click.mp3")
back_button = ImageButton(0, 0, 140, 60, "buttons/back.png",
                          "buttons/back1.png", "audio/click.mp3")
box_button = ImageButton(0, 70, 140, 60, "buttons/box_shop.png",
                         "buttons/box_shop1.png", "audio/click.mp3")
fons_button = ImageButton(0, 140, 140, 60, "buttons/fons_shop.png",
                          "buttons/fons_shop1.png", "audio/click.mp3")
standart_fon = ImageButton(200, 100, 140, 100, "animations/background.jpg",
                           "animations/background.jpg", "audio/click.mp3")
chose_button_fon = ImageButton(500, 100, 140, 100, "animations/fon1.png",
                               "animations/fon1.png", "audio/click.mp3")
chose_button_fon2 = ImageButton(200, 325, 140, 100, "animations/fon2.png",
                                "animations/fon2.png", "audio/click.mp3")
chose_button_fon3 = ImageButton(500, 325, 140, 100, "animations/fon3.png",
                                "animations/fon3.png", "audio/click.mp3")
standart_box = ImageButton(200, 100, 100, 100, "animations/box.png",
                           "animations/box.png", "audio/click.mp3")
chose_button_box = ImageButton(500, 100, 100, 100, "animations/ironbox.png",
                               "animations/ironbox.png", "audio/click.mp3")
chose_button_box2 = ImageButton(200, 325, 100, 100, "animations/ironbox2.png",
                                "animations/ironbox2.png", "audio/click.mp3")
chose_button_box3 = ImageButton(500, 325, 100, 100, "animations/woodbox1.png",
                                "animations/woodbox1.png", "audio/click.mp3")
buy1 = ImageButton(520, 220, 100, 60, "buttons/buy.png",
                   "buttons/cost1.png", "audio/click.mp3")
buy2 = ImageButton(220, 445, 100, 60, "buttons/buy.png",
                   "buttons/cost2.png", "audio/click.mp3")
buy3 = ImageButton(520, 445, 100, 60, "buttons/buy.png",
                   "buttons/cost3.png", "audio/click.mp3")
buying = ImageButton(220, 220, 100, 60, "buttons/buying.png",
                     "buttons/buying.png", "audio/click.mp3")


# класс для упрощённого контроля за переменными
class score_controller:
    def __init__(self, value):
        self.balance = value

    def add(self, value):
        self.balance = self.balance + value
        return self.balance

    def remove(self, value):
        self.balance = self.balance - value
        return self.balance

    def set(self, value):
        self.balance = value
        return self.balance

    def get(self):
        return self.balance


# чтение переменных из внешнего текстового файла
with open(r'record.txt', 'r') as f:
    (highscore, balance, background_skin, box_skin, unblock1, unblock2,
     unblock3, unblock4, unblock5, unblock6) = f.read().split(", ")
    highscore = score_controller(int(highscore))
    balance = score_controller(int(balance))
    background_skin = int(background_skin)
    box_skin = int(box_skin)
    (unblock1, unblock2, unblock3, unblock4, unblock5, unblock6) = (int(unblock1), int(unblock2), int(unblock3),
                                                                    int(unblock4), int(unblock5), int(unblock6))
    f.close()

# Скорость игрока
player_speed = 5

# Создание препятствий, определение их скорости и размеров
obstacle_size = 50
obstacle_x = random.randint(0, WIDTH - obstacle_size)
obstacle_y = -obstacle_size
obstacle_speed = 3
running = True

# Очки игрока
score = score_controller(0)
# шрифт текста внутри игры
font = pygame.font.Font(None, 36)


# функция рестарта(откат счёта, таймера и скорости объектов до стартового)
def reset_game():
    global time, obstacle_speed, player_speed
    score.set(0)
    time = 0
    obstacle_speed = 3
    player_speed = 5


# функция рестарта игры при проигрыше
def restart():
    global obstacle_x, obstacle_y, running, player_x
    obstacle_x = random.randint(0, WIDTH - obstacle_size)
    player_x = WIDTH // 2
    obstacle_y = -obstacle_size
    reset_game()
    game()


# Функция для обновления дисплея, и анимации персонажа
def update_display(events):
    screen.blit(background[background_skin], (0, 0))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        screen.blit(hero_goto_left[int(hero_goto_num_left)], (player_x - 5, player_y))
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        screen.blit(hero_goto_right[int(hero_goto_num_right)], (player_x - 5, player_y))
    else:
        screen.blit(hero_image, (player_x, player_y))
    screen.blit(box[box_skin], (obstacle_x, obstacle_y))
    score_text = font.render("Очки: " + str(score.get()), True, WHITE)
    time_text = font.render("Время: " + str(time // 60) + ':' + str(time % 60), True, WHITE)
    value_text = font.render("Деньги: " + str(balance.get()), True, WHITE)
    highscore_text = font.render("Рекорд: " + str(highscore.get()), True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (600, 10))
    screen.blit(highscore_text, (300, 10))
    screen.blit(value_text, (10, 40))
    if running:
        pw.update(events)
    pygame.display.update()


# функция подсчёта внутри игрового времени
def timer():
    global time
    if running:
        time += 1
    Timer(1, timer).start()


# функция ускорения препятствий от времени
def yskorenie():
    global obstacle_speed
    if obstacle_speed < 15:
        if 3 <= obstacle_speed <= 6:
            obstacle_speed += 0.6
        elif 6 <= obstacle_speed <= 10:
            obstacle_speed += 0.4
        elif 10 <= obstacle_speed <= 15:
            obstacle_speed += 0.3


timer()

clock = pygame.time.Clock()


# Основной игровой цикл
def game():
    global running, player_x, hero_goto_num_left, hero_goto_num_right, obstacle_y, obstacle_x, main_menu, value_text
    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    running = not running

        keys = pygame.key.get_pressed()
        if running:
            next_player_x = player_x
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                next_player_x = player_x - player_speed
                hero_goto_num_left += 0.2
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                next_player_x = player_x + player_speed
                hero_goto_num_right += 0.2
            else:
                hero_goto_num_left += 0
                hero_goto_num_right += 0

            if hero_goto_num_left > 7:
                hero_goto_num_left = 0
            if hero_goto_num_right > 7:
                hero_goto_num_right = 0

            obstacle_y += obstacle_speed

            if 0 <= next_player_x <= (WIDTH - player_size_x):
                player_x = next_player_x

            if obstacle_y > HEIGHT:
                if random.randint(0, 6) == 5:
                    obstacle_x = player_x
                else:
                    obstacle_x = random.randint(0, WIDTH - obstacle_size)
                obstacle_y = -obstacle_size
                score.add(1)
                yskorenie()
                if score.get() % 5 == 0:
                    balance.add(1)

            if (obstacle_x < player_x + player_size_x and obstacle_x + obstacle_size > player_x
                    and obstacle_y < player_y + player_size_y and obstacle_y + obstacle_size > player_y):
                boom = pygame.mixer.Sound("audio/boom.mp3")
                boom.play()
                fon = pygame.image.load("animations/gameover.gif")
                screen.blit(fon, (0, 0))
                main_menu()

        # функция вызова главного меню
        def main_menu():
            global running
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == regame_button:
                        restart()
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            sys.exit()

                    if event.type == pygame.USEREVENT and event.button == shop_button:
                        shop()

                    if event.type == pygame.USEREVENT and event.button == quit_button:
                        pygame.quit()
                        sys.exit()

                    regame_button.handle_event(event)
                    shop_button.handle_event(event)
                    quit_button.handle_event(event)

                regame_button.check_hover(pygame.mouse.get_pos())
                shop_button.check_hover(pygame.mouse.get_pos())
                quit_button.check_hover(pygame.mouse.get_pos())
                regame_button.draw(screen)
                shop_button.draw(screen)
                quit_button.draw(screen)
                pygame.display.flip()

        # функция вызова магазина
        def shop():
            global running, background_skin, balance, value_text, unblock1, unblock2, unblock3
            while running:
                value_text = font.render("Деньги: " + str(balance.get()), True, WHITE)
                fon = pygame.image.load("animations/shop_fon.png")
                screen.blit(fon, (0, 0))
                screen.blit(value_text, (300, 10))
                text = font.render("Для выбора купленного скина нажмите на его картинку", True, WHITE)
                screen.blit(text, (10, 550))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon and unblock1 == 1:
                        background_skin = 1

                    if event.type == pygame.USEREVENT and event.button == standart_fon:
                        background_skin = 0

                    if event.type == pygame.USEREVENT and event.button == box_button:
                        box_shop()

                    if event.type == pygame.USEREVENT and event.button == fons_button:
                        fons_shop()

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon2 and unblock2 == 1:
                        background_skin = 2

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon3 and unblock3 == 1:
                        background_skin = 3

                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            sys.exit()

                    if event.type == pygame.USEREVENT and event.button == buy1:
                        if balance.get() >= 100 and unblock1 == 0:
                            balance.add(-100)
                            unblock1 = 1

                    if event.type == pygame.USEREVENT and event.button == buy2:
                        if balance.get() >= 250 and unblock2 == 0:
                            balance.add(-250)
                            unblock2 = 1

                    if event.type == pygame.USEREVENT and event.button == buy3:
                        if balance.get() >= 500 and unblock3 == 0:
                            balance.add(-500)
                            unblock3 = 1

                    if event.type == pygame.USEREVENT and event.button == quit_button:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == back_button:
                        fon = pygame.image.load("animations/gameover.gif")
                        screen.blit(fon, (0, 0))
                        main_menu()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    back_button.handle_event(event)
                    box_button.handle_event(event)
                    fons_button.handle_event(event)
                    chose_button_fon.handle_event(event)
                    chose_button_fon2.handle_event(event)
                    chose_button_fon3.handle_event(event)
                    standart_fon.handle_event(event)
                    buy1.handle_event(event)
                    buy2.handle_event(event)
                    buy3.handle_event(event)
                    buying.handle_event(event)

                back_button.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                chose_button_fon.check_hover(pygame.mouse.get_pos())
                chose_button_fon2.check_hover(pygame.mouse.get_pos())
                chose_button_fon3.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                standart_fon.check_hover(pygame.mouse.get_pos())
                buy1.check_hover(pygame.mouse.get_pos())
                buy2.check_hover(pygame.mouse.get_pos())
                buy3.check_hover(pygame.mouse.get_pos())
                buying.check_hover(pygame.mouse.get_pos())
                buy1.draw(screen)
                buy2.draw(screen)
                buy3.draw(screen)
                buying.draw(screen)
                standart_fon.draw(screen)
                fons_button.draw(screen)
                box_button.draw(screen)
                chose_button_fon.draw(screen)
                chose_button_fon2.draw(screen)
                chose_button_fon3.draw(screen)
                back_button.draw(screen)
                pygame.display.flip()

        # функция вызова магазина скинов на ящики
        def box_shop():
            global running, box_skin, value_text, unblock4, unblock5, unblock6
            while running:
                value_text = font.render("Деньги: " + str(balance.get()), True, WHITE)
                fon = pygame.image.load("animations/shop_fon.png")
                screen.blit(fon, (0, 0))
                screen.blit(value_text, (300, 10))
                text = font.render("Для выбора купленного скина нажмите на его картинку", True, WHITE)
                screen.blit(text, (10, 550))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == chose_button_box and unblock4 == 1:
                        box_skin = 1

                    if event.type == pygame.USEREVENT and event.button == standart_box:
                        box_skin = 0

                    if event.type == pygame.USEREVENT and event.button == box_button:
                        box_shop()

                    if event.type == pygame.USEREVENT and event.button == fons_button:
                        fons_shop()

                    if event.type == pygame.USEREVENT and event.button == chose_button_box2 and unblock5 == 1:
                        box_skin = 2

                    if event.type == pygame.USEREVENT and event.button == chose_button_box3 and unblock6 == 1:
                        box_skin = 3

                    if event.type == pygame.USEREVENT and event.button == back_button:
                        fon = pygame.image.load("animations/gameover.gif")
                        screen.blit(fon, (0, 0))
                        main_menu()

                    if event.type == pygame.USEREVENT and event.button == back_button:
                        fon = pygame.image.load("animations/gameover.gif")
                        screen.blit(fon, (0, 0))
                        main_menu()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    if event.type == pygame.USEREVENT and event.button == buy1:
                        if balance.get() >= 100 and unblock4 == 0:
                            balance.add(-100)
                            unblock4 = 1

                    if event.type == pygame.USEREVENT and event.button == buy2:
                        if balance.get() >= 250 and unblock6 == 0:
                            balance.add(-250)
                            unblock5 = 1

                    if event.type == pygame.USEREVENT and event.button == buy3:
                        if balance.get() >= 500 and unblock6 == 0:
                            balance.add(-500)
                            unblock6 = 1

                    back_button.handle_event(event), box_button.handle_event(event)

                    fons_button.handle_event(event)
                    chose_button_box.handle_event(event)
                    chose_button_box2.handle_event(event)
                    chose_button_box3.handle_event(event)
                    standart_box.handle_event(event)
                    buy1.handle_event(event)
                    buy2.handle_event(event)
                    buy3.handle_event(event)
                    buying.handle_event(event)

                back_button.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                chose_button_box.check_hover(pygame.mouse.get_pos())
                chose_button_box2.check_hover(pygame.mouse.get_pos())
                chose_button_box3.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                standart_box.check_hover(pygame.mouse.get_pos())
                buy1.check_hover(pygame.mouse.get_pos())
                buy2.check_hover(pygame.mouse.get_pos())
                buy3.check_hover(pygame.mouse.get_pos())
                buying.check_hover(pygame.mouse.get_pos())
                buy1.draw(screen)
                buy2.draw(screen)
                buy3.draw(screen)
                buying.draw(screen)
                standart_box.draw(screen)
                box_button.draw(screen)
                fons_button.draw(screen)
                chose_button_box.draw(screen)
                chose_button_box2.draw(screen)
                chose_button_box3.draw(screen)
                back_button.draw(screen)
                pygame.display.flip()

        # функция вызова магазина скинов на игровой фон
        def fons_shop():
            global running, background_skin, unblock1, unblock2, unblock3, value_text
            while running:
                value_text = font.render("Деньги: " + str(balance.get()), True, WHITE)
                fon = pygame.image.load("animations/shop_fon.png")
                screen.blit(fon, (0, 0))
                screen.blit(value_text, (300, 10))
                text = font.render("Для выбора купленного скина нажмите на его картинку", True, WHITE)
                screen.blit(text, (10, 550))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon and unblock1 == 1:
                        background_skin = 1

                    if event.type == pygame.USEREVENT and event.button == box_button:
                        box_shop()

                    if event.type == pygame.USEREVENT and event.button == fons_button:
                        fons_shop()

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon2 and unblock2 == 1:
                        background_skin = 2

                    if event.type == pygame.USEREVENT and event.button == chose_button_fon3 and unblock3 == 1:
                        background_skin = 3

                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            sys.exit()

                    if event.type == pygame.USEREVENT and event.button == quit_button:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT and event.button == back_button:
                        fon = pygame.image.load("animations/gameover.gif")
                        screen.blit(fon, (0, 0))
                        main_menu()
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    if event.type == pygame.USEREVENT and event.button == buy1:
                        if balance.get() >= 100 and unblock1 == 0:
                            balance.add(-100)
                            unblock1 = 1

                    if event.type == pygame.USEREVENT and event.button == buy2:
                        if balance.get() >= 250 and unblock2 == 0:
                            balance.add(-250)
                            unblock2 = 1

                    if event.type == pygame.USEREVENT and event.button == buy3:
                        if balance.get() >= 500 and unblock3 == 0:
                            balance.add(-500)
                            unblock3 = 1

                    back_button.handle_event(event)
                    box_button.handle_event(event)
                    fons_button.handle_event(event)
                    chose_button_fon.handle_event(event)
                    chose_button_fon2.handle_event(event)
                    chose_button_fon3.handle_event(event)
                    standart_fon.handle_event(event)
                    buy1.handle_event(event)
                    buy2.handle_event(event)
                    buy3.handle_event(event)
                    buying.handle_event(event)

                back_button.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                chose_button_fon.check_hover(pygame.mouse.get_pos())
                chose_button_fon2.check_hover(pygame.mouse.get_pos())
                chose_button_fon3.check_hover(pygame.mouse.get_pos())
                box_button.check_hover(pygame.mouse.get_pos())
                fons_button.check_hover(pygame.mouse.get_pos())
                standart_fon.check_hover(pygame.mouse.get_pos())
                buy1.check_hover(pygame.mouse.get_pos())
                buy2.check_hover(pygame.mouse.get_pos())
                buy3.check_hover(pygame.mouse.get_pos())
                buying.check_hover(pygame.mouse.get_pos())
                buy1.draw(screen)
                buy2.draw(screen)
                buy3.draw(screen)
                buying.draw(screen)
                standart_fon.draw(screen)
                fons_button.draw(screen)
                box_button.draw(screen)
                chose_button_fon.draw(screen)
                chose_button_fon2.draw(screen)
                chose_button_fon3.draw(screen)
                back_button.draw(screen)
                pygame.display.flip()

        if score.get() > highscore.get():
            highscore.set(score.get())

        pygame.display.flip()

        update_display(events)
        clock.tick(60)

        # сохранение переменных во внешний текстовый файл
        with open(r'record.txt', 'w') as f:
            savepoint = (highscore.get(), balance.get(), background_skin, box_skin, unblock1, unblock2,
                         unblock3, unblock4, unblock5, unblock6)
            f.write(str(savepoint)[1:-1:])
            f.close()


# функция вызова стартового меню
def start_menu():
    global running
    while running:
        fon = pygame.image.load("animations/fon.png")
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == game_button:
                game()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            game_button.handle_event(event)
            quit_button.handle_event(event)

        game_button.check_hover(pygame.mouse.get_pos())
        quit_button.check_hover(pygame.mouse.get_pos())
        game_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()


start_menu()

pygame.quit()
