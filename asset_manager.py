# asset_manager.py

import pygame
import sys

class AssetManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.images = {}

    def load_and_scale_image(self, name, path, scale_factor):
        try:
            image = pygame.image.load(path).convert_alpha()
            width = int(image.get_width() * scale_factor)
            height = int(image.get_height() * scale_factor)
            scaled_image = pygame.transform.scale(image, (width, height))
            self.images[name] = scaled_image
        except pygame.error as e:
            print(f"Error loading image: {path}. Error: {e}")
            sys.exit(1)

    def get_image(self, name):
        return self.images.get(name)