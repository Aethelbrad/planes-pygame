import os

# --- Path Setup (Stays at the top for foundation) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")

class Settings:
    """
    Main class holding all game configuration settings.
    Access constants using dot notation, e.g., Settings.Screen.WIDTH.
    """
    
    # --- GLOBAL & DEBUG ---
    IS_DEBUG_MODE = False
    SCALE_FACTOR = 2

    # ----------------------------------------------------
    
    class Screen:
        """Settings related to the display and window size."""
        WIDTH = 800
        HEIGHT = 600
        CAPTION = "Planes"
        
    # ----------------------------------------------------

    class Colors:
        """Standard color definitions."""
        BG = (255, 255, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        MAGENTA = (255, 0, 255)
        
    # ----------------------------------------------------

    class Paths:
        """File paths for game assets."""
        PLAYER_IMAGE = os.path.join(SPRITES_DIR, "player.png")
        BULLET_IMAGE = os.path.join(SPRITES_DIR, "tile_0001.png")
        ENEMY_IMAGE = os.path.join(SPRITES_DIR, "ship_0022.png")
        TILESHEET = os.path.join(BACKGROUNDS_DIR, "tiles.png")

    # ----------------------------------------------------

    class Timers:
        """Time-based constants in milliseconds (ms) and general speed values."""
        SHOOT_DELAY = 500
        ENEMY_SPAWN_DELAY = 1000

    # ----------------------------------------------------

    class Player:
        """All tuning variables and stats for the Player entity."""
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
        """All tuning variables for Enemy entities."""
        SPEED = 3

    # ----------------------------------------------------
        
    class Bullet:
        """All tuning variables for Bullet entities."""
        SPEED = 10

    # ----------------------------------------------------

    class HUD:
        """Constants for the Heads-Up Display elements."""
        HEALTH_BAR_W = 100
        HEALTH_BAR_H = 10