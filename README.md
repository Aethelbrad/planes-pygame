# Planes: Vertical Scrolling Shoot 'em Up

![Game Screenshot](screenshot.png)

A simple, physics-based vertical shoot 'em up built with Pygame-CE and featuring a clean, scalable game architecture.

## Features

| Feature                          | Description                                                                                     |
|----------------------------------|-------------------------------------------------------------------------------------------------|
| Smooth, Physics-Based Movement    | Player movement uses vector math, acceleration, friction, and "banking" for a responsive feel. |
| State Machine                    | Uses the State Design Pattern to manage different phases of the game (Playing, Paused, Game Over). |
| Scalable Architecture            | Code is organized into a dedicated src/ package using an Entity-based design.                  |
| Robust Asset Handling            | Uses an AssetManager with built-in error handling and automatic scaling.                       |
| Pixel-Perfect Collisions         | Utilizes pygame.mask for precise, pixel-based collision detection between the player, enemies, and bullets. |

## Installation & Setup

### Prerequisites

- Python 3.12 or higher

### Setup

1. Clone the Repository:

    ```bash
    git clone [repository_url]
    cd planes
    ```
2. Install Dependencies:

    ```bash
    pip install pygame-ce
    ```

3. Run the Game:

    ```bash
    python main.py
    ```

## Controls

| Key       | Action                                          |
|-----------|-------------------------------------------------|
| UP/DOWN   | Adjust forward/backward speed.                  |
| LEFT/RIGHT| Strafe and bank (tilt) the plane.              |
| SPACE     | Shoot primary weapon (fire rate limited by timer). |
| P / ESC   | Pause the game (from the Playing State).       |
| R         | Restart the game (from the Game Over State).   |

## Project Structure

``` 
planes/
├── assets/                  # All images, sprites, and potential maps/sounds
│   ├── sprites/
│   └── backgrounds/
│
├── src/                     # All core application logic (Python package)
│   ├── __init__.py          # Marks 'src' as a Python package
│   ├── game.py              # The main Game class, loop manager, and state handler
│   ├── settings.py          # All game constants, sizes, speeds, and file paths
│   ├── asset_manager.py     # Handles image loading, scaling, and error fallback
│   ├── hud.py               # Draws the Heads-Up Display (Score, Health, FPS)
│   │
│   ├── entities/            # Module for game objects (Player, Enemy, Bullet)
│   │   └── ...
│   └── states/              # Module for game phase logic (Playing, Paused, GameOver)
│       └── ...
│
└── main.py                  # Project entry point
```

## Future Enhancements

- Add sound effects and background music.
- Implement the Tiled map loader for ground textures and obstacles.
- Implement Power-Up drops with temporary effects
- Implement Tank (Ground) Enemies that follow different movement and attack patterns.
- Add multiple enemy formation patterns.
- Add different projectile types with unique speeds and damage profiles.
- Implement a high-score tracking system.
- Add more visual effects (explosions, smoke trails, etc.).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Assets from Kenney (http://kenney.nl) (THANK YOU!)
