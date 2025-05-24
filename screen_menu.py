from s_game import game, new_start
from about import about
import pygame
import sys
from sound_manager import play_music

# иниты
pygame.init()
pygame.font.init()


# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FPS = 60

# музыка меню
play_music("music/menu_music.ogg", force=True)

# дисплей и название
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Шутер")

# класс
class Object:
    def __init__(self, object_image, object_x, object_y, size_x, size_y):
        self.image = pygame.transform.scale(pygame.image.load(object_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = object_x
        self.rect.y = object_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))



def draw_text(text, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# интерфейсные элементы
button_play = Object("images/button_play.png", WIDTH / 2 - 70, HEIGHT / 2 + 150, 140, 60)
button_about = Object("images/button_about.png", WIDTH / 2 - 70, HEIGHT / 2 + 209, 140, 60)
back = pygame.transform.scale(pygame.image.load("images/back_menu.jpg"), (WIDTH, HEIGHT))

# цикл меню
clock = pygame.time.Clock()
screen_flag = True

while screen_flag:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # кнопка играть
            if pygame.Rect(WIDTH / 2 - 70, HEIGHT / 2 +150, 140, 60).collidepoint((mouse_x, mouse_y)):
                pygame.mixer.music.stop()
                new_start()
                game()
                play_music("music/menu_music.ogg", force=True)
            
            # кнопка о игре
            if pygame.Rect(WIDTH / 2 - 70, HEIGHT / 2 + 210, 140, 60).collidepoint((mouse_x, mouse_y)):
                about()


    screen.blit(back, (0, 0))
    draw_text("Добро пожаловать!", 40, WIDTH / 2, HEIGHT / 4)

    button_play.reset()
    button_about.reset()
    draw_text("Play", 30, WIDTH / 2, HEIGHT / 2 + 175)
    draw_text("About", 30, WIDTH / 2, HEIGHT / 2 + 235)


    pygame.display.flip()
    clock.tick(FPS)
