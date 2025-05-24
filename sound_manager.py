# sound_manager.py
import pygame

pygame.mixer.init()

current_track = None

def play_music(path, loop=True, force=False):
    global current_track
    if force or current_track != path:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1 if loop else 0)
        current_track = path

def stop_music():
    pygame.mixer.music.stop()
    global current_track
    current_track = None
