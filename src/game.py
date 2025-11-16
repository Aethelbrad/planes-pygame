import pygame
import sys
from src.settings import Settings
from src.asset_manager import AssetManager
from src.entities.entities import Player, Bullet, Enemy
from src.states.states import PlayingState, PausedState, GameOverState
from src.hud import HUD


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Planes")
        self.screen = pygame.display.set_mode((Settings.Screen.WIDTH, Settings.Screen.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # State
        self.running = True
        self.keys = pygame.key.get_pressed()

        # Assets
        self.asset_manager = AssetManager()
        self.asset_manager.load_and_scale_image("player", Settings.Paths.PLAYER_IMAGE, Settings.SCALE_FACTOR)
        self.asset_manager.load_and_scale_image("bullet", Settings.Paths.BULLET_IMAGE, Settings.SCALE_FACTOR)
        self.asset_manager.load_and_scale_image("enemy", Settings.Paths.ENEMY_IMAGE, Settings.SCALE_FACTOR)

        # Game systems
        self.hud = HUD(self.font)

        # Entities & groups
        self.player = Player(self.asset_manager)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Timers
        self.last_shot_time = 0
        self.last_enemy_spawn_time = 0
        
        # State
        self.states = {
            "PLAYING": PlayingState(self),
            "PAUSED": PausedState(self),
            "GAME_OVER": GameOverState(self)
        }
        self.current_state_key = "PLAYING"
        self.current_state = self.states[self.current_state_key]

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time > Settings.Timers.ENEMY_SPAWN_DELAY:
            enemy = Enemy(self.asset_manager)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn_time = current_time

    def handle_collisions(self):
        bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullet_enemy:
            hits = sum(len(v) for v in bullet_enemy.values())
            self.player.add_score(hits)

        player_hit = pygame.sprite.spritecollide(self.player, self.enemies, True) 
        if player_hit:
            damage = len(player_hit) * Settings.Player.COLLISION_DAMAGE
            self.player.take_damage(damage)
    
    def handle_shooting(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > Settings.Timers.SHOOT_DELAY:
            bullet = Bullet(self.player.rect.centerx, self.player.rect.top, self.asset_manager)
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shot_time = current_time

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            next_state_key_from_events = self.current_state.handle_events(events)
            next_state_key_from_update = self.current_state.update(delta_time)
            self.current_state.draw(self.screen)
            pygame.display.flip()
            
            # State transition logic
            if next_state_key_from_events == "QUIT":
                self.running = False
            
            elif next_state_key_from_events != "SELF" and next_state_key_from_events is not None:
                self.current_state_key = next_state_key_from_events
                self.current_state = self.states[self.current_state_key]
                
            elif next_state_key_from_update != "SELF" and next_state_key_from_update is not None:
                 self.current_state_key = next_state_key_from_update
                 
                 if self.current_state_key == "GAME_OVER":
                     # Re-instantiate GAME_OVER state to reset its score text
                     self.states["GAME_OVER"] = GameOverState(self) 
                     
                 self.current_state = self.states[self.current_state_key]

        pygame.quit()
        sys.exit()