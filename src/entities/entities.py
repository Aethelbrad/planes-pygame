import pygame
import random
from src.settings import Settings


# -------------------
# Entities
# -------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.original_image = asset_manager.get_image("player")
        self.image = self.original_image.copy()
        self.pos = pygame.math.Vector2(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT - 50)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = Settings.Player.MAX_HEALTH
        self.score = 0
        self.current_velocity = pygame.math.Vector2(0, 0)
        self.current_rotation = 0.0

    @staticmethod
    def lerp(a, b, t):
        """gimme those smooth transitions"""
        return a + (b - a) * t

    def update(self, keys, delta_time):
        input_direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            input_direction.x -= 1
        if keys[pygame.K_RIGHT]:
            input_direction.x += 1
        if keys[pygame.K_UP]:
            input_direction.y -= 1
        if keys[pygame.K_DOWN]:
            input_direction.y += 1

        # NOTE: Do not normalize the input vector.
        # independent axis control is desired.

        target_velocity = pygame.math.Vector2(0, 0)
        target_velocity.x = input_direction.x * Settings.Player.MAX_STRAFE_SPEED
        
        if input_direction.y < 0: # Moving "forward" (up)
            target_velocity.y = input_direction.y * Settings.Player.MAX_FORWARD_SPEED
        else: # Moving "backward" (down) or neutral
            target_velocity.y = input_direction.y * Settings.Player.MAX_BACKWARD_SPEED

        accel_rate_x = Settings.Player.STRAFE_ACCELERATION if input_direction.x != 0 else Settings.Player.FRICTION
        accel_rate_y = Settings.Player.FORWARD_ACCELERATION if input_direction.y != 0 else Settings.Player.FRICTION

        # LERP the current velocity toward the target velocity
        self.current_velocity.x = self.lerp(
            self.current_velocity.x, 
            target_velocity.x, 
            accel_rate_x * delta_time
        )
        self.current_velocity.y = self.lerp(
            self.current_velocity.y, 
            target_velocity.y, 
            accel_rate_y * delta_time
        )

        # Target rotation is based *only* on horizontal input
        # (input_direction.x is -1, 0, or 1)
        target_rotation = -input_direction.x * Settings.Player.MAX_BANK_ANGLE
        # LERP the current rotation toward the target
        self.current_rotation = self.lerp(
            self.current_rotation, 
            target_rotation, 
            Settings.Player.BANK_SPEED * delta_time
        )
    
        self.image = pygame.transform.rotate(self.original_image, self.current_rotation)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos += self.current_velocity * delta_time
        self.rect.center = self.pos 
        self.rect.clamp_ip(pygame.Rect(0, 0, Settings.Screen.WIDTH, Settings.Screen.HEIGHT))

        self.pos.x, self.pos.y = self.rect.centerx, self.rect.centery

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def add_score(self, points):
        self.score += points

    def draw_debug(self, screen):
        DEBUG_COLOR = (0, 0, 250)
        points = self.mask.outline()
        offset_points = []
        for point in points:
            px = point[0] + self.rect.left
            py = point[1] + self.rect.top
            offset_points.append((px, py))
        if len(offset_points) > 2:
            pygame.draw.lines(screen, DEBUG_COLOR, True, offset_points, 2)

# -------------------
# Enemy Class
# -------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("enemy")
        self.rect = self.image.get_rect(center=(random.randint(50, Settings.Screen.WIDTH - 50), -50))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = Settings.Enemy.SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > Settings.Screen.HEIGHT:
            self.kill()

    def draw_debug(self, screen):
        DEBUG_COLOR = Settings.Colors.RED
        points = self.mask.outline()
        offset_points = []
        for point in points:
            px = point[0] + self.rect.left
            py = point[1] + self.rect.top
            offset_points.append((px, py))

        if len(offset_points) > 2:
            pygame.draw.lines(screen, DEBUG_COLOR, True, offset_points, 2)

# -------------------
# Bullet Class
# -------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, asset_manager):
        super().__init__()
        self.image = asset_manager.get_image("bullet")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = Settings.Bullet.SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw_debug(self, screen):
        DEBUG_COLOR = (0, 255, 0)
        pygame.draw.rect(screen, DEBUG_COLOR, self.rect, 2)
