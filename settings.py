import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")

class Settings:
    IS_DEBUG_MODE = False
    SCALE_FACTOR = 2

    # ----------------------------------------------------
    
    class Screen:
        WIDTH = 800
        HEIGHT = 600
        CAPTION = "Planes"
        
    # ----------------------------------------------------

    class Colors:
        BG = (255, 255, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        MAGENTA = (255, 0, 255)
        
    # ----------------------------------------------------

    class Paths:
        PLAYER_IMAGE = os.path.join(SPRITES_DIR, "player.png")
        BULLET_IMAGE = os.path.join(SPRITES_DIR, "tile_0001.png")
        ENEMY_IMAGE = os.path.join(SPRITES_DIR, "ship_0022.png")
        TILESHEET = os.path.join(BACKGROUNDS_DIR, "tiles.png")

    # ----------------------------------------------------

    class Timers:
        SHOOT_DELAY = 500
        ENEMY_SPAWN_DELAY = 1000

    # ----------------------------------------------------

    class Player:
        MAX_HEALTH = 100
        COLLISION_DAMAGE = 20

        # Movement & Physics
        BASE_SPEED = 5
        MAX_FORWARD_SPEED = 400
        MAX_BACKWARD_SPEED = 200
        MAX_STRAFE_SPEED = 250
        FORWARD_ACCELERATION = 12
        STRAFE_ACCELERATION = 8
        FRICTION = 5
        
        # Visuals/Aesthetics
        MAX_BANK_ANGLE = 15  # Max tilt in degrees
        BANK_SPEED = 8       # How fast to tilt

    # ----------------------------------------------------

    class Enemy:
        SPEED = 3

    # ----------------------------------------------------
        
    class Bullet:
        SPEED = 10

    # ----------------------------------------------------

    class HUD:
        HEALTH_BAR_W = 100
        HEALTH_BAR_H = 10