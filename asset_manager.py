import pygame
from settings import Settings

class AssetManager:
    def __init__(self):
        self.images = {}

    def load_and_scale_image(self, name, path, scale_factor, fallback_size=(16,16)):
        try:
            image = pygame.image.load(path).convert_alpha()
            scaled_w = int(image.get_width() * scale_factor)
            scaled_h = int(image.get_height() * scale_factor)
            self.images[name] = pygame.transform.scale(image, (scaled_w, scaled_h))
        except Exception as e:
            print(f"Warning: failed to load {path}: {e}. Using placeholder for '{name}'.")
            scaled_w = int(fallback_size[0] * scale_factor)
            scaled_h = int(fallback_size[1] * scale_factor)
            surf = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
            surf.fill(Settings.Colors.MAGENTA)
            pygame.draw.rect(surf, Settings.Colors.WHITE, surf.get_rect(), 2)
            self.images[name] = surf

    def get_image(self, name):
        return self.images.get(name)