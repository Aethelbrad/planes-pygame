# TODO AssetManager class is doing too much. Refactor to separate concerns
# FIXME Debug screen flickering issue
# TODO Ensure all sprites are add to the same group for rendering
# TODO Add a game over screen

import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR, BG_COLOR, PLAYER_IMAGE_PATH, BULLET_IMAGE_PATH, ENEMY_IMAGE_PATH, ENEMY_SPAWN_DELAY
from asset_manager import AssetManager
from player import Player
from hud import HUD
from enemy import Enemy
from event_handler import EventHandler


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


    def handle_collisions(self):
        bullet_enemy_collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullet_enemy_collisions:
            self.player.add_score(len(bullet_enemy_collisions))

        player_collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_collisions:
            self.player.take_damage(len(player_collisions))

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
            enemy = Enemy(self.asset_manager)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn_time = current_time

    def update(self):
        self.player.update()
        self.bullets.update()
        self.enemies.update()
        self.spawn_enemy()
        self.event_handler.handle_events()
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
