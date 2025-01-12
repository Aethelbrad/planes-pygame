# TODO AssetManager class is doing too much. Refactor to separate concerns
# FIXME Debug screen flickering issue
# TODO Ensure all sprites are add to the same group for rendering
# TODO Add a game over screen

import pygame
import sys
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Screen dimensions
SCALE_FACTOR = 2  # Scale factor for images
PLAYER_SPEED = 5  # px per frame
BULLET_SPEED = 10  # px per frame
ENEMY_SPEED = 3  # px per frame
SHOOT_DELAY = 500  # ms
ENEMY_SPAWN_DELAY = 1000  # ms
BG_COLOR = (0, 0, 0)  # Black
PLAYER_MAX_HEALTH = 100  # Player health
PLAYER_IMAGE_PATH = "assets/sprites/player.png"
BULLET_IMAGE_PATH = "assets/sprites/tile_0001.png"
ENEMY_IMAGE_PATH = "assets/sprites/ship_0022.png"


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

class HUD:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_health(self, player):
        health_text = self.font.render(f"Health: {player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

    def draw_score(self, player):
        score_text = self.font.render(f"Score: {player.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))


class Player(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("player")
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Game Over!")

    def add_score(self, points):
        self.score += points


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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("bullet")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Planes")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Default font, size 36

        # Components
        self.event_handler = EventHandler(self)
        self.hud = HUD(self.screen, self.font)
    

        # Asset manager setup
        self.asset_manager = AssetManager(self.screen, self.font)
        self.asset_manager.load_and_scale_image("player", PLAYER_IMAGE_PATH, SCALE_FACTOR)
        self.asset_manager.load_and_scale_image("bullet", BULLET_IMAGE_PATH, SCALE_FACTOR)
        self.asset_manager.load_and_scale_image("enemy", ENEMY_IMAGE_PATH, SCALE_FACTOR)

        # Game entities
        self.player = Player(self.asset_manager)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.last_shot_time = 0
        self.last_enemy_spawn_time = 0
        self.running = True

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
            enemy = Enemy(self.asset_manager)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn_time = current_time

    def handle_collisions(self):
        bullet_enemy_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullet_enemy_collisions:
            self.player.add_score(len(bullet_enemy_collisions))

        player_collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_collisions:
            self.player.take_damage(len(player_collisions))

    def update(self):
        self.player.update()
        self.bullets.update()
        self.enemies.update()
        self.event_handler.handle_events()
        self.spawn_enemy()
        self.handle_collisions()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.hud.draw_health(self.player)
        self.hud.draw_score(self.player)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.event_handler.handle_shooting()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
