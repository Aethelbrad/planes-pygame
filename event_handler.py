# event_handler.py
import pygame
from bullet import Bullet
from constants import SHOOT_DELAY

class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def handle_shooting(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.game.last_shot_time > SHOOT_DELAY:
            bullet = Bullet(self.game.player.rect.centerx, self.game.player.rect.top, self.game.asset_manager)
            self.game.bullets.add(bullet)
            self.game.all_sprites.add(bullet)
            self.game.last_shot_time = current_time