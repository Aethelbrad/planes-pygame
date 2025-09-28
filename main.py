import pygame
import sys
import random
import os

# -------------------
# Constants
# -------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCALE_FACTOR = 2
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
SHOOT_DELAY = 500      # ms
ENEMY_SPAWN_DELAY = 1000
BG_COLOR = (12, 12, 20)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PLAYER_MAX_HEALTH = 100
PLAYER_COLLISION_DAMAGE = 20 # Damage taken when colliding with one enemy
TILE_SIZE = 16

# Safe Path Management
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")

PLAYER_IMAGE_PATH = os.path.join(SPRITES_DIR, "player.png")
BULLET_IMAGE_PATH = os.path.join(SPRITES_DIR, "tile_0001.png")
ENEMY_IMAGE_PATH = os.path.join(SPRITES_DIR, "ship_0022.png")
TILESHEET_PATH = os.path.join(BACKGROUNDS_DIR, "tiles.png")


# -------------------
# Utility: Tile Extraction
# -------------------
def get_tile(sheet, x, y, tile_size=TILE_SIZE, scale_factor=SCALE_FACTOR, spacing=1, margin=0):
    rect = pygame.Rect(
        margin + x * (tile_size + spacing),
        margin + y * (tile_size + spacing),
        tile_size,
        tile_size
    )
    tile = sheet.subsurface(rect).copy()
    if scale_factor != 1:
        tile = pygame.transform.scale(
            tile,
            (tile_size * scale_factor, tile_size * scale_factor)
        )
    return tile

# -------------------
# Asset Manager (images only) with graceful fallback
# -------------------
class AssetManager:
    def __init__(self):
        self.images = {}

    def load_and_scale_image(self, name, path, scale_factor, fallback_size=(16,16)):
        # Calculate the target scaled dimensions based on fallback size
        scaled_w = int(fallback_size[0] * scale_factor)
        scaled_h = int(fallback_size[1] * scale_factor)

        try:
            image = pygame.image.load(path).convert_alpha()
            # Overwrite scaled dimensions based on loaded image
            scaled_w = int(image.get_width() * scale_factor)
            scaled_h = int(image.get_height() * scale_factor)
            
            self.images[name] = pygame.transform.scale(image, (scaled_w, scaled_h))
        except Exception as e:
            print(f"Warning: failed to load {path}: {e}. Using placeholder for '{name}'.")
            
            # Use the calculated scaled dimensions for the placeholder
            surf = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 255))  # bright placeholder so you can see it
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
            self.images[name] = surf

    def get_image(self, name):
        return self.images.get(name)

# -------------------
# HUD
# -------------------
class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, player, clock):
        # Health Text
        health_text = self.font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

        # Score Text
        score_text = self.font.render(f"Score: {player.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        # Framerate
        fps = int(clock.get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, WHITE)
        fps_rect = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 40))
        screen.blit(fps_text, fps_rect)
        
        # Simple Health Bar (Optional)
        bar_width = 100
        bar_height = 10
        fill = (player.health / PLAYER_MAX_HEALTH) * bar_width
        
        outline_rect = pygame.Rect(10, 40, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 40, fill, bar_height)

        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)


# -------------------
# Entities
# -------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("player")
        self.pos = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50) # Use a vector for position
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.score = 0

# accept keys and act; this is called directly (not via group.update())
    def update(self, keys):
        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_DOWN]:
            direction.y += 1

        # Normalize prevent diagonal speed boost
        if direction.length() > 0:
            direction.normalize_ip()

        # Apply movement
        self.pos += direction * self.speed
        self.rect.center = self.pos # Update rect from vector pos

        # Clamp to screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pos.x, self.pos.y = self.rect.centerx, self.rect.centery # Update vec if clamped
        


    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            # Game class will handle game over state

    def add_score(self, points):
        self.score += points

class Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("enemy")
        # Start above the screen
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH - 50), -50))
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill() # Remove when off screen

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("bullet")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill() # Remove when off screen

# -------------------
# Input Handler
# -------------------
class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            # Allow quitting from game over state
            if self.game.game_over and event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_RETURN:
                    self.game.running = False # Or prompt for restart

        # return the current keys state to caller
        return pygame.key.get_pressed()

# -------------------
# Game
# -------------------
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Planes")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72) # For game over screen

        # Game State
        self.running = True
        self.game_over = False

        # Assets
        self.asset_manager = AssetManager()
        self.asset_manager.load_and_scale_image("player", PLAYER_IMAGE_PATH, SCALE_FACTOR, fallback_size=(16,16))
        self.asset_manager.load_and_scale_image("bullet", BULLET_IMAGE_PATH, SCALE_FACTOR, fallback_size=(8,8))
        self.asset_manager.load_and_scale_image("enemy", ENEMY_IMAGE_PATH, SCALE_FACTOR, fallback_size=(16,16))

        # Tilesheet optional (graceful fallback)
        try:
            sheet = pygame.image.load(TILESHEET_PATH).convert_alpha()
            self.grass_tile = get_tile(sheet, 0, 4, spacing=1, margin=0)
            self.dirt_tile = get_tile(sheet, 0, 6, spacing=1, margin=0)
        except Exception as e:
            print(f"Tilesheet not loaded ({TILESHEET_PATH}): {e}. Skipping tile drawing.")
            self.grass_tile = None
            self.dirt_tile = None

        # Game systems
        self.hud = HUD(self.font)
        self.event_handler = EventHandler(self)

        # Entities & groups
        self.player = Player(self.asset_manager)
        
        # Groups for rendering, updating, and colliding (all_sprites is for rendering/updating and subgroups are for collisions)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Timers
        self.last_shot_time = 0
        self.last_enemy_spawn_time = 0

    # --- Simulation ---
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
            enemy = Enemy(self.asset_manager)
            # Add to both groups for rendering and collision
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn_time = current_time

    def handle_collisions(self):
        # Bullet vs. Enemy
        bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullet_enemy:
            # Sum up hits to update score
            hits = sum(len(v) for v in bullet_enemy.values())
            self.player.add_score(hits)

        # Player vs. Enemy
        player_hit = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if player_hit:
            # Apply damage for each enemy hit
            damage = len(player_hit) * PLAYER_COLLISION_DAMAGE
            self.player.take_damage(damage)
    
    def handle_shooting(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > SHOOT_DELAY:
            bullet = Bullet(self.player.rect.centerx, self.player.rect.top, self.asset_manager)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shot_time = current_time

    def update(self, keys):
        if self.game_over:
            return

        # --- Handle Player Input ---
        self.player.update(keys)
        if keys[pygame.K_SPACE]:
            self.handle_shooting()

        # --- Update Entities --- TODO: all_sprites.update()?
        self.enemies.update()
        self.bullets.update()
        
        # --- Spawn Enemies & Handle Collisions ---
        self.spawn_enemy()
        self.handle_collisions()

        # --- Check Game Over ---
        if self.player.health <= 0:
            self.game_over = True
            print("Game Over!")

    # --- Rendering --- shouuld i change the name of draw to render?
    def draw(self):
        self.screen.fill(BG_COLOR)

        # optional tiles (for debug/demo)
        if self.grass_tile:
            self.screen.blit(self.grass_tile, (50, 50))
        if self.dirt_tile:
            self.screen.blit(self.dirt_tile, (100, 50))

        # draw sprites
        self.all_sprites.draw(self.screen)
        
        # Draw HUD (always visible)
        self.hud.draw(self.screen, self.player, self.clock)

        # Draw Game Over Screen
        if self.game_over:
            # Darken the screen slightly
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180)) 
            self.screen.blit(s, (0, 0))

            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            quit_text = self.font.render("Press ENTER to Quit", True, WHITE)
            
            go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            
            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    # --- Game Loop ---
    def run(self):
        while self.running:
            keys = self.event_handler.handle_input()

            self.update(keys)
            self.draw()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# -------------------
# Main
# -------------------
if __name__ == "__main__":
    Game().run()