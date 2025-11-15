import pygame
from ..settings import Settings


class BaseState:
    def __init__(self, game):
        self.game = game # Store a reference to the main game object

    def handle_events(self, events):
        """Handle all user input for this state."""
        for event in events:
            if event.type == pygame.QUIT:
                return "QUIT" # Signal to the game to quit
        return self.get_next_state() # Return key for the next state

    def update(self, delta_time):
        """Update game logic for this state."""
        return "SELF"

    def draw(self, screen):
        """Draw all graphics for this state."""
        pass # Most states will override this
    
    def get_next_state(self):
        """Return the key for the next state (or self)."""
        return "SELF" # Default: stay in this state

class PlayingState(BaseState):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        # First, check for generic events (like quit)
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # e.g., "QUIT"

        # Handle state-specific inputs
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return "PAUSED" # Signal to transition to PAUSED
        
        # Pass keys to player update
        self.game.keys = pygame.key.get_pressed()
        return "SELF" # Stay in PLAYING state

    def update(self, delta_time):
        self.game.player.update(self.game.keys, delta_time)
        if self.game.keys[pygame.K_SPACE]:
            self.game.handle_shooting()

        self.game.spawn_enemy()
        self.game.handle_collisions()

        self.game.enemies.update()
        self.game.bullets.update()

        # Check for state transition
        if self.game.player.health <= 0:
            print("Shot Down")
            return "GAME_OVER" # Signal to transition
        
        return "SELF"

    def draw(self, screen):
        # All of your main drawing logic from Game.draw()
        screen.fill(Settings.Colors.BG)
        self.game.all_sprites.draw(screen)
        current_fps = int(self.game.clock.get_fps())
        self.game.hud.draw(screen, self.game.player, current_fps)


class PausedState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        # Pre-render text surfaces
        self.overlay = pygame.Surface((Settings.Screen.WIDTH, Settings.Screen.HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        
        self.pause_text = self.game.big_font.render("PAUSED", True, Settings.Colors.WHITE)
        self.resume_text = self.game.font.render("Press 'R' or 'P' to Resume", True, Settings.Colors.WHITE)
        self.quit_text = self.game.font.render("Press 'Q' to Quit", True, Settings.Colors.WHITE)
        
        self.p_rect = self.pause_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 - 50))
        self.r_rect = self.resume_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 + 20))
        self.q_rect = self.quit_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 + 70))

    def handle_events(self, events):
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # "QUIT"

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
                    return "PLAYING" # Signal to resume
                if event.key == pygame.K_q:
                    return "QUIT" # Signal to quit
        return "SELF"

    def update(self, delta_time):
        # Nothing happens when paused!
        pass

    def draw(self, screen):
        # IMPORTANT: Draw the playing screen *first*
        self.game.states["PLAYING"].draw(screen)
        
        # Then draw the pause overlay and text on top
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.pause_text, self.p_rect)
        screen.blit(self.resume_text, self.r_rect)
        screen.blit(self.quit_text, self.q_rect)


class GameOverState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        # Pre-render text surfaces
        self.overlay = pygame.Surface((Settings.Screen.WIDTH, Settings.Screen.HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        self.game_over_text = self.game.big_font.render("Shot Down", True, Settings.Colors.RED)
        self.score_text = self.game.font.render(f"Final Score: {self.game.player.score}", True, Settings.Colors.WHITE)
        self.quit_text = self.game.font.render("Press 'R' to Restart or ENTER to Quit", True, Settings.Colors.WHITE)        
        self.go_rect = self.game_over_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 - 50))
        self.score_rect = self.score_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 + 20))
        self.quit_rect = self.quit_text.get_rect(center=(Settings.Screen.WIDTH // 2, Settings.Screen.HEIGHT // 2 + 70))

    def handle_events(self, events):
        next_state_key = super().handle_events(events)
        if next_state_key != "SELF":
            return next_state_key # "QUIT"
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "QUIT" # Signal to quit
                
                if event.key == pygame.K_r: 
                    # Call the reset function on the main game object
                    self.game.reset_game()
                    # IMPORTANT: Re-instantiate the PlayingState to reset its internal state if needed
                    self.game.states["PLAYING"] = PlayingState(self.game)
                    return "PLAYING" # Restart the game

        return "SELF"

    def update(self, delta_time):
        # Nothing happens on game over screen
        pass

    def draw(self, screen):
        # Draw the final playing screen *first*
        self.game.states["PLAYING"].draw(screen)
        
        # Then draw the game over overlay and text
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.game_over_text, self.go_rect)
        screen.blit(self.score_text, self.score_rect)
        screen.blit(self.quit_text, self.quit_rect)