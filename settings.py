import os

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCALE_FACTOR = 2
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
SHOOT_DELAY = 500 # ms
ENEMY_SPAWN_DELAY = 1000

BG_COLOR = (12, 12, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)

PLAYER_MAX_HEALTH = 100
PLAYER_COLLISION_DAMAGE = 20

HEALTH_BAR_W = 100
HEALTH_BAR_H = 10

# --- Player Tuning Variables ---
MAX_FORWARD_SPEED = 400
MAX_BACKWARD_SPEED = 200
MAX_STRAFE_SPEED = 250

FORWARD_ACCELERATION = 12
STRAFE_ACCELERATION = 8
FRICTION = 5

MAX_BANK_ANGLE = 15  # Max tilt in degrees
BANK_SPEED = 8       # How fast to tilt

IS_DEBUG_MODE = False

# Safe Path Management
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, "backgrounds")
PLAYER_IMAGE_PATH = os.path.join(SPRITES_DIR, "player.png")
BULLET_IMAGE_PATH = os.path.join(SPRITES_DIR, "tile_0001.png")
ENEMY_IMAGE_PATH = os.path.join(SPRITES_DIR, "ship_0022.png")
TILESHEET_PATH = os.path.join(BACKGROUNDS_DIR, "tiles.png")
