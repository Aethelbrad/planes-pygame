import pygame
import sys
from settings import *
from entities import Player, Bullet, Enemy

class AssetManager:
    def __init__(self):
        self.images = {}

    def load_and_scale_image(self, name, path, scale_factor, fallback_size=(16,16)):
        scaled_w = int(fallback_size[0] * scale_factor)
        scaled_h = int(fallback_size[1] * scale_factor)

        try:
            image = pygame.image.load(path).convert_alpha()
            scaled_w = int(image.get_width() * scale_factor)
            scaled_h = int(image.get_height() * scale_factor)
            
            self.images[name] = pygame.transform.scale(image, (scaled_w, scaled_h))
        except Exception as e:
            print(f"Warning: failed to load {path}: {e}. Using placeholder for '{name}'.")
            surf = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 255))  # Magenta placeholder
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
            self.images[name] = surf

    def get_image(self, name):
        return self.images.get(name)

class HUD:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, player, clock):
        # Health Text
        health_text = self.font.render(f"Health: {player.health}", True, BLACK)
        screen.blit(health_text, (10, 10))

        # Score Text
        score_text = self.font.render(f"Score: {player.score}", True, BLACK)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

        # Framerate
        fps = int(clock.get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, BLACK)
        fps_rect = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 40))
        screen.blit(fps_text, fps_rect)
        
        # Health Bar
        bar_width = 100
        bar_height = 10
        fill = (player.health / PLAYER_MAX_HEALTH) * bar_width
        
        outline_rect = pygame.Rect(10, 40, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 40, fill, bar_height)

        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 2)

class EventHandler:
    def __init__(self, game):
        self.game = game

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            if event.type == pygame.KEYDOWN:
                
                if self.game.game_over:
                    # --- GAME OVER STATE ---
                    if event.key == pygame.K_RETURN:
                        self.game.running = False

                elif self.game.paused:
                    # --- PAUSED STATE ---
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                        self.game.toggle_pause() # Resume
                    if event.key == pygame.K_q:
                        self.game.running = False # Quit
                
                else:
                    # --- PLAYING STATE ---
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.game.toggle_pause() # Pause

        return pygame.key.get_pressed()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Planes")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72) # Game Over / Pause font
        

        # Game State
        self.running = True
        self.game_over = False
        self.paused = False

        # Assets
        self.asset_manager = AssetManager()
        self.asset_manager.load_and_scale_image("player", PLAYER_IMAGE_PATH, SCALE_FACTOR, fallback_size=(16,16))
        self.asset_manager.load_and_scale_image("bullet", BULLET_IMAGE_PATH, SCALE_FACTOR, fallback_size=(8,8))
        self.asset_manager.load_and_scale_image("enemy", ENEMY_IMAGE_PATH, SCALE_FACTOR, fallback_size=(16,16))

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

    # --- Pause Toggle ---
    def toggle_pause(self):
        if not self.game_over:
            self.paused = not self.paused

    # --- Simulation ---
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY:
            enemy = Enemy(self.asset_manager)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn_time = current_time

    def handle_collisions(self):
        # Bullet vs. Enemy
        bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullet_enemy:
            hits = sum(len(v) for v in bullet_enemy.values())
            self.player.add_score(hits)

        # Player vs. Enemy
        # *** CHANGED: Switched to faster rect collision ***
        player_hit = pygame.sprite.spritecollide(self.player, self.enemies, True) 
        if player_hit:
            damage = len(player_hit) * PLAYER_COLLISION_DAMAGE
            self.player.take_damage(damage)
    
    def handle_shooting(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > SHOOT_DELAY:
            bullet = Bullet(self.player.rect.centerx, self.player.rect.top, self.asset_manager)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shot_time = current_time

    def update(self, keys, delta_time):
        self.player.update(keys, delta_time)
        if keys[pygame.K_SPACE]:
            self.handle_shooting()

        self.spawn_enemy()
        self.handle_collisions()

        self.enemies.update()
        self.bullets.update()

        if self.player.health <= 0:
            self.game_over = True
            print("Shot Down")

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.hud.draw(self.screen, self.player, self.clock)

        if self.game_over:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180)) 
            self.screen.blit(s, (0, 0))

            game_over_text = self.big_font.render("Shot Down", True, RED)
            score_text = self.font.render(f"Final Score: {self.player.score}", True, BLACK)
            quit_text = self.font.render("Press ENTER to Quit", True, BLACK)
            
            go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            
            self.screen.blit(game_over_text, go_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(quit_text, quit_rect)

        elif self.paused:

            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180)) 
            self.screen.blit(s, (0, 0))

            pause_text = self.big_font.render("PAUSED", True, WHITE)
            resume_text = self.font.render("Press 'R' or 'P' to Resume", True, WHITE)
            quit_text = self.font.render("Press 'Q' to Quit", True, WHITE)
            
            p_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            r_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            q_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            
            self.screen.blit(pause_text, p_rect)
            self.screen.blit(resume_text, r_rect)
            self.screen.blit(quit_text, q_rect)

        is_debug_mode = False  # TOGGLE DEBUG MODE HERE!

        if is_debug_mode:
            for sprite in self.all_sprites:
                if hasattr(sprite, 'draw_debug'):
                    sprite.draw_debug(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            keys = self.event_handler.handle_input()
            
            if not self.paused and not self.game_over:
                self.update(keys, delta_time)
            
            self.draw()

        pygame.quit()
        sys.exit()