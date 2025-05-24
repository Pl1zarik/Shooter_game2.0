# модули
import pygame
import sys
from random import randint
from time import time as timer, perf_counter
from sound_manager import play_music

# константы
W = 800
H = 600
FPS = 60

# игровые перменные
score = 0  # сбито
lost = 0  # пропущено
patrons = 20
health = 100
finish = False
FLAG = False

# экран
main_win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Шутер")
back = pygame.transform.scale(pygame.image.load("images/sky.jpg"), (W, H))

# музыка
fire = pygame.mixer.Sound("music/laser-blast.ogg")

# шрифты
pygame.font.init()
font1 = pygame.font.SysFont("Arial", 28)
font2 = pygame.font.SysFont("Arial", 50)


# изображение здоровья
img1 = pygame.transform.scale(pygame.image.load("images/rocket_100hp.png"), (100, 120))
img2 = pygame.transform.scale(pygame.image.load("images/rocket_75hp.png"), (100, 120))
img3 = pygame.transform.scale(pygame.image.load("images/rocket_50hp.png"), (100, 120))
img4 = pygame.transform.scale(pygame.image.load("images/rocket_25hp.png"), (130, 150))


# Конструктор класса
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(player_image), (size_x, size_y)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d] and self.rect.x < W - 85:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def FIRE(self):
        global patrons
        bullet = Bullet(
            "images/bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15
        )
        bullets.add(bullet)
        patrons -= 1


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W - 80)
            lost += 1  # тут


class Sprites(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H:
            self.rect.y = 0
            self.rect.x = randint(80, W - 80)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Boss(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.speed *= -1
        else:
            self.speed *= -1

# Группы
player = None
boss = None
bullets = pygame.sprite.Group()
monsters = pygame.sprite.Group()
no_break_monsters = pygame.sprite.Group()
boosts_health = pygame.sprite.Group()
boosts_cartridges = pygame.sprite.Group()


# сброс игры
def new_start():
    global score, lost, patrons, health, player, finish, FLAG, boss

    score = 0
    lost = 0
    patrons = 20
    health = 100
    finish = False
    FLAG = False

    bullets.empty()
    monsters.empty()
    no_break_monsters.empty()
    boosts_health.empty()
    boosts_cartridges.empty()

    player = Player("images/rocket_100hp.png", W // 2, H - 130, 100, 120, 5)
    # boss = Boss("images/boss.png", W // 2, H - 130, 100, 120, 5)

    for _ in range(5):
        monster = Enemy("images/ufo.png", randint(80, W - 80), randint(-200, -50), 80, 50, randint(1, 3))
        monsters.add(monster)

    for _ in range(2):
        asteroid = Sprites(
            "images/asteroid.png", randint(80, W - 80), -40, 80, 50, randint(1, 2)
        )
        no_break_monsters.add(asteroid)

    for _ in range(1):
        health_png = Sprites(
            "images/health.png", randint(80, W - 80), -40, 80, 50, randint(1, 5)
        )
        boosts_health.add(health_png)
        patron_png = Sprites(
            "images/cartridges.png", randint(80, W - 80), -40, 80, 50, randint(1, 5)
        )
        boosts_cartridges.add(patron_png)
# def boss_go():
#     if int(start_time) - int(boss_and_speed_time) == time_boss or lost >= boss_lost:
#                 print(int(current_time-boss_and_speed_time))
#                 boss_and_speed_time = current_time
#                 sprite.Group.empty(monsters) 
#                 sprite.Group.empty(no_break_monsters)
#                 time_boss += current_time
#                 time_boss *= 1.5
#                 boss_lost += lost
#                 boss_lost *= 1.5

# отрисовка спрайтов
def draw_sprite():
    main_win.blit(back, (0, 0))
    monsters.draw(main_win)
    no_break_monsters.draw(main_win)
    boosts_health.draw(main_win)
    boosts_cartridges.draw(main_win)
    bullets.draw(main_win)
    


# движение спрайтов
def move_sprites():
    player.update()
    monsters.update()
    no_break_monsters.update()
    boosts_health.update()
    boosts_cartridges.update()
    bullets.update()
    # boss.update()


# столкновение групп
def collide_group():
    global score, health, patrons
    for f in pygame.sprite.groupcollide(bullets, monsters, True, True):
        score += 1
        monster = Enemy(
            "images/ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 2)
        )
        monsters.add(monster)

    pygame.sprite.groupcollide(bullets, no_break_monsters, True, False)

    for asteroid in pygame.sprite.spritecollide(player, no_break_monsters, True):
        asteroid = Enemy(
            "images/asteroid.png", randint(80, W - 80), -40, 80, 50, randint(1, 2)
        )
        no_break_monsters.add(asteroid)
        health -= 50

    for boost in pygame.sprite.spritecollide(player, boosts_health, True):
        health_png = Sprites("images/health.png", randint(80, W - 80), -40, 80, 50, 1)
        boosts_health.add(health_png)
        health += 20

    for cartridge in pygame.sprite.spritecollide(player, boosts_cartridges, True):
        patron_png = Sprites(
            "images/cartridges.png", randint(80, W - 80), -40, 80, 50, randint(1, 5)
        )
        boosts_cartridges.add(patron_png)
        patrons += 5

    for _ in pygame.sprite.spritecollide(player, monsters, True):
        monster = Enemy(
            "images/ufo.png", randint(80, W - 80), -40, 80, 50, randint(1, 2)
        )
        monsters.add(monster)
        health -= 25


# текст
def texts():
    text_score = font1.render(f"Счёт: {score}", True, (255, 255, 255))
    text_lost = font1.render(f"Пропущено: {lost}", True, (255, 255, 255))
    text_hp = font1.render(f"Здоровье: {health}", True, (255, 255, 255))
    text_cartridges = font1.render(f"{patrons}/20", True, (255, 255, 255))

    main_win.blit(text_score, (10, 20))
    main_win.blit(text_lost, (10, 50))
    main_win.blit(text_hp, (10, 80))
    main_win.blit(text_cartridges, (10, 110))


def ifs():
    global health, patrons
    if health > 100:
        health = 100
    if patrons > 20:
        patrons = 20
    if patrons < 0:
        patrons = 0
    if health < 0:
        health = 0

    if health > 75:
        player.image = img1
    elif health > 50:
        player.image = img2
    elif health > 25:
        player.image = img3
    else:
        player.image = img4


def game():
    global FLAG, finish, health

    play_music("music/space.ogg")
    finish = False
    clock = pygame.time.Clock()

    start_time = perf_counter()
    last_shot = timer()
    while not finish:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return  # для выхода

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if patrons > 0 and timer() - last_shot > 0.5:
                    fire.play()
                    player.FIRE()
                    last_shot = timer()



        main_win.blit(back, (0, 0))
        draw_sprite()
        player.reset()
        # boss.reset()
        move_sprites()
        collide_group()
        ifs()
        texts()

        if health <= 0:
            lose_text = font2.render("Ты проиграл, нажмите r для рестарта", True, (139, 0, 0))
            main_win.blit(lose_text, (W // 2 - 350, H // 2 - 30))
            pygame.display.update()

            # задержка перед выходом
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r and wait:
                        new_start()
                        wait = False
                clock.tick(FPS)
            # return
        pygame.display.update()
        clock.tick(FPS)
       