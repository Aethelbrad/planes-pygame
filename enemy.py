# enemy.py
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("enemy")
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH - 50), -50))
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Remove enemy from group when off screen